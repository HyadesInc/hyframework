import os

from status.models import Status

DEVNULL = open(os.devnull, 'wb')

def is_process_running(process_id):
    try:
        os.kill(process_id, 0)
        print 'Proc %s running' % process_id 
        return True
    except OSError, err:
        import errno
        if err.errno == errno.ESRCH:
            print "Proc %s not running" % process_id
            return False
        elif err.errno == errno.EPERM:
            return True
        else:
            print "Proc %s generated an unknown error" % process_id

def monitor():
    arpspoof = Status.objects.get(name='ARPSpoof')
    sslstrip = Status.objects.get(name='SSLStrip')
    
    if not is_process_running(arpspoof.pid):
        print 'lol arp'
        arpspoof.status = False
        arpspoof.save()
        
    if not is_process_running(sslstrip.pid):
        print 'lol ssl'
        sslstrip.status = False
        sslstrip.save()

def set_pid_status(process,status,pid='0'):
    try:
        proc = Status.objects.get(name=process)
        proc.pid = pid
        proc.status = status
        proc.save()
    except:
        from django.db import transaction
        with transaction.commit_on_success():
            Status.objects.create(name=process,pid=pid,status=status)
            
def kill_helpers(helper='all'):
    if helper == 'all':
        for proc in Status.objects.all():
            os.kill(proc.pid, 9)
    elif helper == 'sslstrip':
        proc = Status.objects.get(name='SSLStrip')
        os.kill(proc.pid, 9)
    elif helper == 'arpspoof':
        proc = Status.objects.get(name='ARPSpoof')
        os.kill(proc.pid, 9)
            
def run_helpers(helper='all'):
    from sniffer.network_utils import iptables, get_promiscuous, ip_forward
    ip_forward()
    #iptables()
    #get_promiscuous()
    if helper == 'all':
        from sniffer.sslstrip import sslstrip
        from sniffer.arpspoof import arpspoof
        
        #sslstrip()
        arpspoof()
    elif helper == 'sslstrip':
        from sniffer.sslstrip import sslstrip
        sslstrip()
    elif helper == 'arpspoof':
        from sniffer.arpspoof import arpspoof
        arpspoof()
