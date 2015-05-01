from enum import Enum


class VMSegmentTypes:
    def __init__(self):
        self._segment_types = dict.fromkeys([
            """SP:0, LCL:1, ARG:2, THIS:3, THAT:4"""
            "SP", "LCL", "ARG", "THIS", "THAT",

            """ Designated memory segments - they point towards the hard coded locations:
                                            this,that - by pointer(location 3,4). the pointer itself is in
                                            temp - for 'temp' segments(location 5-12)
                                            general purpose (R13,R14,R15)
                                            static - for the static segment (location 16-255)
                                            """
            "POINTER", "TEMP", "R13", "R14", "R15", "STATIC",

            """ Constant is a virtual segment so it does not get a real memory name
                                             or address """
            "CONSTANT"
        ])

    def bootstrap(self, dic):
        for key, value in dic:
            self._segment_types[key] = value

    def set_value(self, key, value):
        self._segment_types[key] = value

    def get_value(self, key):
        return self._segment_types[{"local": "LCL",
                                    "argument": "ARG",
                                    "this": "THIS",
                                    "that": "THAT",
                                    "pointer": "POINTER",
                                    "temp": "TEMP",
                                    "GP": "GENERAL_PURPOSE",
                                    "static": "STATIC",
                                    "constant": "CONSTANT"
        }[key]]

    def get_address(self, key):
        return self._segment_types[key]