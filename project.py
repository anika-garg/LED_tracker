import csv
from datetime import datetime, timedelta
from moviepy.editor import VideoFileClip, concatenate_videoclips 
import os
import shutil
import pandas as pd
import sys

class LightRow:
    def __init__(self):
        self.blink_start = None
        self.blink_end = None
        self.person_start = None
        self.person_end = None
        self.end = None

# create videos.csv

# folder argument
folder = str(sys.argv[1])

# make list of datetime objects of video start times
video_times = []
with open("/Users/anikagarg/Desktop/" + folder + "/videos.csv") as file:
    csvreader = csv.reader(file)
    header = next(csvreader)
    for row in csvreader:
        for date in row:
            datetimeOb = datetime.strptime(date[0:-4], '%Y-%m-%d-%H-%M-%S')
            video_times.append(datetimeOb)
list.sort(video_times)

# make sorted list of filenames of video start times
video_filenames = []
for v in video_times:
    filename = v.strftime('%Y-%m-%d-%H-%M-%S')
    video_filenames.append(filename + ".avi")


# make nested list of datetime objects of blinking [start_time, end_time]
light_rows = []
with open("/Users/anikagarg/Desktop/" + folder + "/events.csv") as file2:
    csvreader2 = csv.reader(file2)
    header = next(csvreader2)
    for row in csvreader2:
        # light_start_time = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        # light_end_time = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
        # person_arrives= light_start_time + timedelta(seconds = (int(row[4])))
        # person_leaves = light_start_time + timedelta(seconds = (int(row[4]) + int(row[5])))
        # end_time = max(light_end_time, person_leaves)
        # light_rows.append([light_start_time, end_time])
        light_row = LightRow()
        light_row.blink_start = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        light_row.blink_end = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
        light_row.person_start = light_row.blink_start + timedelta(seconds = (int(row[4])))
        light_row.person_end = light_row.blink_start + timedelta(seconds = (int(row[4]) + int(row[5])))
        light_row.end = max(light_row.blink_end, light_row.person_end)
        light_rows.append(light_row)

# function to find start video
def nearest_start(items, pivot):
    return min([i for i in items if i <= pivot], key=lambda x: abs(x - pivot))

# function to find end video
def nearest_end(items, pivot):
    # later = filter(lambda d: d > pivot, items)
    # return min(later, key=lambda x: abs(x - pivot))
    # later = filter(lambda d: d > pivot, items)
    # if (len(list(later)) > 0):
    #     return min(later, key = lambda d: d)
    # return min(items, key=lambda s: s - pivot)
    later = []
    for i in items:
        if i > pivot:
            later.append(i)
    if len(later) > 0:
        return min(later, key=lambda x: abs(x - pivot))
    else:
        # return "anikagarg/Desktop/vid2.csv"
        return items[0]


# ex = light_times[0][1]
# end_video = nearest_end(video_times,ex)
# print(ex)
# print(end_video)

# make nested list of indexes of videos [start_idx, end_idx]
indexes = []
for light_row in light_rows:
    start_video = video_times.index(nearest_start(video_times, light_row.blink_start))
    end_video = video_times.index(nearest_end(video_times, light_row.end))
    indexes.append([start_video, end_video])

#. 1 for loop for light time
#. 1.5 
#. 2 inner for loop going through video times
#. 3 keep track of closest start and end time


# concatenate video clips and save to folder, add video name and time stamp columns to csv
df = pd.read_csv("/Users/anikagarg/Desktop/" + folder + "/events.csv")
os.makedirs("/Users/anikagarg/Desktop/" + folder + "/Final_Videos", exist_ok=True)
for i in range(len(indexes)):
    start_idx, end_idx = indexes[i]
    clips = []
    for j in range(start_idx, end_idx):
        clips.append(VideoFileClip("/Users/anikagarg/Desktop/" + folder + "/Videos/" + video_filenames[j]))
    final_clip = concatenate_videoclips(clips, method = 'compose')
    final_clip_name = "video_" + str(video_filenames[start_idx]) + ".mp4"
    final_clip.write_videofile(final_clip_name)
    shutil.move("/Users/anikagarg/Desktop/" + final_clip_name, "/Users/anikagarg/Desktop/" + folder + "/Final_Videos/")
    df.loc[df.index[i], 'video_name'] = final_clip_name
    df.loc[df.index[i], 'start_timestamp'] = str(light_rows[i].blink_start - video_times[indexes[i][0]])
    df.loc[df.index[i], 'arrives_timestamp'] = str(light_rows[i].person_start - video_times[indexes[i][0]])
    df.loc[df.index[i], 'stop_timestamp'] = str(light_rows[i].blink_end - video_times[indexes[i][0]])
    df.loc[df.index[i], 'leaves_timestamp'] = str(light_rows[i].person_end - video_times[indexes[i][0]])
df.to_csv("/Users/anikagarg/Desktop/" + folder + "/events_copy.csv", index=False)












