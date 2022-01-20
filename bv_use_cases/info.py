# -*- coding: utf-8 -*-

version_major = 0
version_minor = 0
version_micro = 1
version_extra = ''

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
__version__ = "%s.%s.%s%s" % (version_major,
                              version_minor,
                              version_micro,
                              version_extra)
CLASSIFIERS = [
    "Programming Language :: Python",
    "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    "Operating System :: OS Independent"]


description = "Use cases for future BrainVISA API"

# versions for dependencies
SPHINX_MIN_VERSION = '1.0'

# Main setup parameters
NAME = 'bv_use_cases'
PROJECT = 'bv_use_cases'
ORGANISATION = "brainvisa"
MAINTAINER = "nobody"
MAINTAINER_EMAIL = ""
DESCRIPTION = description
URL = "https://github.com/brainvisa/use-cases"
DOWNLOAD_URL = "https://github.com/brainvisa/use-cases"
LICENSE = "CeCILL-B"
AUTHOR = ""
AUTHOR_EMAIL = ''
PLATFORMS = "OS Independent"
PROVIDES = ["bv_use_cases"]
REQUIRES = ['capsul', 'soma-base', 'soma-workflow']
EXTRA_REQUIRES = {
    "doc": ["sphinx>=" + SPHINX_MIN_VERSION]}

brainvisa_build_model = 'pure_python'

