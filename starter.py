from ftplib import FTP
from os import system

ftp = FTP('31.31.196.63')
ftp.login(user='u1270293_spbubot', passwd = 'lE0lH4oT0wpU1f')

print("successfully connected")
print ("File List:")
files = ftp.dir()
print (files)