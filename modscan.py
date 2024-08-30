import pandas as pd 
from pymodbus.client.sync import ModbusSerialClient 
from pymodbus.exceptions import ModbusIOException, ConnectionException
import logging 
import time 


class ModbusRTUScaner(object):
    def __init__(self, port, baudrate=9600, parity='N', stopbits=1,
                 bytesize=8,  timeout=1): 
        
        self.client = ModbusSerialClient(
            method='rtu',
            port=port,
            baudrate=baudrate,
            parity=parity,
            stopbits=stopbits,
            bytesize=bytesize,
            timeout=timeout
        ) 
        
        self.is_connected = False
        self.log_setup() 
        
    def log_setup(self):
        logging.basicConfig(filename='modbus_rtu.log',
                            level=logging.INFO,
                            format='%(asctime)s %(levelname)s: %(message)s')
        
    def connect(self):
        self.is_connected = self.client.connect() 
        if self.is_connected:
            logging.info('Connected to RS-485 successfuly!')
        else:
            logging.error('Failed to connect to RS-485!!!')
            
    def disconnect(self): 
        self.client.close() 
        self.is_connected = False 
        logging.info('Disconnected from RS-485 successfuly!')
        
    def reconnect(self, retrise=3, delay=5): 
        for i in range(retrise): 
            if self.client.connect():
                self.is_connected = True 
                logging.info('Reconnected successfuly.')
                return True 
            
        