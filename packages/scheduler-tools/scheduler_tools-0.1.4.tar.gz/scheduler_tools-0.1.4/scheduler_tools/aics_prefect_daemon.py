from datetime import datetime
from pathlib import Path
from time import sleep

from aicsdaemon import Daemon

from .load_custom_obj import load_custom_object
from .types import Pathlike


class AicsPrefectDaemon(Daemon):

    def __init__(self, slurm_prefs: dict, pidfile: Pathlike, stdin: Pathlike = None, stdout: Pathlike = None,
                 stderr: Pathlike = None, foreground: bool = False):
        super(AicsPrefectDaemon, self).__init__(pidfile=pidfile,
                                                stdout=stdout,
                                                stdin=stdin,
                                                stderr=stderr,
                                                foreground=foreground)
        print("AicsPrefectDaemon: pidfile: ", pidfile)
        print(f"prefs {slurm_prefs}")
        open(stdout, 'w').close() if stdout else None

        localdir = Path(pidfile).parent / "logs" / datetime.now().strftime("%Y%m%d_%H:%M:%S")

        self._cluster_obj_name = slurm_prefs['cluster_obj_name']

        self._cluster_prefs = slurm_prefs['cluster_conf'].copy()
        self._cluster_prefs['local_directory'] = localdir
        self._cluster_prefs['log_directory'] = localdir

        self._adapt_prefs = slurm_prefs['worker_conf'].copy()

    def run(self):

        object_kwargs = self._cluster_prefs
        if self._adapt_prefs is None:
            object_kwargs = {}

        cluster = load_custom_object(module_path=self._cluster_obj_name['module'],
                                     object_name=self._cluster_obj_name['object'],
                                     object_kwargs=object_kwargs)

        if self._adapt_prefs is not None:
            cluster.adapt(**self._adapt_prefs)

        print(f"{cluster.scheduler_info['address']}")
        print(f"{cluster.scheduler_info['services']['dashboard']}", flush=True)

        # this enables us to put something in stdin and if so this loop will
        # exit. Thus using the stdin="filepath" argument gives us a clean way to
        # shutdown the process
        mtime = self.stdin.stat().st_mtime
        while mtime == self.stdin.stat().st_mtime:
            sleep(5)


