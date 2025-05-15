from diagrams import Diagram
from diagrams.onprem.client import Users
from diagrams.onprem.network import Pfsense, Haproxy, Traefik
from diagrams.onprem.container import K3S
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.queue import Rabbitmq
from diagrams.onprem.database import Postgresql
from diagrams.onprem.dns import Coredns
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Gitlab
from diagrams.generic.os import LinuxGeneral
from diagrams.generic.network import VPN
from diagrams.generic.place import Datacenter
from diagrams.onprem.storage import Ceph

with Diagram("Test - Carga Completa de Íconos", show=True, direction="TB"):

    Users("Usuarios")
    VPN("VPN")
    Pfsense("Firewall")
    Datacenter("LAN")
    Traefik("Traefik LB")
    Haproxy("HAProxy")
    K3S("Master Node")
    LinuxGeneral("Worker Node")
    Ceph("Storage Node")
    Coredns("CoreDNS")
    Postgresql("PostgreSQL")
    Prometheus("Prometheus")
    Grafana("Grafana")
    Jenkins("Jenkins CI")
    Rabbitmq("RabbitMQ")
    Gitlab("GitLab")
