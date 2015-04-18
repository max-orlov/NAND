__author__ = 'Maxim'
from enum import Enum


class VMSegmentTypes(Enum):
    SP = "SP"                   #==0
    LOCAL = "LCL"                #==1
    ARGUMENT = "ARG"             #==2
    POINTER = "3"
    THIS = "THIS"                 #==3
    THAT = "THAT"                 #==4
    TEMP = 5                 #<=12
    GENERAL_PURPOSE = 13      #<=15
    STATIC = 16               #<=255
    CONSTANT = "constant"


def get_segment_type(seg_name):
    return {
        "static": VMSegmentTypes.STATIC,
        "argument": VMSegmentTypes.ARGUMENT,
        "local": VMSegmentTypes.LOCAL,
        "constant": VMSegmentTypes.CONSTANT,
        "this": VMSegmentTypes.THIS,
        "that": VMSegmentTypes.THAT,
        "pointer": VMSegmentTypes.POINTER,
        "temp": VMSegmentTypes.TEMP
    }[seg_name]




