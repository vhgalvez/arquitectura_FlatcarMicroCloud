from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import Users
from diagrams.generic.network import Internet
from diagrams.onprem.network import Haproxy, Traefik
from diagrams.onprem.container import K3S
from diagrams.onprem.dns import Coredns
from diagrams.onprem.database import Postgresql
from diagrams.generic.os import LinuxGeneral
from diagrams.generic.blank import Blank  # VIPs / elementos lógicos

with Diagram("FlatcarMicroCloud — Vista Lógica (K3s HA + HAProxy/Keepalived)", show=False, direction="TB", outformat="png"):

    # Usuarios y borde público (CDN/WAF)
    users = Users("Usuarios Externos")
    cdn = Internet("CDN/WAF (Cloudflare)")

    # Router físico con port-forward público
    router = Internet("Router físico\nPort-Forward:\n8080→80 · 2052→443")

    # Acceso remoto seguro (VPN) y host hypervisor + firewall
    vpn = Internet("VPN WireGuard\n10.17.0.0/24")
    host_fw = LinuxGeneral("Host Hypervisor + Firewall (nftables)\nKVM/libvirt · 192.168.0.40")

    # Flujo público Web
    users >> Edge(label="HTTPS") >> cdn >> router

    # Acceso de operadores por VPN hasta el host
    users >> Edge(label="WireGuard") >> vpn >> host_fw

    # ===================== LAN 192.168.0.0/24 =====================
    with Cluster("LAN 192.168.0.0/24"):
        # VIPs (objetos lógicos en LAN)
        vip_api = Blank("VIP API\n192.168.0.32:6443")
        vip_web = Blank("VIP Web\n192.168.0.33:80/443")

        # L4 Load Balancers (HAProxy + Keepalived) en LAN
        with Cluster("L4 Load Balancers"):
            lb1 = Haproxy("LB1 · ACTIVE\nHAProxy/Keepalived\n192.168.0.30")
            lb2 = Haproxy("LB2 · BACKUP\nHAProxy/Keepalived\n192.168.0.31")

        # Router entrega tráfico público a la VIP Web (vía LBs)
        router >> Edge(label="PF 8080/2052") >> vip_web

        # VIPs anuncian hacia el par de LBs
        vip_api >> [lb1, lb2]
        vip_web >> [lb1, lb2]

        # El host enruta LAN <-> redes internas
        host_fw >> Edge(label="LAN ↔ rutas internas") >> [vip_api, vip_web]

    # ===================== K3s 10.17.4.0/24 =====================
    with Cluster("K3s · Red 10.17.4.0/24"):
        # Plano de control (masters K3s)
        with Cluster("Masters"):
            m1 = K3S("master1 · 2vCPU/2GB/50GB\n10.17.4.21")
            m2 = K3S("master2 · 2vCPU/2GB/50GB\n10.17.4.22")
            m3 = K3S("master3 · 2vCPU/2GB/50GB\n10.17.4.23")

        # Ingress L7 Traefik dentro del clúster (expuesto por NodePort/HostPort en workers)
        with Cluster("Ingress L7"):
            traefik = Traefik("Traefik\nService/Ingress\n(NodePort/HostPort en workers)")

        # Workers + Storage (incluye Longhorn/NFS)
        with Cluster("Workers + Storage"):
            w1 = LinuxGeneral("worker1 · 3vCPU/8GB/20GB +40GB\n10.17.4.24")
            w2 = LinuxGeneral("worker2 · 3vCPU/8GB/20GB +40GB\n10.17.4.25")
            w3 = LinuxGeneral("worker3 · 3vCPU/8GB/20GB +40GB\n10.17.4.26")
            storage = LinuxGeneral("storage1 · 2vCPU/4GB/10GB +80GB\nLonghorn + NFS\n10.17.4.27")

        # Tráfico L4 desde LBs a K3s
        [lb1, lb2] >> Edge(label="6443/TCP") >> [m1, m2, m3]        # API Server
        [lb1, lb2] >> Edge(label="80/443") >> traefik               # HTTP(S) hacia Ingress

        # Ingress enruta a workloads en workers
        traefik >> [w1, w2, w3]

    # ===================== Infra 10.17.3.0/24 =====================
    with Cluster("Infra · Red 10.17.3.0/24"):
        dns_ntp = Coredns("CoreDNS + Chrony\n10.17.3.11")
        pg = Postgresql("PostgreSQL\n10.17.3.14")

    # Dependencias lógicas: DNS/NTP para nodos y DB para workloads
    [m1, m2, m3, w1, w2, w3, storage] >> Edge(label="DNS/NTP") >> dns_ntp
    [w1, w2, w3] >> Edge(label="DB (5432)") >> pg

    # Nota de enrutamiento interno del host hacia subredes K3s/Infra
    host_fw >> Edge(label="Rutas a 10.17.3.0/24 y 10.17.4.0/24") >> [dns_ntp, pg, m1, m2, m3, w1, w2, w3, storage]
