from diagrams import Diagram
from diagrams.onprem.ci import Jenkins

with Diagram("Test Jenkins", show=True):
    Jenkins("Jenkins CI")
