from diagrams import Diagram, Cluster, Edge

# OnPrem Components
from diagrams.onprem.client import Users
from diagrams.onprem.network import Pfsense, Haproxy, Traefik
from diagrams.onprem.container import K3S
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.queue import Rabbitmq
from diagrams.onprem.database import Postgresql
from diagrams.onprem.dns import Coredns
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Gitlab
from diagrams.onprem.storage import Ceph

# Generic Components
from diagrams.generic.os import LinuxGeneral
from diagrams.generic.network import VPN
from diagrams.generic.place import Datacenter

with Diagram("FlatcarMicroCloud - Infraestructura Global Optimizada", show=False, direction="TB", outformat="png"):

    # Zona de acceso externo
    usuarios = Users("Usuarios Públicos")
    vpn = VPN("VPN Pública\n10.17.0.1")
    firewall = Pfsense("Firewall NAT\n192.168.0.19")
    lan = Datacenter("Red LAN\n192.168.0.0/24")

    usuarios >> Edge(label="HTTPS + Cloudflare") >> vpn >> firewall >> lan

    with Cluster("Kubernetes Ingress"):
        lb1 = Traefik("LB1\n10.17.3.12\nloadbalancer1")
        lb2 = Traefik("LB2\n10.17.3.13\nloadbalancer2")
        lan >> [lb1, lb2]

    haproxy = Haproxy("HAProxy + Keepalived\nVIP: 10.17.5.10\nAPI LB")
    [lb1, lb2] >> haproxy

    with Cluster("Kubernetes Control Plane"):
        m1 = K3S("master1\n10.17.4.21\netcd + API")
        m2 = K3S("master2\n10.17.4.22\netcd")
        m3 = K3S("master3\n10.17.4.23\netcd")
    haproxy >> [m1, m2, m3]

    with Cluster("Kubernetes Workers + Storage"):
        w1 = LinuxGeneral("worker1\n10.17.4.24\nFlatcar")
        w2 = LinuxGeneral("worker2\n10.17.4.25\nFlatcar")
        w3 = LinuxGeneral("worker3\n10.17.4.26\nFlatcar")
        storage = Ceph("storage1\n10.17.3.27\nLonghorn + NFS")
    haproxy >> [w1, w2, w3, storage]

    with Cluster("Servicios Complementarios"):
        dns = Coredns("CoreDNS\n10.17.3.11")
        db = Postgresql("PostgreSQL\n10.17.3.14")
        prom = Prometheus("Prometheus")
        graf = Grafana("Grafana")
        jenkins = Jenkins("Jenkins CI/CD")
        queue = Rabbitmq("RabbitMQ")
        vcs = Gitlab("GitLab")

    for w in [w1, w2, w3]:
        w >> [dns, db, prom, graf, jenkins, queue, vcs]