__author__ = 'Maxim'
from enum import Enum


class VMSegmentTypes(Enum):
    STATIC = "static"
    ARGUMENT = "argument"
    LOCAL = "local"
    CONSTANT = "constant"
    THIS = "this"
    THAT = "that"
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


class VMSegment:

    def __init__(self):
        self._segments = {
            VMSegmentTypes.STATIC: {},
            VMSegmentTypes.ARGUMENT: {},
            VMSegmentTypes.LOCAL: {},
            VMSegmentTypes.CONSTANT: '',
            VMSegmentTypes.THIS: {},
            VMSegmentTypes.THAT: {},
            VMSegmentTypes.POINTER: {}
        }

    def get_segment(self, seg_name):
        return self._segments[get_segment_type(seg_name)]

    def get_value(self, segment, index):
        if get_segment_type(segment) is VMSegmentTypes.CONSTANT:
            return self._segments[VMSegmentTypes.CONSTANT]
        else:
            return self._segments[get_segment_type(segment)][index]


    def set_value(self, segment, index):
        if get_segment_type(segment) is VMSegmentTypes.CONSTANT:
            self._segments[VMSegmentTypes.CONSTANT] = "@{}".format(index)
        else:
            self._segments[get_segment_type(segment)][index] = "@{}_{}".format(segment, index)



