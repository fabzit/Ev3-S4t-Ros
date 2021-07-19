from iotronic_lightningrod.modules.plugins import Plugin
import subprocess

from oslo_log import log as logging
LOG = logging.getLogger(__name__)


class Worker(Plugin.Plugin):

    def __init__(self, uuid, name, q_result, params=None):
        super(Worker, self).__init__(uuid, name, q_result, params)

    def run(self):
        LOG.info("PROVO AD AVVIARE")
        subprocess.call(['python3', '/var/lib/iotronic/plugins/39251657-ad3d-4dad-ab92-fda00deeb461/39251657-ad3d-4dad-ab92-fda00deeb461.py'])
        LOG.info("OK ") 
        self.q_result.put("AVVIATO!")