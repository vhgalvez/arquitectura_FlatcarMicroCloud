from diagrams import Cluster, Diagram, Edge, Node
from diagrams.k8s.compute import Pod, StatefulSet

with Diagram("FlatcarMicroCloud - Arquitectura de Infraestructura", 
             show=False, 
             direction="TB", 
             outformat="svg"):

    # Acceso externo
    user = Node("👥 Usuarios Públicos")
    cloudflare = Node("🌐 Cloudflare CDN\nProxy + WAF + Anti-DDoS")
    vpn = Node("VPS Público\nWireGuard Gateway\n10.17.0.1")
    fisico = Node("Servidor Físico\nWireGuard + NAT + nftables\n192.168.0.19")

    user >> Edge(label="HTTPS + Seguridad + Caché") >> cloudflare
    cloudflare >> vpn >> fisico

    with Cluster("Ingress Kubernetes"):
        lb1 = Node("Load Balancer 1 (Traefik)\n10.17.3.12\nloadbalancer1.cefaslocalserver.com")
        lb2 = Node("Load Balancer 2 (Traefik)\n10.17.3.13\nloadbalancer2.cefaslocalserver.com")

    fisico >> [lb1, lb2]

    haproxy = Node("HAProxy + Keepalived\nVIP: 10.17.5.10\nHA: 10.17.5.20\nk8s-api-lb.cefaslocalserver.com")
    [lb1, lb2] >> haproxy

    with Cluster("Kubernetes Control Plane"):
        master1 = StatefulSet("master1.cefaslocalserver.com\n10.17.4.21\nFlatcar / etcd + API")
        master2 = StatefulSet("master2.cefaslocalserver.com\n10.17.4.22\nFlatcar / etcd")
        master3 = StatefulSet("master3.cefaslocalserver.com\n10.17.4.23\nFlatcar / etcd")

    haproxy >> [master1, master2, master3]

    with Cluster("Workers + Almacenamiento"):
        worker1 = Pod("worker1.cefaslocalserver.com\n10.17.4.24\nFlatcar / Longhorn")
        worker2 = Pod("worker2.cefaslocalserver.com\n10.17.4.25\nFlatcar / Longhorn")
        worker3 = Pod("worker3.cefaslocalserver.com\n10.17.4.26\nFlatcar / Longhorn")
        storage = Pod("storage1.cefaslocalserver.com\n10.17.3.27\nAlmaLinux / 🐂 Longhorn + 📁 NFS")

    haproxy >> [worker1, worker2, worker3, storage]

    with Cluster("🧠 Servicios Complementarios"):
        dns = Node("CoreDNS\n10.17.3.11\ninfra-cluster.cefaslocalserver.com\nDNS interno + NTP")
        db = Node("PostgreSQL\n10.17.3.14\npostgresql1.cefaslocalserver.com\nDB centralizada")

    for w in [worker1, worker2, worker3]:
        w >> dns
        w >> db