import os, csv

f=open("/Users/anikagarg/Desktop/videos.csv",'r+')

w=csv.writer(f)
for path, dirs, files in os.walk("/Users/anikagarg/Desktop/Videos"):
    for filename in files:
        w.writerow([filename])