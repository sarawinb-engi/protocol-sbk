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
            else:
                logging.warning(f"Reconnection attempt {i+1} failed. Retrying in {delay} second...")
                time.sleep(delay)
        logging.error("Failed to reconnect after several attemps.")
        return False 
    
    def transform_value(self, raw_value, date_type):
        
        return raw_value 
    
    def scan(self, start_address=0, end_address=1000, unit_ids=range(1,247), batch_size=100):
        all_data = []
        for unit_id in unit_ids:
            for start in range(start_address, end_address, batch_size):
                end = min(start + batch_size - 1, end_address)
                unit_data = {'Unit ID' : unit_id}
                try:
                    holding_registers = self.client.read_holding_registers(start, end - start + 1, unit=unit_id)
                    if not holding_registers.isError():
                        unit_data['Holding Registers'] = [self.transform_value(val, 'temperature') for val in holding_registers.registers]
                
                except (ModbusIOException, ConnectionException) as ex:
                    logging.error(f"Communication error with Unit ID {unit_id} : {ex}")
                    if not self.reconnect():
                        return all_data
                    if len(all_data) >= 1000:
                        self.save_to_excel(all_data)
                        all_data.clear()