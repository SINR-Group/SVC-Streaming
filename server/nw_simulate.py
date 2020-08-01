import time
import json
import subprocess
import threading
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


class nw:
	def __init__(self):
		self.file = None
		self.thread = None
		self.traces = None
		self.flag = False

	def nwThread(self):

		create_handle_cmd[11] = str(self.traces[0]['latency_ms']) + 'ms'
		process = subprocess.Popen(create_handle_cmd)
		
		b = self.traces[0]['bandwidth_kbps']
		if b <= 0:
			b = 1
		
		limit_bandwidth_cmd[12] = str(b)+"kbit"
		limit_bandwidth_cmd[3] = "add"
		process = subprocess.Popen(limit_bandwidth_cmd)
		time.sleep(self.traces[0]['duration_ms'] * 0.001)

		# now every command we need to edit already specified rules
		limit_bandwidth_cmd[3] = "change"
		idx = 1

		while self.flag:			
			b = self.traces[idx]['bandwidth_kbps']
			if b <= 0:
				b = 1

			limit_bandwidth_cmd[12] = str(b)+"kbit"
			print(' '.join(limit_bandwidth_cmd))
			process = subprocess.run(limit_bandwidth_cmd)
			time.sleep(self.traces[idx]['duration_ms'] * 0.001)
			idx = (idx + 1) % len(self.traces)
		
		process = subprocess.Popen(del_cmd)

		print('thread exiting')
		


	def start(self, fileName):

		with open('nw_logs/'+fileName, 'r') as f:
			self.traces = json.loads(f.read())
		
		# print('starting thread')
		self.flag = True
		self.thread = threading.Thread(target=self.nwThread)
		self.thread.start()


	def stop(self):
		self.flag = False
		self.thread.join()
		return 'Nw Stopped'


# to add new handle
# sudo tc qdisc add dev enp3s0 root handle 1:0 netem delay 100ms

# sudo tc qdisc change dev enp3s0 parent 1:1 handle 10: tbf rate 256kbit buffer 160000 limit 300000
# sudo tc qdisc add dev enp3s0 root netem delay 200ms
# tc qdisc show  dev enp3s0
# sudo tc qdisc del dev enp3s0 root