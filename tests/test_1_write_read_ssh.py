import io
import paramiko
from scp import SCPClient
from constants.credential import *
from constants.folders import *
from helpers.all_helper import AllHelper


class TestController:

    def test_1_write_and_read_to_txt(self):
        all_helper = AllHelper()
        all_helper.handle_write()

        handle = open(TEST_TXT, "r")
        # handle = open("D:/test.txt", "r")  # example2 Opens along the path
        data = handle.read()
        # data = handle.readline()  # example1 read just one line
        # data = handle.readlines() # example2 read ALL the lines!
        print(data)
        write = list(data)
        read = ['\n', 'T', 'h', 'i', 's', ' ', 'i', 's', '\n', 'i', 's', '\n', 'S', 'P', 'A', 'R', 'T', 'A', '!']
        assert write == read
        print(list(data))
        handle.close()

    def test_3_read_part(self):
        handle = open("D:/test.pdf", "rb")

        for line in handle:
            print(line)
        handle.close()
        handle = open("D:/test.pdf", "rb")
        while True:
            data = handle.read(1024)
            print(data)

            if not data:
                break
        with open(TEST_TXT, "r") as handle:
            text = handle.read(16)
            print(text)
        with open(TEST_TXT, "r") as handle:  # 'Hello, world!'
            first_part = handle.read(9)  # 'Hello, w'
            handle.seek(4)
            second_part = handle.read(12)  # 'o, world'
            print(first_part)
            print(second_part)

    def test_4_read_pdf_binary(self):
        handle = open(TEST_D_TXT1, "rb")
        data = handle.read()
        print(data)
        handle.close()

    def test_5_write_txt(self):
        newFileBytes = [123, 3, 255, 0, 100]
        # make file
        newFile = open(FILENAME_TXT, "wb")
        # write to file
        for byte in newFileBytes:
            newFile.write(byte.to_bytes(1, byteorder='big'))

    def test_6_write_txt_binary(self):
        f = open(TEST_TXT, 'w+b')
        byte_arr = [120, 3, 255, 0, 100]
        binary_format = bytearray(byte_arr)
        f.write(binary_format)
        f.close()

    def test_7_write_binary_file_example(self):
        import numpy as np
        import struct

        with open('binary.file', 'wb') as f:
            i = 777
            if isinstance(i, int):
                f.write(struct.pack('i', i))  # write an int
            elif isinstance(i, str):
                f.write(i)  # write a string
            else:
                raise TypeError('Can only write str or int')

        with open('binary.file', 'rb') as g:
            first = np.fromfile(g, dtype=np.uint32, count=1)
            second = np.fromfile(g, dtype=np.float64, count=1)

        print(first, second)

    def test_8_write_txt_binary_1(self):
        file = open(TEST_TXT1, "wb")
        file.write(b"This binary string will be written to test1.txt")
        file.close()

    def test_9_from_vm_to_pc(self):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(IP_VM, username=USERNAME_VM, password=PASSWORD_VM)
        print("Connected")
        scp = SCPClient(ssh.get_transport())
        scp.get(TEST_UB_TXT1_ON_VM)
        scp.close()

        handle = open(TEST_UB_TXT1, "r")
        data = handle.read()
        print(data)
        s = list(data)
        l = ['E', 'p', 'i', 'c', ' ', 'w', 'i', 'n', '!', '!', '!', ' ', 'y', 'o', 'u', ' ', 'G', 'O', 'O', 'D', '\n']
        assert s == l
        print(list(data))
        handle.close()

    def test_10_read_on_vm(self):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(IP_VM, username=USERNAME_VM, password=PASSWORD_VM)
        print("Connected")
        scp = SCPClient(ssh.get_transport())
        scp.get(TEST_UB_TXT1_ON_VM)
        scp.close()


    def test_11_create_and_put_txt_to_vm(self):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(IP_VM, username=USERNAME_VM, password=PASSWORD_VM)
        print("Connected")

        # all_helper = AllHelper()
        # all_helper.connect_to_vm()

        # generate in-memory file-like object
        handle = io.BytesIO()
        handle.write(b'Now Sparta is here !!! ')
        handle.seek(0)
        # upload it directly from memory
        scp = SCPClient(ssh.get_transport())
        scp.putfo(handle, PATH_TEST_WIN_TXT_ON_VM)
        # close connection
        scp.close()
        # close file handler
        handle.close()

    def test_12_copy_pdf_to_vm(self):
        import scp
        import paramiko
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(IP_VM, username=USERNAME_VM, password=PASSWORD_VM)
        print("Connected")

        sftp = ssh.open_sftp()
        sftp.put(TEST_PDF_PC, PATH_TEST_PDF_ON_VM)
        sftp.close()
        ssh.close()


