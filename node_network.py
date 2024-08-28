import matplotlib.pyplot as plt
import networkx as nx

def draw_modbus_communication():
    # สร้างกราฟด้วย NetworkX
    G = nx.DiGraph()

    # เพิ่มโหนด (Nodes)
    G.add_node("Client", pos=(0, 1))
    G.add_node("Server", pos=(2, 1))

    # เพิ่มขอบ (Edges) ซึ่งแทนการส่งคำสั่งและการตอบกลับ
    G.add_edge("Client", "Server", label="Request: Read Holding Registers")
    G.add_edge("Server", "Client", label="Response: [111, 222, 333, ...]")

    G.add_edge("Client", "Server", label="Request: Write Holding Registers")
    G.add_edge("Server", "Client", label="Response: Write Success")

    # ดึงตำแหน่งของโหนดเพื่อใช้ในการวาด
    pos = nx.get_node_attributes(G, 'pos')

    # วาดโหนดและขอบในกราฟ
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=12, font_weight="bold", arrows=True)

    # เพิ่มป้ายกำกับบนขอบ
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red', font_size=10)

    plt.title("Modbus Communication")
    plt.show()

if __name__ == "__main__":
    draw_modbus_communication()
