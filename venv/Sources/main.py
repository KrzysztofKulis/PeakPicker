import wave
import matplotlib.pyplot as plt
from typing import List

import Sources.PeakPicker as pp


def main():
    # load wave samples
    file = wave.open(r"C:\Users\Kulio\Documents\Python\Precyzja\single_stroke_four_mono.wav")
    raw_samples: List[int] = pp.read_samples(file, file.getnframes())

    # define peaks
    peaks: pp.Sample = pp.get_peaks_from_samples(raw_samples, file.getframerate())

    # draw samples and peaks
    plt.plot(peaks.number, peaks.value, '.r')
    plt.plot(list(range(0, len(raw_samples))), raw_samples)
    #plt.pause(0.001)

    # determine tempo by the first 5 peaks (4 beat durations)
    clicks = list(peaks.number[0:5])
    click_duration = pp.get_avg_bpm(clicks, file.getframerate())

    # find peaks closest to click grid
    closest = pp.find_closest_peaks(peaks, click_duration)
    plt.plot(closest.number, closest.value, '^g')
    #plt.pause(0.001)

    # acquire template subticks
    divisors = [3]
    template_subticks = pp.get_template_subticks_as_timepoints(click_duration, divisors)

# todo: last job end is right here
    # calculate subticks for the peaks
    peaks_timepoints = []
    for peak in peaks.number[5:]:
        peaks_timepoints.append(pp.sample_to_timepoint(peak, file.getframerate()))
    subticks = [sorted(pp.get_subticks_as_timepoints(template_subticks, peaks_timepoints))]

    subticks_samples = []
    for subtick in subticks[0]:
        subticks_samples.append(pp.timepoint_to_sample(subtick))

    subticks_y = [30000] * len(subticks[0])
    plt.plot(subticks_samples, subticks_y, '.g')
    plt.show()
    return
if __name__ == "__main__":
    main()
