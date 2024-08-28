import logging
from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException, ConnectionException

# ตั้งค่าการบันทึก Log
logging.basicConfig(filename='modbus_client.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def display_modbus_response(response):
    if response.isError():
        logging.error(f"Error: {response}")
        print(f"Error: {response}")
    else:
        logging.info(f"Function Code: {response.function_code}")
        logging.info(f"Address: {response.address if hasattr(response, 'address') else 'N/A'}")
        logging.info(f"Register Data: {response.registers if hasattr(response, 'registers') else 'N/A'}")
        logging.info(f"Byte Count: {response.byte_count if hasattr(response, 'byte_count') else 'N/A'}")
        logging.info(f"Data: {response.encode()}")
        print(f"Function Code: {response.function_code}")
        print(f"Address: {response.address if hasattr(response, 'address') else 'N/A'}")
        print(f"Register Data: {response.registers if hasattr(response, 'registers') else 'N/A'}")
        print(f"Byte Count: {response.byte_count if hasattr(response, 'byte_count') else 'N/A'}")
        print(f"Data: {response.encode()}")  # แสดงข้อมูลในรูปแบบ byte

def read_holding_registers(client, start_address=0, count=10):
    try:
        holding_registers = client.read_holding_registers(start_address, count)
        print("Holding Registers Response:")
        display_modbus_response(holding_registers)
    except ModbusIOException as e:
        logging.error(f"Failed to read holding registers: {e}")
        print(f"Failed to read holding registers: {e}")

def read_input_registers(client, start_address=0, count=10):
    try:
        input_registers = client.read_input_registers(start_address, count)
        print("\nInput Registers Response:")
        display_modbus_response(input_registers)
    except ModbusIOException as e:
        logging.error(f"Failed to read input registers: {e}")
        print(f"Failed to read input registers: {e}")

def write_holding_registers(client, start_address=0, values=None):
    if values is None:
        values = [111, 222, 333, 444, 555, 666, 777, 888, 999, 1010]
    try:
        write_response = client.write_registers(start_address, values)
        print("\nWrite Holding Registers Response:")
        display_modbus_response(write_response)
    except ModbusIOException as e:
        logging.error(f"Failed to write holding registers: {e}")
        print(f"Failed to write holding registers: {e}")

def read_coils(client, start_address=0, count=10):
    try:
        coils = client.read_coils(start_address, count)
        print("\nCoils Response:")
        display_modbus_response(coils)
    except ModbusIOException as e:
        logging.error(f"Failed to read coils: {e}")
        print(f"Failed to read coils: {e}")

def write_single_coil(client, address, value):
    try:
        response = client.write_coil(address, value)
        print(f"\nWrite Coil at {address} Response:")
        display_modbus_response(response)
    except ModbusIOException as e:
        logging.error(f"Failed to write coil at {address}: {e}")
        print(f"Failed to write coil at {address}: {e}")

def run_client(host='localhost', port=5020, start_address=0, count=10):
    client = ModbusTcpClient(host, port)
    
    try:
        if not client.connect():
            logging.error(f"Failed to connect to Modbus server at {host}:{port}")
            print(f"Failed to connect to Modbus server at {host}:{port}")
            return

        # อ่าน holding registers
        read_holding_registers(client, start_address, count)

        # อ่าน input registers
        read_input_registers(client, start_address, count)

        # เขียนค่าไปยัง holding registers
        write_holding_registers(client, start_address, [i for i in range(111, 111 + count)])

        # อ่านและเขียน Coils
        read_coils(client, start_address, count)
        write_single_coil(client, start_address, True)

    except (ModbusIOException, ConnectionException) as e:
        logging.error(f"Modbus communication error: {e}")
        print(f"Modbus communication error: {e}")
    
    finally:
        client.close()

if __name__ == "__main__":
    run_client()
