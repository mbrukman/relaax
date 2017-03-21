import sys
import logging
from honcho.manager import Manager

from relaax.common.python.cmdl.cmdl_config import options

log = logging.getLogger("relaax")


class RManager(Manager):

    def __init__(self, *args, **kwargs):
        super(RManager, self).__init__(*args, **kwargs)

    def _any_stopped(self):
        clients = []
        for _, p in self._processes.iteritems():
            if p['process'].name.startswith('client'):
                clients.append(p.get('returncode') is not None)
        if len(clients):
            return all(clients)
        else:
            super(RManager, self)._any_stopped()


class CmdlRun(object):

    def __init__(self):
        self.nobuffer = 'PYTHONUNBUFFERED=true'
        self.cmdl = "--config %s " % options.config
        if options.cmdl_log_level:
            self.cmdl += "--log-level %s" % options.cmdl_log_level

    def run_componenets(self):

        manager = RManager()

        self.run_parameter_server(manager)
        self.run_rlx_server(manager)
        self.run_client(manager)

        manager.loop()
        sys.exit(manager.returncode)

    def run_parameter_server(self, manager):
        if options.run in ['all', 'servers', 'parameter-server']:
            manager.add_process('parameter-server',
                                '%s relaax-parameter-server %s'
                                % (self.nobuffer, self.cmdl))

    def run_rlx_server(self, manager):
        if options.run in ['all', 'servers', 'rlx-server']:
            manager.add_process('rlx-server',
                                '%s relaax-rlx-server %s'
                                % (self.nobuffer, self.cmdl))

    def run_client(self, manager):
        if options.run in ['all', 'client']:
            if options.client:
                self.run_all_clients(manager)
            else:
                COLOR_SEQ = "\033[1;31m"
                RESET_SEQ = "\033[0m"
                log.info(COLOR_SEQ+"No client specified"+RESET_SEQ)

    def run_all_clients(self, manager):
        if options.concurrent_clients > 1:
            count = 0
            while count < options.concurrent_clients:
                self.run_one_client('client-%d' % count, manager)
                count += 1
        else:
            self.run_one_client('client', manager)

    def run_one_client(self, process_name, manager):
        manager.add_process(
            process_name, '%s python %s' % (self.nobuffer, options.client))


run_all = CmdlRun().run_componenets