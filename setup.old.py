try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import os
from setuptools import find_packages

packages=find_packages()

VERSION = '0.0.4.dev'
config = {
    'author' : "Malte Kuhlmann, Eric Lacosse, Johannes Stelzer",
    'name' : 'viff',
    'maintainer' : '',
    'maintainer_email' : '',
    'license' : 'MIT',
    'description' : 'A visualization tool for 3D MRI slices and fMRI applications',
    'long_description' : '',
    'version' : VERSION,
    'url' : '',
    'download_url' : '',
    'keywords' : 'visualization, neuroscience, MRI, fMRI',
    'packages' : packages, 
    'scripts' : ['viff/viff.py'],
    'zip_safe' : False,
    
    'classifiers' : [
        "Development Status :: 1 - Beta",
        "Topic :: Scientific Software",
        "License :: OSI Approved :: MIT License",
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: OS Independent',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
    ],
    'install_requires' : ['nose', 'nibabel', 'numpy', 'scipy', 'matplotlib', 'PyQt5'],
}



def checkDependencies():

    # Just make sure dependencies exist, I haven't rigorously
    # tested what the minimal versions that will work are
    needed_deps = ['IPython', 'nibabel', 'numpy', 'scipy', 'matplotlib', 'PyQt5']
    missing_deps = []
    for dep in needed_deps:
        try:
            __import__(dep)
        except ImportError:
            missing_deps.append(dep)
    if missing_deps:
        missing = (", ".join(missing_deps))
        raise ImportError("Missing dependencies: %s" % missing)

if __name__ == "__main__":

    if os.path.exists('MANIFEST'):
        os.remove('MANIFEST')

    import sys
    if not (len(sys.argv) >= 2 and ('--help' in sys.argv[1:] or
            sys.argv[1] in ('--help-commands',
                            '--version',
                            'egg_info',
                            'clean'))):
        checkDependencies()

    setup(**config)



