from typing import List
from dataclasses import dataclass


@dataclass
class Sample:
    """
    Holds info about sample numbers and their values
    """
    number: List[int]
    value:  List[int]

    def __init__(self, number=List[int], value=List[int]):
        self.number = number
        self.value = value


"""
Number of samples type
"""
sample_num_t = int

"""
Timepoint type
"""
timepoint_t = float
