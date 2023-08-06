import asyncio
import json
import logging
import os
import re
import subprocess
import sys
from pathlib import Path

import asyncssh
import psutil

from scheduler_tools.PrefectPreferences import PrefectPreferences
from scheduler_tools.ScpDaskPrefs import run_scp_copy_dask_prefs, \
    run_launch_dask_head_node, run_watch_and_report_ports, shutdown_dask_head_node
from scheduler_tools.types import PathDict, PrefDict
from scheduler_tools.default_dask_prefs import default_dask_prefs
from scheduler_tools.default_ssh_prefs import default_ssh_prefs


class Connector:

    def __init__(self, dask_prefs: dict = None, prefs: PathDict = None):

        self._dask_scheduler_ip = None
        self._dask_scheduler_port = None
        self._dask_dashboard_port = None
        self._tunnel = None
        self._pattern = re.compile(r"tcp://(?P<host>[\d\.]+):(?P<DASK_PORT>\d+)\s+(?P<DASHBOARD_PORT>\d+)$",
                                   re.MULTILINE)

        if prefs is None:
            prefs = default_ssh_prefs()
        elif isinstance(prefs, (Path, str)):
            localfolder = Path(prefs).parent
            if Path(prefs).expanduser().exists():
                with open(Path(prefs).expanduser(), 'r') as fp:
                    prefs = json.load(fp)
                print(f"localfolder: {localfolder}")
                if 'localfolder' not in prefs.keys():
                    prefs['localfolder'] = localfolder
            else:
                raise FileNotFoundError(f"{prefs} file does not exists.")
            print("survived elsif")
        print("in pref")
        self._pref = PrefectPreferences(prefs)
        print("from pref")

        if dask_prefs is None:
            self._dask_prefs = default_dask_prefs()
        else:
            self._dask_prefs = dask_prefs
        print("survived init")
        self.serialize_and_push_prefs()

    def serialize_and_push_prefs(self):
        # serialize the json prefs
        dask_prefs_path = self._pref.default_path().expanduser() / "dask_prefs.json"
        print(f"in serialize: {dask_prefs_path}")
        with open(str(dask_prefs_path), 'w') as fp:
            json.dump(self._dask_prefs, fp)
        # scp json to cluster
        try:
            print(f"relp: {self._dask_prefs['remote_conf']['path']}")
            relative_path = Path(self._dask_prefs['remote_conf']['path'])
            print(f"rel path: {relative_path}")
            asyncio.get_event_loop().run_until_complete(run_scp_copy_dask_prefs(dask_prefs_path,
                                                                                self._pref.gateway_url,
                                                                                self._pref.identity_file,
                                                                                relative_path))
        except (OSError, asyncssh.Error) as exc:
            sys.exit('SCP connection failed: ' + str(exc))
        print("survived serialize")

    def run_command(self):
        self.serialize_and_push_prefs()
        remote_home = self._dask_prefs['remote_conf']['path']
        try:
            asyncio.get_event_loop().run_until_complete(run_launch_dask_head_node(self._pref.gateway_url,
                                                                                  self._pref.identity_file,
                                                                                  self._dask_prefs,
                                                                                  self._pref,
                                                                                  remote_home))
        except (OSError, asyncssh.Error) as exc:
            sys.exit('Launch dask cluster failed: ' + str(exc))

    def stop_forward_if_running(self, query=True):
        pid_str = self._pref.read_ssh_pid()
        # if there is no pid or the pid isn't valid return
        if pid_str is None or not psutil.pid_exists(int(pid_str)):
            self._pref.remove_ssh_pid()
            return
        # if the pid doesn't match the command issued
        ppid = psutil.Process(pid=int(pid_str))
        children = ppid.children(recursive=True)
        if ppid and children:
            logging.info(f"Shutting down PID({ppid.pid}): {ppid.name()}")
            for child in children:
                logging.info(f"Shutting down PID({child.pid}): {child.name()}")
            remove = True
            if query:
                data = input("Shutdown the above processes? [YES/no]")
                pat = r'\s*(no|NO|No)\s*'
                remove = not re.match(pat, data)
            if remove:
                for child in children:
                    child.kill()
                ppid.kill()
        # remove the file
        self._pref.ssh_pid_path().unlink()

    @property
    def local_dask_port(self):
        return self._pref.local_dask_port
    
    @property
    def local_dashboard_port(self):
        return self._pref.local_dashboard_port

    def forward_ports(self):
        rel_folder = self._pref.default_path().expanduser().relative_to(Path().home())
        info = asyncio.get_event_loop().run_until_complete(
            run_watch_and_report_ports(self._pref.gateway_url, self._pref.identity_file, rel_folder)
        )

        ssh_command = (f"ssh-add {self._pref.identity_file} ; "
                       f"ssh -o StrictHostKeyChecking=no "
                       f"-N -A -J {self._pref.gateway_url} "
                       f"-L {self._pref.local_dask_port}:{info['host']}:{info['DASK_PORT']} "
                       f"-L {self._pref.local_dashboard_port}:{info['host']}:{info['DASHBOARD_PORT']} "
                       f"{self._pref.username}@{info['host']}"
                       )

        print(ssh_command)
        self._tunnel = subprocess.Popen(ssh_command, shell=True, executable='/bin/bash')
        os.environ['DASK_PORT'] = info['DASK_PORT']
        print(f"\nTo connect to remote server use \n\tDask:\t \t localhost:{self._pref.local_dask_port}\n"
              f"\tDashboard:\t localhost:{self._pref.local_dashboard_port}")
        self._pref.write_ssh_pid(pid=self._tunnel.pid)

    def stop_dask(self):
        job_id = self._pref.read_prefect_job_id()
        pidfile = Path(self._dask_prefs['remote_conf']['path']) / "pidfile"
        if job_id is None:
            logging.warning("Job ID is None")
            return
        logging.info(f"Cancelling Slurm Head Node: {job_id}")
        try:
            asyncio.get_event_loop().run_until_complete(shutdown_dask_head_node(self._pref.gateway_url,
                                                                                self._pref.identity_file,
                                                                                job_id,
                                                                                pidfile))
        except asyncssh.process.ProcessError as e:
            logging.warn(f"it looks like the remote process was already shutdown: {e}")

        self.stop_forward_if_running(query=False)

    def __enter__(self):
        self.run_command()
        self.stop_forward_if_running()
        self.forward_ports()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop_dask()
        self.stop_forward_if_running()
