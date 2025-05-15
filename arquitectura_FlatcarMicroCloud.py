from diagrams import Diagram, Cluster, Edge
from diagrams.generic.network import VPN
from diagrams.generic.place import Datacenter
from diagrams.onprem.client import Users
from diagrams.onprem.network import Pfsense, Haproxy, Traefik
from diagrams.onprem.container import K3S
from diagrams.onprem.storage import Ceph
from diagrams.generic.os import LinuxGeneral
from diagrams.onprem.dns import Coredns
from diagrams.onprem.database import Postgresql
from diagrams.generic.blank import Blank  # Para título visual y nodo lógico

with Diagram("", show=False, direction="TB", outformat="png"):

    # Título visual como nodo superior
    titulo = Blank("**FlatcarMicroCloud - Infraestructura Global**")

    # Entrada pública
    usuarios = Users("Usuarios Públicos")
    cloudflare = VPN("Cloudflare\nCDN + WAF")
    vpn = VPN("WireGuard\n10.17.0.1")
    firewall = Pfsense("Firewall + NAT\n192.168.0.19")

    titulo >> usuarios >> Edge(label="HTTPS + Seguridad + Caché") >> cloudflare >> vpn >> firewall

    # Ingress
    with Cluster("Ingress"):
        lb1 = Traefik("LB1\n10.17.3.12")
        lb2 = Traefik("LB2\n10.17.3.13")
    firewall >> [lb1, lb2]

    haproxy = Haproxy("HAProxy\nVIP: 10.17.5.10\nHA: 10.17.5.20")
    [lb1, lb2] >> haproxy

    # Masters
    with Cluster("Masters"):
        m1 = K3S("master1\n10.17.4.21")
        m2 = K3S("master2\n10.17.4.22")
        m3 = K3S("master3\n10.17.4.23")
    haproxy >> [m1, m2, m3]

    # Workers + Storage
    with Cluster("Workers + Storage"):
        w1 = LinuxGeneral("worker1\n10.17.4.24")
        w2 = LinuxGeneral("worker2\n10.17.4.25")
        w3 = LinuxGeneral("worker3\n10.17.4.26")
        s1 = Ceph("storage1\n10.17.3.27")
    haproxy >> [w1, w2, w3, s1]

    # Nodo lógico invisible para simplificar conexiones
    infra = Blank("")

    [m1, m2, m3, w1, w2, w3] >> infra

    # Servicios centrales
    dns = Coredns("CoreDNS\n10.17.3.11")
    db = Postgresql("PostgreSQL\n10.17.3.14")
    infra >> dns
    infra >> db