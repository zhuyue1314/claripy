import logging
l = logging.getLogger("claripy.ops")

#
# AST creation
#

def AbstractLocation(*args, **kwargs): #pylint:disable=no-self-use
    aloc = vsa.AbstractLocation(*args, **kwargs)
    return aloc

#
# Some operations
#


#
# sigh
#

#pylint:disable=wildcard-import,unused-wildcard-import
from .ast_base import *
from .ast.bv import *
from .ast.fp import *
from .ast.bool import *
from . import vsa

BVV = BitVecVal
BV = BitVec
VS = ValueSet
SI = StridedInterval
TSI = TopStridedInterval
