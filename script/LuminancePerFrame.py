import cv2
import csv
import matplotlib.pyplot as plt
import numpy as np


def plot_Luminance(luminance, output_dir):
    # baseline times (these lines was set manually according to V45 video) according to different scenarios of video
    video_time = list(range(0, round(len(luminance))))
    baseline_time_a = list(range(0, 109))
    baseline_time_b = list(range(471, 580))
    baseline_time_c = list(range(1044, 1153))
    baseline_time_d = list(range(1384, 1493))
    baseline_time_e = list(range(1911, 2020))
    baseline_time_f = list(range(2392, 2501))
    baseline_time_g = list(range(2787, 2896))
    baseline_time_h = list(range(3129, 3238))
    baseline_time_i = list(range(3524, 3633))
    baseline_time_j = list(range(4000, 4111))

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
            baseline_luminance_a.append(luminance[i])
        elif video_time[i] in baseline_time_b:
            baseline_luminance_b.append(luminance[i])
        elif video_time[i] in baseline_time_c:
            baseline_luminance_c.append(luminance[i])
        elif video_time[i] in baseline_time_d:
            baseline_luminance_d.append(luminance[i])
        elif video_time[i] in baseline_time_e:
            baseline_luminance_e.append(luminance[i])
        elif video_time[i] in baseline_time_f:
            baseline_luminance_f.append(luminance[i])
        elif video_time[i] in baseline_time_g:
            baseline_luminance_g.append(luminance[i])
        elif video_time[i] in baseline_time_h:
            baseline_luminance_h.append(luminance[i])
        elif video_time[i] in baseline_time_i:
            baseline_luminance_i.append(luminance[i])
        elif video_time[i] in baseline_time_j:
            baseline_luminance_j.append(luminance[i])

    # Data for plotting
    fig, ax = plt.subplots()
    ax.plot(video_time, luminance, color='r')
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

    ax.set(xlabel='frame number', ylabel='Luminance value', title='')
    ax.grid()
    fig.savefig(output_dir + "/Luminance_per_frame.png")
    plt.show()


def write_csv(luminance, output_dir):
    # write results
    with open(output_dir + '/video_frames_analysis.csv', 'w', newline='') as video_analysis:
        wr = csv.writer(video_analysis)

        # header
        wr.writerow(['Frame', 'Luminance value'])

        for counter, element in enumerate(luminance):
            wr.writerow([counter + 1, luminance[counter]])


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
    print('Frame Numbers:' + str(frame_number))

    # Process each frame.
    # storing luminance of each frame in Luminance list
    luminance = []

    # for all correct frames
    while okay:
        avg_color_per_row = np.average(frame, axis=0)
        # in BGR Format
        avg_color = np.average(avg_color_per_row, axis=0)
        # https://en.wikipedia.org/wiki/Relative_luminance
        # Luminance = 0.2126 * R + 0.7152 * G+ 0.0722 * B
        luminance_val = 0.2126 * avg_color[2] + 0.7152 * avg_color[1] + 0.0722 * avg_color[0]
        luminance.append(luminance_val)
        # read next frame
        okay, frame = video.read()

    return luminance


if __name__ == '__main__':
    video_file = '../input video/V45.mp4'
    output_dir = '../outputs'
    video = read_video_file(video_file)
    luminance = measure_luminance(video)
    plot_Luminance(luminance, output_dir)
    write_csv(luminance, output_dir)
