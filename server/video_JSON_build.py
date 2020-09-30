import os
import json

VIDEO_PATH = 'static/all'
TOTAL_SEGMENTS = 5
TOTAL_BITRATES = 10
FRAMES_PER_SEGMENT = 97
IFRAME_PER_SEGMENT = 9
IFRAME_FREQUENCY = 12
PFRAME_PER_SEGMENT = 88



properties = {}
properties['total_segments'] = TOTAL_SEGMENTS
properties['total_representations'] = TOTAL_BITRATES
properties['bitrates'] = [149974,
            285988,
            420968,
            572960,
            702064,
            803924,
            963899,
            1098811,
            1243279,
            1151095
            ] #bits per second
properties['total_duration'] = 15 #seconds
properties['frames_per_segment'] = FRAMES_PER_SEGMENT
properties['iframe_name'] = 'video_f_$frameNum$.p'
properties['flows_name'] = 'video_f_$frameNum$.p'
properties['pframe_name'] = 'video_t_$trackNum$_f_$frameNum$.p'


# media file details such as file name, segment duration, start index of segments
# change $REPID$ with representation ID and $Number$ with segment number to download.
properties['media'] = 'video_$trackNum$_dash$Number$.zip'
properties['duration'] = 3000
properties['timescale'] = 1000
properties['seg_start_number'] = 1

# video segment sizes
segments_size = []
for sg in range(0,TOTAL_SEGMENTS):
    seg_size = []
    for tk in range(TOTAL_BITRATES):
        s = 0
        currFrList = []
        for fr in range(1,98):
            if (fr-1) % 12 == 0:
                continue

            currFr = 97*sg + fr
            pfn = properties['pframe_name']
            pfn = pfn.replace('$trackNum$', str(tk+1).zfill(4)) \
                    .replace('$frameNum$', str(currFr).zfill(4))

            fp = os.path.join(VIDEO_PATH, 'pcodes',  pfn)
            s += os.path.getsize(fp)
            currFrList.append(currFr)
        print(f'current seg:{sg} current bitrate{tk}')
        print(currFrList)
        seg_size.append(s)
    
    segments_size.append(seg_size)
properties['segment_size_bytes'] = segments_size

# writes dict to file
with open(VIDEO_PATH + '/video_properties.json','w') as f :
    f.write(json.dumps(properties, indent=4))

