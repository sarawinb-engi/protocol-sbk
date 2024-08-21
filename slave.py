from pymodbus.server.sync import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore.store import ModbusSequentialDataBlock
from pymodbus.transaction import ModbusRtuFramer, ModbusBinaryFramer

def run_server():
    # กำหนดข้อมูลที่หลากหลายใน registers
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0, 1, 0, 1, 1, 0, 1, 0, 1, 0] * 10),
        co=ModbusSequentialDataBlock(0, [1]*100),
        hr=ModbusSequentialDataBlock(0, list(range(1, 101))),  # 100 holding registers
        ir=ModbusSequentialDataBlock(0, list(range(101, 201)))  # 100 input registers
    )

    
    context = ModbusServerContext(slaves=store, single=True)
    
    # กำหนดข้อมูลของอุปกรณ์
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Pymodbus'
    identity.ProductCode = 'PM'
    identity.VendorUrl = 'http://github.com/riptideio/pymodbus/'
    identity.ProductName = 'Pymodbus Server'
    identity.ModelName = 'Pymodbus Server'
    identity.MajorMinorRevision = '1.0'

    # เริ่มต้น TCP server
    StartTcpServer(context, identity=identity, address=("localhost", 5020))

if __name__ == "__main__":
    run_server()
