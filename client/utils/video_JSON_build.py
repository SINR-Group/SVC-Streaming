import os
import json

VIDEO_PATH = '/home/arian/aakash/10minVid/static/video1'
TOTAL_SEGMENTS = 300
TOTAL_BITRATES = 5

properties = {}
properties['total_segments'] = TOTAL_SEGMENTS
properties['total_representations'] = TOTAL_BITRATES
properties['bitrates'] = [214915, 562660, 990946, 1520727, 2963872] #bits per second
properties['total_duration'] = 600 #seconds
properties['duration'] = 2000 # milliseconds
properties['timescale'] = 1000

properties['start_number'] = 0

# change $REPID$ with representation ID and $Number$ with segment number to download.
fileName = 'video_$REPID$_dash$Number$.zip'
properties['media'] = fileName


# video segment sizes
segments_size = []
for i in range(0, TOTAL_SEGMENTS):
    seg_size = []
    for j in range(TOTAL_BITRATES):
        fp = VIDEO_PATH + '/' + fileName.replace('$REPID$',str(j+1)).replace('$Number$',str(i))
        s = os.path.getsize(fp)
        seg_size.append(s)
    
    segments_size.append(seg_size)
properties['segment_size_bytes'] = segments_size

# writes dict to file
with open(VIDEO_PATH + '/video_properties.json','w') as f :
    json.dump(properties, f)

