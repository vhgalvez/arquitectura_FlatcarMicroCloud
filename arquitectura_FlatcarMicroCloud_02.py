from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Users
from diagrams.generic.network import Internet
from diagrams.onprem.network import Haproxy
from diagrams.onprem.container import K3S
from diagrams.onprem.network import Traefik
from diagrams.onprem.dns import Coredns
from diagrams.onprem.database import Postgresql
from diagrams.generic.os import LinuxGeneral
from diagrams.generic.blank import Blank  # para VIPs/elementos lógicos

with Diagram("FlatcarMicroCloud — Vista Lógica", show=False, direction="TB", outformat="png"):

    # Público + CDN/WAF (si usas Cloudflare, representamos como "Internet" genérico)
    users = Users("Usuarios Externos")
    internet = Internet("CDN/WAF (Cloudflare)")

    # Acceso remoto seguro (VPN lógica)
    vpn = Internet("VPN WireGuard (10.17.0.0/24)")

    users >> Edge(label="HTTPS") >> internet >> vpn

    # Firewall del host (nftables) como "Internet" genérico
    fw = Internet("Firewall (nftables)\nHost KVM 192.168.0.40")
    vpn >> fw

    # VIPs (objetos lógicos)
    vip_api = Blank("VIP API: 192.168.0.10:6443")
    vip_web = Blank("VIP Web: 192.168.0.14:80/443")

    fw >> Edge(label="LAN") >> vip_api
    fw >> Edge(label="LAN") >> vip_web

    # L4 Load Balancers (HAProxy + Keepalived)
    with Cluster("L4 Load Balancers (LAN 192.168.0.0/24)"):
        lb1 = Haproxy("LB1\nHAProxy/Keepalived\n192.168.0.11")
        lb2 = Haproxy("LB2\nHAProxy/Keepalived\n192.168.0.12")

    vip_api >> [lb1, lb2]
    vip_web >> [lb1, lb2]

    # Plano de control (K3s masters)
    with Cluster("Masters (10.17.4.0/24)"):
        m1 = K3S("master1\n10.17.4.21")
        m2 = K3S("master2\n10.17.4.22")
        m3 = K3S("master3\n10.17.4.23")

    # Enrutamiento: API 6443 -> masters
    [lb1, lb2] >> Edge(label="6443") >> [m1, m2, m3]

    # Ingress L7 (Traefik) dentro del cluster
    with Cluster("Ingress L7 (en K3s)"):
        traefik = Traefik("Traefik\nService/Ingress\n(NodePort/LB interno)")

    # Enrutamiento: 80/443 -> Traefik (Ingress)
    [lb1, lb2] >> Edge(label="80/443") >> traefik

    # Workers y Storage
    with Cluster("Workers + Storage (10.17.4.0/24)"):
        w1 = LinuxGeneral("worker1\n10.17.4.24")
        w2 = LinuxGeneral("worker2\n10.17.4.25")
        w3 = LinuxGeneral("worker3\n10.17.4.26")
        longhorn = LinuxGeneral("Longhorn (storage1)\n10.17.4.27")

    traefik >> [w1, w2, w3]

    # Servicios base
    with Cluster("Servicios base (Infra)"):
        dns = Coredns("CoreDNS + Chrony\n192.168.0.30")
        pg = Postgresql("PostgreSQL\n10.17.3.14")

    # Dependencias lógicas
    [m1, m2, m3, w1, w2, w3] >> Edge(label="DNS/NTP") >> dns
    [w1, w2, w3] >> Edge(label="DB") >> pg
