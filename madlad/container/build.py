import yaml
import warnings
import subprocess

from madlad.container.commands import lhapdf_build, fastjet_build, pythia8_build, delphes_build, mg5_build
from madlad.container.download import get_model, get_pdfset


def DockerBuild(config: str):
    with open(config) as f:
        settings = yaml.load(f, Loader=yaml.SafeLoader)

    init = """FROM tzuhanchang/madlad:madlad-base

    # metainformation
    LABEL org.opencontainers.image.base.name="docker.io/library/tzuhanchang/madlad:madlad-base"

    """

    with open("Dockerfile", "w") as text_file:
        text_file.write(init)
        try:
            text_file.write(lhapdf_build(version=settings['build']['lhapdf'])[0])
        except KeyError:
            warnings.warn("LHAPDF preference not found, use `LHAPDF=6.5.3`.")
            text_file.write(lhapdf_build(version="6.5.3")[0])

        try:
            text_file.write(pythia8_build(version=settings['build']['pythia'])[0])
        except KeyError:
            warnings.warn("PYTHIA8 preference not found, use `PYTHIA8=8.301`.")
            text_file.write(pythia8_build(version="8.301")[0])

        try:
            text_file.write(fastjet_build(version=settings['build']['fastjet'])[0])
        except KeyError:
            warnings.warn("FastJet preference not found, use `FastJet=3.4.1`.")
            text_file.write(fastjet_build(version="3.4.1")[0])

        try:
            text_file.write(delphes_build(version=settings['build']['delphes'])[0])
        except KeyError:
            warnings.warn("Delphes preference not found, use `Delphes=3.5.0`.")
            text_file.write(delphes_build(version="3.5.0")[0])

        try:
            if "." in settings['build']['mg5']:
                text_file.write(mg5_build(version=settings['build']['mg5'])[0])
            else:
                print(f"Using external custom MadGraph5 installation provided in {settings['build']['mg5']}")
                text_file.write(mg5_build(external=settings['build']['mg5'])[0])
        except KeyError:
            warnings.warn("MadGraph5 preference not found, use `MadGraph5=3.5.3`.")
            text_file.write(mg5_build(version="3.5.3")[0])

        try:
            text_file.write(get_pdfset(settings['extra']['pdfs'])),
        except KeyError:
            warnings.warn("No optional pdf sets provided, none will be downloaded.")
            pass

        try:
            text_file.write(get_model(settings['extra']['models']))
        except KeyError:
            warnings.warn("No optional models provided, none will be downloaded.")
            pass

    try:
        image_name = settings['image']['name']
    except KeyError:
        warnings.warn("Use Docker image name `madlad-custom`.")
        image_name = "madlad-custom"

    building = subprocess.Popen(["docker", "build", "-t", image_name, "."])
    building.wait()