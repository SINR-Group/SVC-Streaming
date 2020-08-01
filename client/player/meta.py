import nw_filenames

base_url = 'http://130.245.144.152:5000/'
manifest_path = 'video1/video_properties.json'

# rules = ['tputRule', 'BBA0', 'BBA2', 'Bola']
rules = ['Bola']

# nw_files = nw_filenames.logs3g
# nw_files=['3Glogs/report.2011-01-04_0820CET.json', '4Glogs/report_bus_0011.json']

nw_files=['normal_nw']

# number of segments to download. -1 will download full video.
lastSeg = 60

nw_trace_start_url = base_url + 'networkTrace?file='
nw_trace_stop_url = base_url + 'stopNWtrace'

