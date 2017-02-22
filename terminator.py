#simple script to make sure that I don't leave AWS machines running
#NOTE: must be run with root privileges

####
# The script 
# 1. creates a file with one line specifying how much time t (in hours) to wait until shutdown
# 2. the script periodically reads this file for the last modification date (md) and the count down timer t
# 3. if md+t < current time, the script tries to shutdown the machine 

# There are two ways of postponing the shutdown:
#	1. 'touch' the [FNAME] file (thus changing it's last modification date)
#   2. replace the value on FNAME (e.g. 'echo 2 > [FNAME]' will reset the timer to 2 hours)
###

import numpy as np
import os 
import time
from ipdb import set_trace
import sys
DEFAULT_TIMER=2
FNAME=".ticktack"
HOUR=3600
MIN=60

def check(path):
	last_mod = os.path.getmtime(path)
	curr = time.time()	
	with open(FNAME) as fid:
		t = fid.readline()				
	timer = float(t)*HOUR
	delta = last_mod + timer - curr		
	if delta > 0:
		hours = np.floor(delta*1.0/HOUR)
		mins = (delta - hours*HOUR)/MIN
		sys.stderr.write("\rT - %d:%d" % (hours,mins))
		sys.stderr.flush()
		return False
	else:
		return True

if __name__ == "__main__":
	if not os.geteuid() == 0:
		sys.exit('Script must be run as root')
	with open(FNAME,"w") as fod: fod.write(str(DEFAULT_TIMER))	
	while not check(FNAME): time.sleep(MIN)	
	os.system("shutdown -h now")