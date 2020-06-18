import json
import subprocess
import time

# creates handle with 20ms packet delay
create_handle_cmd = ["sudo", "/sbin/tc", "qdisc", "add", "dev", "enp3s0", "root", 
                     "handle", "1:0", "netem", "delay", "20ms", "limit", "300000"]

# change network rule as specified
limit_bandwidth_cmd = ["sudo", "/sbin/tc", "qdisc", "add", "dev", "enp3s0",
                        "parent", "1:1", "handle", "10:", "tbf", "rate", "256kbit",
                        "buffer", "160000", "limit", "300000"]

# to delete all applied rules
del_cmd = ["sudo", "/sbin/tc", "qdisc", "del", "dev", "enp3s0", "root"]

# to show current network rules
check_cmd = ["sudo", "tc", "qdisc", "show", "dev", "enp3s0"]

trace_file = "3Greport.2010-09-13_1003CEST.json"
# 3Greport.2010-09-13_1003CEST.json

with open(trace_file,'r') as f:
    traces = json.loads(f.read())

# add command for first time. 
create_handle_cmd[create_handle_cmd.index('delay') + 1] = str(traces[0]['latency_ms']) + 'ms'
process = subprocess.Popen(create_handle_cmd)

rate_idx = limit_bandwidth_cmd.index("rate")
limit_bandwidth_cmd[rate_idx+1] = str(traces[0]['bandwidth_kbps'])+"kbit"

process = subprocess.Popen(limit_bandwidth_cmd)
time.sleep(traces[0]['duration_ms'] * 0.001)

# change command from add to change already specified rule
limit_bandwidth_cmd[limit_bandwidth_cmd.index("add")] = "change"

# NOTE: can we change it to something better instead of 20 time loop
for i in range(20):
    print("iter:{}".format(i))
    for a in traces:
        limit_bandwidth_cmd[rate_idx+1] = str(a['bandwidth_kbps'])+"kbit"
        # print(str(limit_bandwidth_cmd))
        process = subprocess.run(limit_bandwidth_cmd)
        time.sleep(a['duration_ms'] * 0.001)
        # print("next",a)

# before exiting delete all changed rules
process = subprocess.Popen(del_cmd)


# to add new handle
# sudo tc qdisc add dev enp3s0 root handle 1:0 netem delay 100ms

# sudo tc qdisc change dev enp3s0 parent 1:1 handle 10: tbf rate 256kbit buffer 160000 limit 300000
# sudo tc qdisc add dev enp3s0 root netem delay 200ms
# tc qdisc show  dev enp3s0
# sudo tc qdisc del dev enp3s0 root

# default rules
# arian@abbas-lab:~/aakash/networkSimulator$ tc qdisc show  dev enp3s0
# qdisc pfifo_fast 0: root refcnt 2 bands 3 priomap  1 2 2 2 1 2 0 0 1 1 1 1 1 1 1 1