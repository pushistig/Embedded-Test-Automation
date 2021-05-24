import paramiko
from constants.credential import *


class AllHelper:

    def connect_to_vm(self):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(IP_VM, username=USERNAME_VM, password=PASSWORD_VM)
        print("Connected")

    def handle_write(self):
        handle = open("test.txt", "w")
        # handle.write("This is SPARTA!")   #-----------Example 1
        handle.writelines(["\nThis is", "\nis", "\nSPARTA!"])

    def handle_read(self):
        handle = open("test.txt", "r")
        data = handle.read()
        print(data)

    def open_rb(self):
        open("D:/test.pdf", "rb")




        

