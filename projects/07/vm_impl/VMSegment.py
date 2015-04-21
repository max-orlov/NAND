__author__ = 'Maxim'
from enum import Enum


class VMSegmentTypes(Enum):
    SP = "SP"  # ==0
    LOCAL = "LCL"  # ==1
    ARGUMENT = "ARG"  # ==2
    THIS = "THIS"  # ==3
    THAT = "THAT"  # ==4

    """ Designated memory segments - they point towards the hard coded locations:
        this,that - by pointer(location 3,4)
        temp - for 'temp' segments(location 5-15)
        general purpose - what is this good for?
        static - for the static segment (location 16-255)
    """
    POINTER = 3
    TEMP = 5
    GENERAL_PURPOSE = 13
    STATIC = 16

    """ Constant is a virtual segment so it does not get a real memory name or address """
    CONSTANT = "constant"


c_segment_dictionary = {
    "static": VMSegmentTypes.STATIC,
    "argument": VMSegmentTypes.ARGUMENT,
    "local": VMSegmentTypes.LOCAL,
    "constant": VMSegmentTypes.CONSTANT,
    "this": VMSegmentTypes.THIS,
    "that": VMSegmentTypes.THAT,
    "pointer": VMSegmentTypes.POINTER,
    "temp": VMSegmentTypes.TEMP
}




