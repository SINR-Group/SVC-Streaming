## Instructions for client player
1. [Start Server](../../server/) on remote machine 
2. Then change variables accordingly in [meta.py](meta.py)
   - base_url : url of server machine
   - manifest_path : relative path of json file. to be place inside static folder on server.
   - rules : list of abr rules to run.
   - nw_files: list of relative path of network file trace. Full 3g and 4g file traces path are in [nw_filenames.py](nw_filenames.py). Make sure traces that you select are present in [nw_logs folder](../../server/nw_logs/) at server. Use `nw_files = ['normal_nw']` if you don't want to run network trace.
   - lastSeg: set it to number of segments you want to download. Helpful if you don't want to wait and test for full video. `lastSeg = 60` will download first 60 segment. set it to `lastSeg = -1` to download all segments.
   - resultFileName :file name prefix to save results.
3. Finally run `python3 stream.py`, after successful run, it will save observed results in json file. Change name of file
