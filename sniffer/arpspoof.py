import subprocess
import shlex


from sniffer.proc_utils import set_pid_status, DEVNULL
from sniffer.network_utils import get_interface, get_gw

def arpspoof():
    try:
        print 'arpspoof -i %s %s' % (str(get_interface()), str(get_gw()))
        p = subprocess.Popen(shlex.split('arpspoof -i %s %s' % (str(get_interface()), str(get_gw()))), stdout=DEVNULL, stderr=DEVNULL)
        set_pid_status('ARPSpoof',True,p.pid)
    except:
        set_pid_status('ARPSpoof',False)
