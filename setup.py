#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.command.install import install as DistutilsInstall
import os
import subprocess

def compile_seqtk():
    """Compiling the seqtk toolkit"""
    old_wd = os.getcwd()
    new_wd = os.path.join(old_wd,"mapdamage","seqtk")
    os.chdir(new_wd)
    if not os.path.isfile("seqtk.c"):
        raise SystemExit("Cannot find seqtk.c")
    if (os.path.isfile("seqtk")):
        os.system("rm seqtk")
    xs = os.system("make -f Makefile")
    os.chdir(old_wd)
    if (xs != 0):
        raise SystemExit("Cannot compile seqtk")


def setup_version():
    if not os.path.exists(".git"):
        # Release version, no .git folder
        return

    try:
        version = subprocess.check_output(("git", "describe", "--always", "--tags", "--dirty"))
        with open(os.path.join("mapdamage", "_version.py"), "w") as handle:
            handle.write("#!/usr/bin/env python\n")
            handle.write("__version__ = %r\n" % (version.strip(),))
    except (subprocess.CalledProcessError, OSError), error:
        raise SystemExit("Could not determine mapDamage version: %s" % (error,))


class compileInstall(DistutilsInstall):
    # extension of the class to account for an extra compiling step
    def run(self):
        self.record=""
        setup_version()
        compile_seqtk()
        DistutilsInstall.run(self)
        # fixing the permission problem of seqtk
        files = self.get_outputs()
        for fi in files:
            if fi.endswith("seqtk/seqtk"):
                os.chmod(fi,0755)





setup(
    cmdclass={'install': compileInstall},
    name='mapdamage',
    version='2.0.8',
    author='Aurélien Ginolhac, Mikkel Schubert, Hákon Jónsson',
    author_email='MSchubert@snm.ku.dk, jonsson.hakon@gmail.com',
    packages=['mapdamage'],
    package_data={'mapdamage': ['Rscripts/*.R','Rscripts/stats/*.R','seqtk/seqtk']},
    scripts=['bin/mapDamage'],
    url='https://github.com/ginolhac/mapDamage',
    license='LICENSE.txt',
    description='mapDamage tracks and quantify DNA damage pattern among ancient DNA sequencing reads generated by Next-Generation Sequencing platforms',
    long_description=open('README.md').read()
)
