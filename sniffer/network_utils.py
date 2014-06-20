import subprocess
import shlex

def iptables():
    subprocess.check_output(shlex.split('iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-ports 10000'))

def ip_forward():
    subprocess.check_output(shlex.split('sysctl -w net.ipv4.ip_forward=1'))
        
def get_gw():
    ip = subprocess.Popen(shlex.split('ip route show'), stdout=subprocess.PIPE) 
    grep = subprocess.Popen(shlex.split('grep "default via"'), stdout=subprocess.PIPE, stdin=ip.stdout)
    return str(subprocess.check_output(shlex.split("awk '{print$3}'"), stdin=grep.stdout)).strip()
    
def get_interface():
    ip = subprocess.Popen(shlex.split('ip route show'), stdout=subprocess.PIPE) 
    grep = subprocess.Popen(shlex.split('grep "default via"'), stdout=subprocess.PIPE, stdin=ip.stdout)
    return str(subprocess.check_output(shlex.split("awk '{print$5}'"), stdin=grep.stdout)).strip()
    
    
def get_promiscuous():
    subprocess.check_output(shlex.split('airmon-ng start %s' % str(get_interface())))