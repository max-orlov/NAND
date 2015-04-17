__author__ = 'Maxim'
from enum import Enum


class VMSegmentTypes(Enum):
    STATIC = "16"
    ARGUMENT = "2"
    LOCAL = "1"
    THIS = "3"
    THAT = "4"
    CONSTANT = "constant"
    POINTER = "pointer"


def get_segment_type(seg_name):
    return {
        "static": VMSegmentTypes.STATIC,
        "argument": VMSegmentTypes.ARGUMENT,
        "local": VMSegmentTypes.LOCAL,
        "constant": VMSegmentTypes.CONSTANT,
        "this": VMSegmentTypes.THIS,
        "that": VMSegmentTypes.THAT,
        "pointer": VMSegmentTypes.POINTER
    }[seg_name]




