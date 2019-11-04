import wave
import struct
import scipy.signal
import statistics
from typing import List
from multipledispatch import dispatch

from Sources.PeakPickerTypes import *


def read_samples(wave_file: wave, frames_num: int) -> List[int]:
    """Reads raw samples from a wave file
    :param wave_file:   Input wave file containing audio data to analyse
    :param frames_num:  Number of frames to be read from the file
    :return:            Tuple containing raw samples
    :rtype:             tuple
# todo: Add a description of the returned data (channels and samples)
# todo: Add tests
    """
    frame_data = wave_file.readframes(frames_num)
    if frame_data:
        sample_width = wave_file.getsampwidth()
        sample_num = len(frame_data) // sample_width
        wave_format = {1: "%db", 2: "<%dh", 4: "<%dl"}[sample_width] % sample_num
        return list(struct.unpack(wave_format, frame_data))
    else:
        return []


def timepoint_to_sample(timepoint: float, rate=44100) -> sample_num_t:
    """
    :param timepoint:   Timepoint to be converted into sample number
    :param rate:        Input file sample rate
    :return:            Rounded value of a sample corresponding to the
                        input timepoint
    """
    return sample_num_t(round(float(timepoint) / (1 / rate)))


def sample_to_timepoint(sample, rate=44100) -> float:
    """
    :param sample:  Sample number to be converted into a timepoint
    :param rate:    Input file sample rate
    :return:        Value of a timepoint corresponding to the input
                    sample number
    """
    return float(sample * 1 / rate)


# todo: refactor the following functions
# todo: convert module into a class


def get_peaks_from_samples(samples: List[int], framerate=44100, threshold=12300) -> Sample:
    """
    :param samples:     Input list of samples represented by integers
    :param framerate:   Input file sample rate
    :param threshold:   Minimum sample threshold
    :return:            Tuple with sample number list and samples value list
    :rtype:             Sample
    """
    # minimum hit resolution set to 50ms - 16th notes in 300BPM
    peak_min_distance: sample_num_t = timepoint_to_sample(50 * 0.001, framerate)
    peaks, props = scipy.signal.find_peaks(samples, height=threshold, distance=peak_min_distance)
    x = Sample()
    x.number, x.value = peaks, props["peak_heights"]

    # todo: refine peaks - remove peaks in neighbourhood of the highest peak

    # x_normalized = []
    # first_peak = True
    # for i in range(0, len(x) - 1):
    #     print("x[i + 1]: %d, x[i]: %d, x[i + 1] - x[i]: %d, first_peak: %d" %
    #           (x[i + 1], x[i], x[i + 1] - x[i], first_peak))
    #     if x[i + 1] - x[i] > stroke_sample_span:
    #         # x_normalized.append(x[i])
    #         first_peak = True
    #     elif first_peak:
    #         x_normalized.append(x[i])
    #         first_peak = False
    #
    # y = []
    # for i in x_normalized:
    #     y.append(samples[i])
    # t = (x_normalized, y)

    return x
    # return t


def get_template_subticks_as_timepoints(click_duration: float, divisors: List[int]) -> List[float]:
    """
    :param click_duration:  Input duration of one click measured in seconds
    :param divisors:        Requested divisors of the beat
    :return:                Set of subdivisions of the input click measured in seconds
    :rtype:                 list[float]
    """
    subticks = set()
    for base in divisors:
        # add first beat
        subticks.add(0.0)
        for subbeat in range(1, base):
            subticks.add(subbeat * click_duration / base)
    return [sorted(subticks)][0]


@dispatch(list, int)
def get_avg_bpm(click: List[int], framerate) -> timepoint_t:
    """
    :param click:
    :param framerate:
    :return:
    """
    click_len = []
    for i in range(len(click) - 1):
        click_len.append(click[i + 1] - click[i])
    click_mean = statistics.mean(click_len)
    return sample_to_timepoint(click_mean, framerate)


@dispatch(list)
def get_avg_bpm(click: List[float]) -> sample_num_t:
    """
    :param click:
    :return:
    """
    click_len = []
    for i in range(len(click) - 1):
        click_len.append(click[i + 1] - click[i])
    click_mean = statistics.mean(click_len)
    return sample_num_t(round(click_mean))


def get_subticks_as_timepoints(template_subticks, peaks_timepoints):
    ret_subticks = []
    for timepoint in peaks_timepoints:
        for subtick in template_subticks:
            ret_subticks.append(timepoint + subtick)
    return [sorted(ret_subticks)][0]
