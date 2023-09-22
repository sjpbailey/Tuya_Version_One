"""
Polyglot v3 node server
Copyright (C) 2023 Steven Bailey
MIT License
Version 3.0.1 Jun 2023
"""
import asyncio
from select import POLLIN
import udi_interface
import time
import json
import logging
from tuya_connector import (
    TuyaOpenAPI,
    TuyaOpenPulsar,
    TuyaCloudPulsarTopic,
    TUYA_LOGGER,)

LOGGER = udi_interface.LOGGER


class PirNode(udi_interface.Node):
    def __init__(self, polyglot, primary, address, name, new_id, deviceid, apiAccessId, apiSecret, apiEndpoint):
        super(PirNode, self).__init__(polyglot, primary, address, name)
        self.poly = polyglot
        self.lpfx = '%s:%s' % (address, name)
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.START, self.start, address)
        self.poly.subscribe(self.poly.POLL, self.poll, self.poll) #, self.poll
        self.new_id = new_id
        self.deviceid = deviceid
        self.DEVICESW_ID = deviceid
        self.apiAccessId = apiAccessId
        self.ACCESS_ID = apiAccessId
        self.apiSecret = apiSecret
        self.ACCESS_KEY = apiSecret
        self.apiEndpoint = apiEndpoint
        self.API_ENDPOINT = apiEndpoint
        self.name = name
        self.DEVICE_NAME = name
        LOGGER.info(name)
        time.sleep(2)
        self.BtStat(self)
        self.SwStat(self)

    def SwStat(self, command):
        API_ENDPOINT = self.API_ENDPOINT
        ACCESS_ID = self.ACCESS_ID
        ACCESS_KEY = self.ACCESS_KEY
        DEVICESW_ID = self.DEVICESW_ID
        openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
        openapi.connect()
        response1 = openapi.get("/v1.0/iot-03/devices/{}".format(DEVICESW_ID) + "/status/")
        LOGGER.info(self.name)
        LOGGER.info(response1)
        # Motion Detected
        for i in response1['result'][0:1]:
            if i['value'] == 'presence':
                self.setDriver('GV2', 1)
            elif i['value'] == 'none':
                self.setDriver('GV2', 0)
            pass
        # checking_result
        for i in response1['result'][4:5]:
            if i['value'] == 'checking':
                self.setDriver('GV10', 0)
            elif i['value'] == 'check_success':
                self.setDriver('GV10', 1)
            elif i['value'] == 'check_failure':
                self.setDriver('GV10', 2)
            elif i['value'] == 'others':
                self.setDriver('GV10', 3)
            elif i['value'] == 'comm_fault':
                self.setDriver('GV10', 4)
            elif i['value'] == 'radar_fault':
                self.setDriver('GV10', 5)
        
        
        #### Device Online Status
        response = openapi.get("/v1.0/devices/{}".format(DEVICESW_ID))
        LOGGER.info(response['result']['online'])
        if response['result']['online'] == True:
            LOGGER.info(response['result']['online'])
            self.setDriver('ST', 1)
        if response['result']['online'] == False:
            LOGGER.info(response['result']['online'])
            self.setDriver('ST', 0)
        else:
            pass
                
    def BtStat(self, command):
        API_ENDPOINT = self.API_ENDPOINT
        ACCESS_ID = self.ACCESS_ID
        ACCESS_KEY = self.ACCESS_KEY
        DEVICESW_ID = self.DEVICESW_ID
        DEVICE_NAME = self.DEVICE_NAME
        openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
        openapi.connect()
        response1 = openapi.get(
            "/v1.0/iot-03/devices/{}".format(DEVICESW_ID) + "/status/")
        LOGGER.info(DEVICE_NAME)
        LOGGER.info(response1)
        for i in response1['result'][1:2]:
            LOGGER.info(i['value'])
            self.setDriver('GV3', i['value'])
        for i in response1['result'][2:3]:
            LOGGER.info(i['value'])
            self.setDriver('GV4', i['value'])
        for i in response1['result'][3:4]:
            LOGGER.info(i['value'])
            self.setDriver('GV5', i['value'])
        for i in response1['result'][5:6]:
            LOGGER.info(i['value'])
            self.setDriver('GV9', i['value'])
            
    # Set Sensitivity
    def setDim(self, command):
        API_ENDPOINT = self.API_ENDPOINT
        ACCESS_ID = self.ACCESS_ID
        ACCESS_KEY = self.ACCESS_KEY
        DEVICESW_ID = self.DEVICESW_ID
        openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
        openapi.connect()
        self.BtStat(self)
        self.SwStat(self)

        ivr_one = 'percent'
        percent = int(command.get('value'))

        def set_percent(self, command):
            percent = int(command.get('value'))
        if percent < 1 or percent > 10:
            LOGGER.error('Invalid Level {}'.format(percent))
        else:
            commands = {'commands': [
                {'code': 'sensitivity', 'value': int(percent)}]}
            openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICESW_ID), commands)
            self.setDriver('GV6', percent)
            LOGGER.info('Sensitivity = ' + str(percent) + ' Level')
            
    # Set Near Detection
    def setNar(self, command):
        API_ENDPOINT = self.API_ENDPOINT
        ACCESS_ID = self.ACCESS_ID
        ACCESS_KEY = self.ACCESS_KEY
        DEVICESW_ID = self.DEVICESW_ID
        openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
        openapi.connect()
        self.BtStat(self)
        self.SwStat(self)

        ivr_one = 'percent'
        percent = int(command.get('value'))

        def set_percent(self, command):
            percent = int(command.get('value'))
        if percent < 0 or percent > 1000:
            LOGGER.error('Invalid Level {}'.format(percent))
        else:
            commands = {'commands': [{'code': 'near_detection', 'value': int(percent)}]}
            openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICESW_ID), commands)
            self.setDriver('GV7', percent)
            LOGGER.info('near_detection = ' + str(percent) + ' Level')
            
    # Set Far Detection
    def setFar(self, command):
        API_ENDPOINT = self.API_ENDPOINT
        ACCESS_ID = self.ACCESS_ID
        ACCESS_KEY = self.ACCESS_KEY
        DEVICESW_ID = self.DEVICESW_ID
        openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
        openapi.connect()
        self.BtStat(self)
        self.SwStat(self)

        ivr_one = 'percent'
        percent = int(command.get('value'))

        def set_percent(self, command):
            percent = int(command.get('value'))
        if percent < 0 or percent > 1000:
            LOGGER.error('Invalid Level {}'.format(percent))
        else:
            commands = {'commands': [{'code': 'far_detection', 'value': int(percent)}]}
            openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICESW_ID), commands)
            self.setDriver('GV8', percent)
            LOGGER.info('near_detection = ' + str(percent) + ' Level')

    def poll(self, polltype):
        if 'longPoll' in polltype:
            LOGGER.debug('longPoll (node)')
        else:
            self.BtStat(self)
            self.SwStat(self)
            LOGGER.debug('shortPoll (node)')

    def query(self, command=None):
        self.BtStat(self)
        self.SwStat(self)
        self.reportDrivers()

    drivers = [
        {'driver': 'ST', 'value': 0, 'uom': 2, 'name': 'Online'},
        {'driver': 'GV2', 'value': 0, 'uom': 2, 'name': 'Status'},
        {'driver': 'GV3', 'value': 0, 'uom': 56, 'name': 'Sensitivity'},
        {'driver': 'GV4', 'value': 0, 'uom': 56, 'name': 'Near Detection'},
        {'driver': 'GV5', 'value': 0, 'uom': 56, 'name': 'Far Detection'},
        {'driver': 'GV6', 'value': 0, 'uom': 56, 'name': 'Sensitivity Setp'},
        {'driver': 'GV7', 'value': 0, 'uom': 38, 'name': 'Near Detection'},
        {'driver': 'GV8', 'value': 0, 'uom': 38, 'name': 'Far Detection'},
        {'driver': 'GV9', 'value': 0, 'uom': 56, 'name': 'Target Distance closest'},
        {'driver': 'GV10', 'value': 0, 'uom': 25, 'name': 'Checking Result'},
    ]

    id = 'pir2'

    commands = {
        'QUERY': query,
        'STLVL': setDim,
        'STNAR': setNar,
        'STFAR': setFar,
    }
