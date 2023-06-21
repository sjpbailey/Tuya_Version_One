import json

import udi_interface
import tinytuya

LOGGER = udi_interface.LOGGER


class TuyaNode(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, device):
        super(TuyaNode, self).__init__(polyglot, primary, address, name)
        self.address = address
        self.name = name
        self.device = device

        self.tuya_device = tinytuya.BulbDevice(
            self.device['gwId'], self.device['ip'], self.device['key'])
        LOGGER.info(self.tuya_device)
        self.tuya_device.set_version(3.3)

        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)

    def poll(self, pollType):
        if 'shortPoll' in pollType:
            LOGGER.info('shortPoll (node)')
            self.query()
        else:
            LOGGER.info('longPoll (node)')
            pass

    def query(self):
        LOGGER.info("Query sensor {}".format(self.address))
        LOGGER.info("Node Name {}".format(self.name))
        node_status = self.tuya_device.status()
        LOGGER.info("Node Status {}".format(str(node_status)))
        node_brightness = node_status['dps']['107']/10
        LOGGER.info("Node Brightness {}".format(node_brightness))
        node_duration = node_status['dps']['105'].replace('MIN', '')
        LOGGER.info("Node On Time {}".format(node_duration))
        switch_status = 0
        if node_status['dps']['101'] == 'AUTO':
            switch_status = 3
        elif node_status['dps']['101'] == 'MODE_MAN_ON':
            switch_status = 1
        elif node_status['dps']['101'] == 'MODE_MAN_OFF':
            switch_status = 2
        self.setDriver('GV1', int(node_brightness), True)
        if node_duration != 'TEST':
            self.setDriver('GV2', int(node_duration), True)
        else:
            self.setDriver('GV2', 0, True)
        self.setDriver('GV3', switch_status, True)

    def start(self):
        self.query()

    def cmd_set_on(self, cmd):
        self.tuya_device.set_value('101', 'MODE_MAN_ON')
        self.setDriver('GV3', 1, True)

    def cmd_set_off(self, cmd):
        self.tuya_device.set_value('101', 'MODE_MAN_OFF')
        self.setDriver('GV3', 2, True)

    def cmd_set_auto(self, cmd):
        self.tuya_device.set_value('101', 'AUTO')
        self.setDriver('GV3', 3, True)

    def cmd_set_bright(self, cmd):
        calc_bright = int(cmd['value']) * 10
        self.tuya_device.set_value('107', calc_bright)
        self.setDriver('GV1', int(cmd['value']), True)

    def cmd_set_duration(self, cmd):
        LOGGER.debug(f"cmd_set_duration value: {cmd['value']}")
        if int(cmd['value']) != 0:
            self.tuya_device.set_value('105', cmd['value'] + 'MIN')
        else:
            self.tuya_device.set_value('105', 'TEST')
        self.setDriver('GV2', int(cmd['value']), True)

    id = 'tuyanode'

    commands = {
        'SET_BRIGHTNESS': cmd_set_bright,
        'SET_ONTIME': cmd_set_duration,
        'ON': cmd_set_on,
        'OFF': cmd_set_off,
        'AUTO': cmd_set_auto,
        'QUERY': query
    }

    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
        {'driver': 'GV1', 'value': 0, 'uom': '51'},
        {'driver': 'GV2', 'value': 0, 'uom': '45'},
        {'driver': 'GV3', 'value': 0, 'uom': '25'}
    ]
