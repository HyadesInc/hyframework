import subprocess
import shlex

from sniffer.proc_utils import set_pid_status, DEVNULL


def sslstrip():
    try:
        p = subprocess.Popen(shlex.split('sslstrip -l 10000 -f -k'), stdout=DEVNULL, stderr=DEVNULL)
        set_pid_status('SSLStrip',True,p.pid)
    except:
        set_pid_status('SSLStrip',False)