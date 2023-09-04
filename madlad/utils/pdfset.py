import os
import subprocess
from madlad.utils import is_running_in_docker_container


def get_pdfset(pdf_id: int, pdfsets_dict: str = "/usr/local/share/LHAPDF"):
    if is_running_in_docker_container():
        pass
    else:
        raise ValueError("`get_pdfset` is not designed to run outside a container!")

    pdf_name = ""
    with open(pdfsets_dict+"/pdfsets.index", "r") as f:
        lines=f.readlines()
        for line in lines:
            info = line.split(' ')
            if info[0] == str(pdf_id):
                pdf_name = info[1]
            else:
                continue

    if os.path.exists(pdfsets_dict+"/{}".format(pdf_name)) != True:
        download = subprocess.Popen(["sudo","wget","-P",pdfsets_dict+"/","http://lhapdfsets.web.cern.ch/lhapdfsets/current/{}.tar.gz".format(pdf_name)])
        download.wait()
        unzip    = subprocess.Popen(["sudo","tar","-zxf",pdfsets_dict+"/{}.tar.gz".format(pdf_name),"-C",pdfsets_dict+"/"])
        unzip.wait()