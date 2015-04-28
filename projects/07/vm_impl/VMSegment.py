from enum import Enum


class VMSegmentTypes:
    def __init__(self):
        self._segment_types = dict.fromkeys(["SP", "LCL", "ARG", "THIS", "THAT",

                                             """ Designated memory segments - they point towards the hard coded locations:
                                            this,that - by pointer(location 3,4)
                                            temp - for 'temp' segments(location 5-15)
                                            general purpose - what is this good for?
                                            static - for the static segment (location 16-255)
                                            """
                                             "POINTER", "TEMP", "GENERAL_PURPOSE", "STATIC",

                                             """ Constant is a virtual segment so it does not get a real memory name
                                             or address """
                                             "constant"
        ])

    def bootstrap(self, dic):
        for key, value in dic:
            self._segment_types[key] = value

    def set_value(self, key, value):
        self._segment_types[key] = value

    def get_value(self, key):
        return self._segment_types[key]


class VMSegmentTypes(Enum):
    SP = "SP"  # ==0
    LOCAL = "LCL"  # ==1
    ARGUMENT = "ARG"  # ==2
    THIS = "THIS"  # ==3
    THAT = "THAT"  # ==4

    POINTER = 3  # 3
    TEMP = 5  # 5
    GENERAL_PURPOSE = 13  # 13
    STATIC = 16  # 16


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