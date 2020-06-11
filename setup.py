from setuptools import setup
from setuptools.command.build_py import build_py
import shutil

from codecs import open
import os
import sys

with open(os.path.join('.', 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

name = 'iint-gui'
version = '0'
release = '0.16.4'

TOOL = "iintgui"
QRCDIR = os.path.join(TOOL, "qrc")

class toolBuild(build_py):
    """ ui and qrc builder for python
    """

    @classmethod
    def makeqrc(cls, qfile, path):
        """  creates the python qrc files
        :param qfile: qrc file name
        :param path:  qrc file path
        """
        qrcfile = os.path.join(path, str(qfile) + ".qrc")
        rccfile = os.path.join(path, str(qfile) + ".rcc")

        compiled = os.system("rcc %s -o %s -binary" % (qrcfile, rccfile))
        if compiled == 0:
            print("Built: %s -> %s" % (qrcfile, rccfile))
        else:
            sys.stderr.write("Error: Cannot build  %s\n" % (rccfile))
            sys.stderr.flush()

    def run(self):
        """ runner
        :\brief: It is running during building
        """
        try:
            qfiles = [(qfile[:-4], QRCDIR) for qfile
                      in os.listdir(QRCDIR) if qfile.endswith('.qrc')]
            for qrc in qfiles:
                if not qrc[0] in (".", ".."):
                    self.makeqrc(qrc[0], qrc[1])
        except TypeError as e:
            print(str(e))
            sys.stderr.write("No .qrc files to build\n")
            sys.stderr.flush()

        build_py.run(self)


setup(
    name='iintgui',
    version=release,

    description='iintgui: a gui to use with iint',
    long_description=long_description,

    test_suite="tests",

    url='https://github.com/syncope/iintgui',

    author='Ch.Rosemann',
    author_email='christoph.rosemann@desy.de',

    license='GPLv2',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='photon science data processing analysis gui interactive',

    packages=['iintgui', ],
    package_dir={'iintgui': 'iintgui', },
    include_package_data=True,

    scripts=['iintgui/bin/iint-gui'],
    cmdclass={
        "build_py": toolBuild,},

)
