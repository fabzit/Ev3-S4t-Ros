from iotronic_lightningrod.modules.plugins import Plugin
import subprocess

from oslo_log import log as logging
LOG = logging.getLogger(__name__)


class Worker(Plugin.Plugin):

    def __init__(self, uuid, name, q_result, params=None):
        super(Worker, self).__init__(uuid, name, q_result, params)

    def run(self):
        LOG.info("PROVO AD AVVIARE")
        path = '/var/lib/iotronic/plugins/{}/{}.py'.format(str(self.params['plugin_id']), str(self.params['plugin_id']))
        subprocess.call(['python3', path])
        LOG.info("OK") 
        self.q_result.put("AVVIATO!")