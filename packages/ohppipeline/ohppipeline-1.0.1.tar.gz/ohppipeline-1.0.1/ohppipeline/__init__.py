# -*- coding: utf8 -*-  

""" package in order to reduce and analyze fits 

:author: Clement Hottier
"""


from .utils import makemasterbias, makemasterflat, processimages, crosscorrelalign


__author__ = "Clement Hottier, Noel Robichon"
__version__ = "1.0.1"
__all__ = [
        "makemasterbias",
        "makemasterflat",
        "processimages",
        "crosscorrelalign",
]
