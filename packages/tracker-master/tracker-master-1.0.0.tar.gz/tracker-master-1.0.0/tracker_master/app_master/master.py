import logging.config
import os.path

from tracker_master.model.Message import Message
from tracker_master.model.Slave import Slave
from tracker_master.model.Master import Master

MASTER_CONFIGURATION_PATH = '../../master.conf'  # todo properties
SLAVES_CONFIGURATION_PATH = '../../slaves.conf'  # todo properties


def parse(message_string):
    return Message(hw_id=int(message_string[0:6]),
                   _type=int(message_string[8]),
                   charge=float(message_string[9:13]))


class TrackerMaster:

    def __init__(self):
        self.slave_manager = SlaveManager()
        self.master = None

    def initialize(self):
        self.init_from_conf()
        self.slave_manager.init_from_conf()

    def apply_configure(self, master_group_name, master_name):
        self.__write_conf(master_group_name, master_name)
        self.init_from_conf()

    def apply_slave_configure(self, _dict):
        self.slave_manager.apply_configure(_dict)

    def is_master_configured(self):
        return self.master and self.master.is_initialized()

    def is_slave_configured(self):
        return self.slave_manager.is_configured()

    def get_master(self) -> Master:
        return self.master

    def get_slaves(self):
        return self.slave_manager.slaves

    def init_from_conf(self):
        if not os.path.exists(MASTER_CONFIGURATION_PATH):
            return False

        with open(MASTER_CONFIGURATION_PATH, 'r') as f:
            master_group_name = f.readline()
            if not master_group_name:
                return False
            master_name = f.readline()
            if not master_name:
                return False

            self.master = Master(master_group_name.strip(), master_name.strip())
            return True

    def __write_conf(self, master_group_name, master_name):
        if not (master_group_name and master_name):
            return

        # todo make backup
        with open(MASTER_CONFIGURATION_PATH, 'w') as f:
            f.write('%s\n' % master_group_name)
            f.write('%s\n' % master_name)


class SlaveManager:

    def __init__(self, zbx_client=None):
        self.logger = logging.getLogger(SlaveManager.__name__)
        self.zbx_client = zbx_client
        self.slaves = dict()
        self.hw_id_to_slaves = dict()
        pass

    def apply_configure(self, _dict):
        self.__write_conf(_dict)
        self.slaves = _dict

    def is_configured(self):
        return self.slaves and len(self.slaves) > 0

    def get_slave(self, hw_id):
        return self.hw_id_to_slaves[hw_id]

    def init_from_conf(self):
        if not os.path.exists(SLAVES_CONFIGURATION_PATH):
            return False

        slaves = dict()
        hw_id_to_slaves = dict()
        with open(SLAVES_CONFIGURATION_PATH, 'r') as f:
            line = f.readline()
            while line:
                zbx_slave_id, hw_id = line.split('\t')
                slave = Slave(int(hw_id), int(zbx_slave_id))
                slaves[int(zbx_slave_id)] = slave
                hw_id_to_slaves[int(hw_id)] = slave
                line = f.readline()
            self.slaves = slaves
            self.hw_id_to_slaves = hw_id_to_slaves

        return True

    def __write_conf(self, slaves):
        # todo make backup
        with open(SLAVES_CONFIGURATION_PATH, 'w') as f:
            for zbx_slave_id, slave in slaves.items():
                assert isinstance(slave, Slave)
                f.write('%s\t%s\n' % (zbx_slave_id, slave.hw_id))


class SlavesConfigurer:

    def __init__(self):
        self.slaves = dict()
        self.logger = logging.getLogger(SlavesConfigurer.__name__)

    def register_slave(self, msg):
        zbx_slave_number = len(self.slaves) + 1
        slave = Slave(msg.hw_id, zbx_slave_number)
        if slave in self.slaves.values():
            self.logger.info('Slave %s %s is already existed' % (zbx_slave_number, msg.hw_id))
            return False

        self.slaves[zbx_slave_number] = slave
        self.logger.info('Slave %s %s has registered' % (zbx_slave_number, msg.hw_id))
        return True
