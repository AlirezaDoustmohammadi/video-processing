import cv2
import csv
import matplotlib.pyplot as plt
import numpy as np


def write_csv(luminance_fps, output_dir):
    # write results
    with open(output_dir + '/video_per_second_analysis.csv', 'w', newline='') as file:
        wr = csv.writer(file)

        # header
        wr.writerow(['Second', 'Luminance value'])

        for counter, element in enumerate(luminance_fps):
            wr.writerow([counter, luminance_fps[counter]])


def plot_Luminance(luminance_fps, video_time, output_dir):

    # baseline times (these lines was set manually according to V45 video) according to different scenarios of video
    baseline_time_a = [0, 1, 2]
    baseline_time_b = [16, 17, 18]
    baseline_time_c = [35, 36, 37]
    baseline_time_d = [47, 48]
    baseline_time_e = [64, 65, 66]
    baseline_time_f = [80, 81, 82]
    baseline_time_g = [93, 94, 95]
    baseline_time_h = [105, 106]
    baseline_time_i = [118, 119, 120]
    baseline_time_j = [134, 135, 136]

    baseline_luminance_a = []
    baseline_luminance_b = []
    baseline_luminance_c = []
    baseline_luminance_d = []
    baseline_luminance_e = []
    baseline_luminance_f = []
    baseline_luminance_g = []
    baseline_luminance_h = []
    baseline_luminance_i = []
    baseline_luminance_j = []

    for i in range(len(video_time)):
        if video_time[i] in baseline_time_a:
            baseline_luminance_a.append(luminance_fps[i])
        elif video_time[i] in baseline_time_b:
            baseline_luminance_b.append(luminance_fps[i])
        elif video_time[i] in baseline_time_c:
            baseline_luminance_c.append(luminance_fps[i])
        elif video_time[i] in baseline_time_d:
            baseline_luminance_d.append(luminance_fps[i])
        elif video_time[i] in baseline_time_e:
            baseline_luminance_e.append(luminance_fps[i])
        elif video_time[i] in baseline_time_f:
            baseline_luminance_f.append(luminance_fps[i])
        elif video_time[i] in baseline_time_g:
            baseline_luminance_g.append(luminance_fps[i])
        elif video_time[i] in baseline_time_h:
            baseline_luminance_h.append(luminance_fps[i])
        elif video_time[i] in baseline_time_i:
            baseline_luminance_i.append(luminance_fps[i])
        elif video_time[i] in baseline_time_j:
            baseline_luminance_j.append(luminance_fps[i])

    # Data for plotting
    fig, ax = plt.subplots()
    ax.plot(video_time, luminance_fps, color='r')
    ax.plot(baseline_time_a, baseline_luminance_a, color='b')
    ax.plot(baseline_time_b, baseline_luminance_b, color='b')
    ax.plot(baseline_time_c, baseline_luminance_c, color='b')
    ax.plot(baseline_time_d, baseline_luminance_d, color='b')
    ax.plot(baseline_time_e, baseline_luminance_e, color='b')
    ax.plot(baseline_time_f, baseline_luminance_f, color='b')
    ax.plot(baseline_time_g, baseline_luminance_g, color='b')
    ax.plot(baseline_time_h, baseline_luminance_h, color='b')
    ax.plot(baseline_time_i, baseline_luminance_i, color='b')
    ax.plot(baseline_time_j, baseline_luminance_j, color='b')

    ax.set(xlabel='second', ylabel='Luminance value', title='')
    ax.grid()

    fig.savefig(output_dir + "/Luminance_per_second.png")
    plt.show()


def read_video_file(video_file):
    # read video file
    video = cv2.VideoCapture(video_file)

    return video


def measure_luminance(video):
    # get all frames and frames status (correct or incorrect)
    okay, frame = video.read()
    print(f'# Video appears to be {len(frame[0])} x {len(frame)}')

    # number of frames
    frame_number = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # FPS (frame rate)
    frame_rate = round(video.get(cv2.CAP_PROP_FPS))

    # Process each frame.
    # storing luminance of each frame in Luminance list
    luminance = []

    # for all correct frames
    while okay:
        avg_color_per_row = np.average(frame, axis=0)
        # in BGR Format
        avg_color = np.average(avg_color_per_row, axis=0)
        # https://en.wikipedia.org/wiki/Relative_luminance
        # luminance = 0.2126 * R + 0.7152 * G+ 0.0722 * B
        luminance_val = 0.2126 * avg_color[2] + 0.7152 * avg_color[1] + 0.0722 * avg_color[0]
        luminance.append(luminance_val)
        # read next frame
        okay, frame = video.read()

    # storing luminance of each second in luminance_fps list
    luminance_fps = [np.mean(luminance[i:i + frame_rate]) for i in range(0, len(luminance), frame_rate)]
    video_time = list(range(0, round(len(luminance) / frame_rate)))

    return luminance_fps, video_time


if __name__ == '__main__':
    video_file = '../input video/V45.mp4'
    output_dir = '../outputs'

    video = read_video_file(video_file)
    luminance_fps, video_time = measure_luminance(video)
    plot_Luminance(luminance_fps, video_time, output_dir)
    write_csv(luminance_fps, output_dir)

