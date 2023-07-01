"""
Polyglot v3 node server
Copyright (C) 2023 Steven Bailey
MIT License
Version 3.0.1 Jun 2023
"""
import asyncio
import colorsys
import udi_interface
import time
import json
from tuya_bulb_control import Bulb
from tuya_connector import (
    TuyaOpenAPI,)

LOGGER = udi_interface.LOGGER


class LightNode(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, new_id, deviceid, apiAccessId, apiSecret, apiEndpoint, apiRegion):
        super(LightNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll)
        self.new_id = new_id
        self.deviceid = deviceid
        self.DEVICELED_ID = deviceid
        self.apiAccessId = apiAccessId
        self.ACCESS_ID = apiAccessId
        self.apiSecret = apiSecret
        self.ACCESS_KEY = apiSecret
        self.apiEndpoint = apiEndpoint
        self.API_ENDPOINT = apiEndpoint
        self.apiRegion = apiRegion
        self.API_REGION = apiRegion
        self.SwStat(self)
        self.setDriver('ST', 1)
        # LOGGER.info('{name}\n{id_new}\n{ip}\n{key}\n'.format(
        # name=name, id_new=id_new, ip=ip, key=key,))

    # Light On
    def setSwOn(self, command):
        API_ENDPOINT = self.API_ENDPOINT
        ACCESS_ID = self.ACCESS_ID
        ACCESS_KEY = self.ACCESS_KEY
        DEVICELED_ID = self.DEVICELED_ID
        openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
        openapi.connect()

        commands = {'commands': [{'code': 'switch_led', 'value': True}]}
        openapi.post(
            '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
        time.sleep(.5)
        self.SwStat(self)

    # Light Off
    def setSwOff(self, command):
        API_ENDPOINT = self.API_ENDPOINT
        ACCESS_ID = self.ACCESS_ID
        ACCESS_KEY = self.ACCESS_KEY
        DEVICELED_ID = self.DEVICELED_ID

        openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
        openapi.connect()

        commands = {'commands': [{'code': 'switch_led', 'value': False}]}
        openapi.post(
            '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
        time.sleep(.5)
        self.SwStat(self)

    # Test Light Does Not Work version 1 Need To Fix
    def setclrflip(self, command):
        API_ENDPOINT = self.API_ENDPOINT
        ACCESS_ID = self.ACCESS_ID
        ACCESS_KEY = self.ACCESS_KEY
        DEVICELED_ID = self.DEVICELED_ID
        openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
        openapi.connect()

        # On Off Test
        LOGGER.info('\nDimmer Switch Test')
        commands = {'commands': [{'code': 'switch_led', 'value': True}]}
        openapi.post(
            '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
        LOGGER.info('On Test')
        time.sleep(2)
        self.SwStat(self)
        
        commands = {'commands': [{'code': 'switch_led', 'value': False}]}
        openapi.post(
            '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
        LOGGER.info('Off Test')
        time.sleep(2)
        self.SwStat(self)
        
        commands = {'commands': [{'code': 'switch_led', 'value': True}]}
        openapi.post(
            '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
        LOGGER.info('On Test')
        time.sleep(2)
        self.SwStat(self)
        

        # Dimmer Test
        LOGGER.info('\nDimmer Control Test')
        for level in range(11):
            LOGGER.info('    Level: %d%%' % (level*10))
            commands = {'commands': [
                {'code': 'colour_data', 'value': '{\"v\":' + str(level*100) + '}'}]}  # \"h\":0,\"s\":0,
            openapi.post(
                '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
            self.setDriver('GV3', level)
            time.sleep(2)

        # Test Modes
        LOGGER.info('\nTesting Bulb Modes')
        LOGGER.info('Colour Test')
        commands = {'commands': [{'code': 'work_mode', 'value': 'colour'}]}
        openapi.post(
            '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
        time.sleep(2)
        self.SwStat(self)
        
        LOGGER.info('Scene Test')
        commands = {'commands': [{'code': 'work_mode', 'value': 'scene'}]}
        openapi.post(
            '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
        time.sleep(2)
        self.SwStat(self)
        
        LOGGER.info('Music Test')
        commands = {'commands': [{'code': 'work_mode', 'value': 'music'}]}
        openapi.post(
            '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
        time.sleep(2)
        self.SwStat(self)
        
        LOGGER.info('White Test')
        commands = {'commands': [
            {'code': 'colour_data', 'value': '{\"h\":0,\"s\":0,\"v\":1000}'}]}
        openapi.post(
            '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
        time.sleep(2)
        self.SwStat(self)
        

        # Color Cycler
        LOGGER.info('\nColor Test')
        bulb = Bulb(
            client_id=self.ACCESS_ID,
            secret_key=self.ACCESS_KEY,
            device_id=self.DEVICELED_ID,
            region_key=self.API_REGION,
        )

        current_colour = json.loads(bulb.current_value(
            "colour_data"))  # For Version 2 # new_colour_v2
        # Conversion current HSV to RGB
        current_colour = colorsys.hsv_to_rgb(
            h=current_colour["h"] / 360,
            s=current_colour["s"] / 1000,
            v=current_colour["v"] / 1000,
        )
        # Convert the current RGB to format 0-255
        current_colour = tuple(map(lambda x: int(x * 255), current_colour))
        LOGGER.info(current_colour)
        # Get new RGB colour
        # colorchooser.askcolor(color=current_colour)[0]
        rainbow = {"red": [255, 0, 0], "orange": [255, 127, 0], "yellow": [255, 200, 0], "green": [
            0, 255, 0], "blue": [0, 0, 255], "indigo": [46, 43, 95], "violet": [139, 0, 255], "white": [255, 255, 255]}
        for x in range(2):
            for i in rainbow:
                r = rainbow[i][0]
                g = rainbow[i][1]
                b = rainbow[i][2]
                time.sleep(2)
                LOGGER.info('    %s (%d,%d,%d)' % (i, r, g, b))
                new_colour = (r, g, b)
                # Convert RGB coordinates to int
                new_colour = tuple(map(lambda x: int(x), new_colour))
                LOGGER.info(new_colour)
                # Set colour ✨
                # For Version 2 # set_colour_v2(new_color)
                bulb.set_colour(new_colour)
            else:
                LOGGER.info('Test Complete')
                return

    # Set Modes
    def modeOn(self, command):
        API_ENDPOINT = self.API_ENDPOINT
        ACCESS_ID = self.ACCESS_ID
        ACCESS_KEY = self.ACCESS_KEY
        DEVICELED_ID = self.DEVICELED_ID
        self.SwStat(self)
        openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
        openapi.connect()
        self.modeOn = int(command.get('value'))
        self.setDriver('GV4', self.modeOn)
        if self.modeOn == 0:
            commands = {'commands': [{'code': 'work_mode', 'value': 'colour'}]}
            openapi.post(
                '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
            LOGGER.info('Colour')
            time.sleep(.5)
            self.SwStat(self)
            time.sleep(1)
        elif self.modeOn == 1:
            commands = {'commands': [{'code': 'work_mode', 'value': 'scene'}]}
            openapi.post(
                '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
            LOGGER.info('Scene')
            time.sleep(.5)
            self.SwStat(self)
            time.sleep(1)
        elif self.modeOn == 2:
            commands = {'commands': [{'code': 'work_mode', 'value': 'music'}]}
            openapi.post(
                '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
            time.sleep(.5)
            self.SwStat(self)
            time.sleep(1)
        # Red
        elif self.modeOn == 3:
            commands = {'commands': [
                {'code': 'colour_data', 'value': '{\"h\":0,\"s\":1000,\"v\":1000}'}]}
            openapi.post(
                '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
            # (255, 0, 0)
            LOGGER.info('Red')
            time.sleep(.5)
            self.SwStat(self)
            time.sleep(1)
        # Orange
        elif self.modeOn == 4:
            commands = {'commands': [
                {'code': 'colour_data', 'value': '{\"h\":29,\"s\":1000,\"v\":1000}'}]}
            openapi.post(
                '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
            # (255, 127, 0)
            LOGGER.info('Orange')
            time.sleep(.5)
            self.SwStat(self)
            time.sleep(1)
        # Yellow
        elif self.modeOn == 5:
            commands = {'commands': [
                {'code': 'colour_data', 'value': '{\"h\":47,\"s\":1000,\"v\":1000}'}]}
            openapi.post(
                '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
            # (255, 200, 0)
            LOGGER.info('Yellow')
            time.sleep(.5)
            self.SwStat(self)
            time.sleep(1)
        # Green
        elif self.modeOn == 6:
            commands = {'commands': [
                {'code': 'colour_data', 'value': '{\"h\":120,\"s\":1000,\"v\":1000}'}]}
            openapi.post(
                '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
            # (0, 255, 0)
            LOGGER.info('Green')
            time.sleep(.5)
            self.SwStat(self)
            time.sleep(1)
        # Blue
        elif self.modeOn == 7:
            commands = {'commands': [
                {'code': 'colour_data', 'value': '{\"h\":240,\"s\":1000,\"v\":1000}'}]}
            openapi.post(
                '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
            # (0, 0, 255)
            LOGGER.info('Blue')
            time.sleep(1)
            self.SwStat(self)
            time.sleep(.5)
        # Indigo
        elif self.modeOn == 8:
            commands = {'commands': [
                {'code': 'colour_data', 'value': '{\"h\":243,\"s\":547,\"v\":1000}'}]}
            openapi.post(
                '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
            # (46, 43, 95)
            LOGGER.info('Indigo')
            time.sleep(1)
            self.SwStat(self)
            time.sleep(.5)
        # Violet
        elif self.modeOn == 9:
            commands = {'commands': [
                {'code': 'colour_data', 'value': '{\"h\":272,\"s\":1000,\"v\":1000}'}]}
            openapi.post(
                '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
            # (139, 0, 255)
            LOGGER.info('Violet')
            time.sleep(.5)
            self.SwStat(self)
            time.sleep(1)
        # White
        elif self.modeOn == 10:
            commands = {'commands': [
                {'code': 'colour_data', 'value': '{\"h\":0,\"s\":0,\"v\":1000}'}]}
            openapi.post(
                '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)
            LOGGER.info('White')
            time.sleep(.5)
            self.SwStat(self)
        else:
            pass

    # Led Level Does Not Work version 1 Need To Fix
    def setDim(self, command):
        API_ENDPOINT = self.API_ENDPOINT
        ACCESS_ID = self.ACCESS_ID
        ACCESS_KEY = self.ACCESS_KEY
        DEVICELED_ID = self.DEVICELED_ID
        self.SwStat(self)
        openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
        openapi.connect()

        ivr_one = 'percent'
        percent = int(command.get('value'))

        def set_percent(self, command):
            percent = int(command.get('value')*10)
        if percent < 1 or percent > 100:
            LOGGER.error('Invalid Level {}'.format(percent))
        else:
            # commands = {'commands': [
            #    {'code': 'colour_data', 'value': '{\"h\":272,\"s\":1000,\"v\":' + str(percent*10) + '}'}]}
            commands = {'commands': [
                {'code': 'bright_value', 'value': int(percent)*10}]}
            openapi.post(
                '/v1.0/iot-03/devices/{}/commands'.format(DEVICELED_ID), commands)

    def SwStat(self, command):
        API_ENDPOINT = self.API_ENDPOINT
        ACCESS_ID = self.ACCESS_ID
        ACCESS_KEY = self.ACCESS_KEY
        DEVICELED_ID = self.DEVICELED_ID
        openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
        openapi.connect()

        response1 = openapi.get(
            "/v1.0/iot-03/devices/{}".format(DEVICELED_ID) + "/status/")  # DEVICE_ID
        LOGGER.info(response1)
        for i in response1['result'][0:1]:
            LOGGER.info(i['value'])
            if i['value'] == True:
                self.setDriver('GV2', 1)
            elif i['value'] == False:
                self.setDriver('GV2', 0)

    def poll(self, polltype):
        if 'longPoll' in polltype:
            LOGGER.debug('longPoll (node)')
        else:
            self.SwStat(self)
            self.query(self)
            LOGGER.debug('shortPoll (node)')

    def query(self, command=None):
        self.SwStat(self)
        self.reportDrivers()

    drivers = [
        {'driver': 'ST', 'value': 1, 'uom': 2},
        {'driver': 'GV2', 'value': 0, 'uom': 2},
        {'driver': 'GV3', 'value': 0, 'uom': 51},
        {'driver': 'GV4', 'value': 0, 'uom': 25},

    ]

    id = 'lightv1'

    commands = {
        'LGTON': setSwOn,
        'LGTOF': setSwOff,
        # 'LGTCFLIP': setclrflip,
        'MODE': modeOn,
        # 'STLVL': setDim,
        'QUERY': query,
    }
