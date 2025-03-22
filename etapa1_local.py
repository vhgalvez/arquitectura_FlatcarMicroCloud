from diagrams import Node, Diagram, Cluster
from diagrams.k8s.compute import Pod, StatefulSet

class CustomNode(Node):
    _attr = {
        "fontsize": "8",
        "width": "4.5",         # Antes: 3.0
        "height": "1.5",        # Antes: 1.2
        "fixedsize": "false"
    }

with Diagram("Etapa 1 - Infraestructura Local Privada", show=False, direction="TB", outformat="png"):

    with Cluster("Red Local Segura (192.168.0.0/24)"):
        pfsense = CustomNode("pfSense\n192.168.0.200")

        with Cluster("Load Balancers - Ingress"):
            lb1 = CustomNode("Traefik LB1\n10.17.3.12")
            lb2 = CustomNode("Traefik LB2\n10.17.3.13")

        with Cluster("Alta Disponibilidad"):
            haproxy = CustomNode("VIP 10.17.5.10\nHAProxy + Keepalived")

        pfsense >> [lb1, lb2] >> haproxy

        with Cluster("Kubernetes - Plano de Control"):
            master1 = StatefulSet("Master 1\n10.17.4.21")
            master2 = StatefulSet("Master 2\n10.17.4.22")
            master3 = StatefulSet("Master 3\n10.17.4.23")

        haproxy >> [master1, master2, master3]

        with Cluster("Kubernetes - Nodos Trabajadores"):
            worker1 = Pod("Worker 1\n10.17.4.24")
            worker2 = Pod("Worker 2\n10.17.4.25")
            worker3 = Pod("Worker 3\n10.17.4.26")
            storage = Pod("Storage\n10.17.4.27")

        lb1 >> [worker1, worker2, worker3, storage]
        lb2 >> [worker1, worker2, worker3, storage]

        with Cluster("Servicios de Soporte"):
            freeipa = CustomNode("FreeIPA\n10.17.3.11")
            db = CustomNode("PostgreSQL\n10.17.3.14")
            persistent = CustomNode("Almacenamiento\n10.17.4.27")

        lb1 >> [freeipa, db, persistent]
        lb2 >> [freeipa, db, persistent]