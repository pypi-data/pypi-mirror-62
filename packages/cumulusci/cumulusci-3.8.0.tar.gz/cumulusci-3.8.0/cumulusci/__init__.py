import os
import sys

__import__("pkg_resources").declare_namespace("cumulusci")

__version__ = "3.8.0"

__location__ = os.path.dirname(os.path.realpath(__file__))

if sys.version_info < (3, 6):  # pragma: no cover
    raise Exception("CumulusCI requires Python 3.6+.")
