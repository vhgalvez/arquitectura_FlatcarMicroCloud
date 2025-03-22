from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.network import Traefik, HAProxy, Pfsense
from diagrams.onprem.security import FreeIPA
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.container import Kubernetes
from diagrams.generic.network import VPN, Users
from diagrams.generic.cloud import CDN

with Diagram("FlatcarMicroCloud - Arquitectura de Infraestructura", show=True, direction="TB"):
    users = Users("Usuarios Públicos")
    cloudflare = CDN("Cloudflare CDN\nWAF + DDoS")
    vps = Server("VPS (IP Pública)\nTúnel WireGuard")
    wireguard = VPN("WireGuard VPN Gateway\n10.17.0.1")

    users >> Edge(label="HTTPS") >> cloudflare >> Edge(label="Proxy + Cache") >> vps >> Edge(label="VPN Segura") >> wireguard

    with Cluster("Red Local Segura (192.168.0.0/24)"):
        pfsense = Pfsense("pfSense\n192.168.0.200")
        wireguard >> pfsense

        with Cluster("Ingress - Balanceo de Carga"):
            lb1 = Traefik("Traefik LB1\n10.17.3.12")
            lb2 = Traefik("Traefik LB2\n10.17.3.13")

        with Cluster("HAProxy + Keepalived"):
            haproxy = HAProxy("VIP: 10.17.5.10\nAlta Disponibilidad")

        pfsense >> [lb1, lb2] >> haproxy

        with Cluster("Kubernetes - Plano de Control"):
            m1 = Kubernetes("Master 1\n10.17.4.21")
            m2 = Kubernetes("Master 2\n10.17.4.22")
            m3 = Kubernetes("Master 3\n10.17.4.23")

        haproxy >> [m1, m2, m3]

        with Cluster("Kubernetes - Nodos Worker"):
            w1 = Kubernetes("Worker 1\n10.17.4.24")
            w2 = Kubernetes("Worker 2\n10.17.4.25")
            w3 = Kubernetes("Worker 3\n10.17.4.26")
            storage = Kubernetes("Storage Node\n10.17.4.27")

        lb1 >> [w1, w2, w3, storage]
        lb2 >> [w1, w2, w3, storage]

        with Cluster("Infraestructura de Soporte"):
            freeipa = FreeIPA("FreeIPA\n10.17.3.11")
            db = PostgreSQL("PostgreSQL\n10.17.3.14")
            persistence = Server("Almacenamiento\n10.17.4.27")

        lb1 >> [freeipa, db, persistence]
        lb2 >> [freeipa, db, persistence]