from pymodbus.client.sync import ModbusTcpClient

def display_modbus_response(response):
    if response.isError():
        # แสดง error code ถ้ามีข้อผิดพลาด
        print(f"Error: {response}")
    else:
        # แสดงโครงสร้างข้อมูลของ Modbus response
        print(f"Function Code: {response.function_code}")
        print(f"Address: {response.address if hasattr(response, 'address') else 'N/A'}")
        print(f"Register Data: {response.registers if hasattr(response, 'registers') else 'N/A'}")
        print(f"Byte Count: {response.byte_count if hasattr(response, 'byte_count') else 'N/A'}")
        print(f"Data: {response.encode()}")  # แสดงข้อมูลในรูปแบบ byte

def run_client():
    client = ModbusTcpClient('localhost', port=5020)
    client.connect()

    # อ่าน holding registers
    holding_registers = client.read_holding_registers(0, 10)
    print("Holding Registers Response:")
    display_modbus_response(holding_registers)

    # อ่าน input registers
    input_registers = client.read_input_registers(0, 10)
    print("\nInput Registers Response:")
    display_modbus_response(input_registers)

    # เขียนค่าไปยัง holding registers
    write_response = client.write_registers(0, [111, 222, 333, 444, 555, 666, 777, 888, 999, 1010])
    print("\nWrite Holding Registers Response:")
    display_modbus_response(write_response)

    client.close()

if __name__ == "__main__":
    run_client()
