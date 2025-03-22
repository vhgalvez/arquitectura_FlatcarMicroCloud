from diagrams import Node, Diagram, Cluster, Edge
from diagrams.generic.network import VPN
from diagrams.aws.general import User

class CustomNode(Node):
    _attr = {
        "fontsize": "8",
        "width": "4.5",
        "height": "1.5",    
        "fixedsize": "false"
    }


with Diagram("Etapa 2 - Acceso Publico Seguro", filename="etapa2_acceso_publico", show=False, direction="TB", outformat="png"):
    users = User("Usuarios Públicos")
    vpn = VPN("WireGuard VPN\n10.17.0.1")
    users >> Edge(label="VPN Segura") >> vpn

    pfsense = CustomNode("pfSense\n192.168.0.200")
    vpn >> pfsense