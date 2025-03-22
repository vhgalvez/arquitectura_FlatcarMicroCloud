from diagrams import Node, Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, StatefulSet
from diagrams.generic.network import VPN
from diagrams.aws.general import User

# Clase personalizada para evitar errores de tamaño
class CustomNode(Node):
    _attr = {
        "fontsize": "10",
        "width": "2.5",
        "height": "1",
        "fixedsize": "false"
    }

# SVG para mejor compatibilidad
with Diagram("FlatcarMicroCloud - Arquitectura de Infraestructura", 
             show=False, 
             direction="TB", 
             outformat="svg"):
    
    # Acceso externo
    users = User("Usuarios Públicos")
    vpn_gateway = VPN("WireGuard VPN\n10.17.0.1")
    users >> Edge(label="VPN Segura") >> vpn_gateway

    # Red local
    with Cluster("Red Local Segura (192.168.0.0/24)"):
        pfsense = CustomNode("pfSense\n192.168.0.200")
        vpn_gateway >> pfsense

        # Balanceadores
        with Cluster("Ingress Load Balancers"):
            lb1 = CustomNode("Traefik LB1\n10.17.3.12")
            lb2 = CustomNode("Traefik LB2\n10.17.3.13")

        with Cluster("HAProxy + Keepalived"):
            haproxy = CustomNode("VIP 10.17.5.10\nAlta Disponibilidad")

        pfsense >> [lb1, lb2] >> haproxy

        # Plano de control de Kubernetes
        with Cluster("Kubernetes - Control Plane"):
            master1 = StatefulSet("Master 1\n10.17.4.21")
            master2 = StatefulSet("Master 2\n10.17.4.22")
            master3 = StatefulSet("Master 3\n10.17.4.23")

        haproxy >> [master1, master2, master3]

        # Nodos Workers
        with Cluster("Kubernetes - Workers"):
            worker1 = Pod("Worker 1\n10.17.4.24")
            worker2 = Pod("Worker 2\n10.17.4.25")
            worker3 = Pod("Worker 3\n10.17.4.26")
            storage = Pod("Storage\n10.17.4.27")

        lb1 >> [worker1, worker2, worker3, storage]
        lb2 >> [worker1, worker2, worker3, storage]

        # Infraestructura de soporte
        with Cluster("Infraestructura de Soporte"):
            freeipa = CustomNode("FreeIPA\n10.17.3.11")
            db = CustomNode("PostgreSQL\n10.17.3.14")
            persistent = CustomNode("Almacenamiento\n10.17.4.27")

        lb1 >> [freeipa, db, persistent]
        lb2 >> [freeipa, db, persistent]