#!/usr/bin/env python3
"""
Polyglot v3 node server Lighting Version
Copyright (C) 2021 For James Paul Modified by Steven Bailey
"""
import logging
from nodes import tuya_light_node_v1
from nodes import tuya_light_node
from nodes import tuya_switch_node
from nodes import TuyaNode
from nodes import TuyaController
import udi_interface
import sys

LOGGER = udi_interface.LOGGER
LOG_HANDLER = udi_interface.LOG_HANDLER


if __name__ == "__main__":
    try:
        LOGGER.debug("Staring Tuya Cloud Interface")
        polyglot = udi_interface.Interface([TuyaController, TuyaNode])
        polyglot.start()
        control = TuyaController(
            polyglot, 'controller', 'controller', 'Tuya Cloud')
        polyglot.runForever()
    except (KeyboardInterrupt, SystemExit):
        polyglot.stop()
        sys.exit(0)
    except Exception as err:
        LOGGER.error('Exception: {0}'.format(err), exc_info=True)
        sys.exit(0)
