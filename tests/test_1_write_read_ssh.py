import io
import shutil

import paramiko
import os
import time
import scp

from scp import SCPClient
from constants.credential import *
from constants.folders import *
from helpers.all_helpers import AllHelpers


class TestController:

    def test_1_write_and_read_to_txt_on_pc(self):
        all_helpers = AllHelpers()
        all_helpers.handle_write()

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

    def test_3_read_part_on_pc(self):
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

    def test_4_read_pdf_binary_on_pc(self):
        handle = open(TEST_D_TXT1, "rb")
        data = handle.read()
        print(data)
        handle.close()

    def test_5_write_txt_on_pc(self):
        newFileBytes = [123, 3, 255, 0, 100]
        # make file
        newFile = open(FILENAME_TXT, "wb")
        # write to file
        for byte in newFileBytes:
            newFile.write(byte.to_bytes(1, byteorder='big'))

    def test_6_write_txt_binary_pc(self):
        handle = open(TEST_TXT, 'w+b')
        byte_arr = [120, 3, 255, 0, 100]
        binary_format = bytearray(byte_arr)
        handle.write(binary_format)
        handle.close()

    def test_7_write_binary_file_example_on_pc(self):
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

    def test_8_write_txt_binary_1_on_pc(self):
        handle = open(TEST_TXT1, "wb")
        handle.write(b"This binary string will be written to test1.txt")
        handle.close()

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
        print('Read_on_vm done')


    def test_11_create_and_put_txt_pc_to_vm(self):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(IP_VM, username=USERNAME_VM, password=PASSWORD_VM)
        print("Connected")

        # all_helpers = AllHelper()
        # all_helpers.connect_to_vm()

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
        print('Create_and_put done')

    def test_12_copy_pdf_to_vm(self):
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(IP_VM, username=USERNAME_VM, password=PASSWORD_VM)
        print("Connected")


        sftp = ssh.open_sftp()
        sftp.put(TEST_PDF_PC, PATH_TEST_PDF_ON_VM)
        sftp.close()
        ssh.close()
        print('Copy done')

    def test_13_get_current_directory_on_pc(self):
        current_dir = os.getcwd()
        print(current_dir)

    def test_14_write_edit_test2_on_pc(self):
        f = open("test2.txt", "a")
        f.write("Now the file has more content!")
        f.close()

        # open and read the file after the appending:
        f = open("test2.txt", "r")
        print(f.read())

        d = open("test2.txt", "w")
        d.write("Woops! I have deleted the content!")
        d.close()

        # open and read the file after the appending:
        d = open("test2.txt", "r")
        print(d.read())

    def test_15_delete_test2_on_pc(self):
        # Remove the file "test2.txt":
        if os.path.exists("test2.txt"):
            os.remove("test2.txt")
        else:
            print("The file does not exist")

    # def test_16_create_folder_on_pc(self):
    #     # create current folder
    #     os.mkdir("hello")
    #     # create custom folder
    #     os.mkdir("c://test_create_dir")
    #     os.mkdir("c://test_create_dir/second_dir_hello")

    def test_17_create_and_delete_folder_on_pc(self):
        # create current folder
        os.mkdir("hello_2")
        # delete current folder
        os.rmdir("hello_2")

        # create custom folder
        os.mkdir("c://test_create_dir_2")
        os.mkdir("c://test_create_dir_2/second_dir_hello_2")
        # delete custom folder
        os.rmdir("c://test_create_dir_2/second_dir_hello_2")
        os.rmdir("c://test_create_dir_2")

    def test_18_create_and_rename_folder_on_pc(self):
        # create current folder
        os.mkdir("hello_2")
        # rename current folder
        os.rename("hello_2", "hello_4")
        os.rmdir("hello_4")

        # rename(source, target)
        os.mkdir("c://test_create_dir_2")
        os.rename("c://test_create_dir_2", "c://test_create_dir_3")
        os.rmdir("c://test_create_dir_3")

# ----------------------------------archive---------------------------------------
    def test_19_create_archive_on_pc(self):
        # create current folder
        # os.mkdir('C://otcuda')
        # open('C://otcuda/textfile_1.txt', 'tw', encoding='utf-8').close()
        # os.mkdir('C://cuda')

        # Files and directories to be copied are collected in a list.
        source = 'C:/otcuda'
        target_dir = 'C:/cuda'
        target = target_dir + os.sep + time.strftime("%Y%m%d%H%M%S") + ".zip"
        zip_command = "zip -qr {0} {1}".format(target, " ".join(source))
        # start creating a zip
        print(zip_command)

        error = os.system(zip_command)
        if error == 0:
            print('zip was successfully created in ', target)
        else:
            print('zip creation Failed ')
            print('Error = ', error)

    def test_20_move_file_to_new_folder_on_pc(self):
        all_helpers = AllHelpers()
        all_helpers.handle_write()

        os.mkdir("hello_5")
        # Move file to new folder
        shutil.move(TEST_TXT, FOLDER_HELLO5)
        file_list = os.listdir()
        print(file_list)

        # Rename TXT file
        os.rename("hello_5/test.txt", "hello_5/test666.txt")

        # List
        for dirpath, dirnames, filenames in os.walk("."):
            # iterate over directories
            for dirname in dirnames:
                print("Folder:", os.path.join(dirpath, dirname))
            # iterate over files
            for filename in filenames:
                print("File:", os.path.join(dirpath, filename))
        # Delete txt file
        os.remove("hello_5/test666.txt")
        os.rmdir("hello_5")

    def test_21_copy_file_txt_to_new_folder_on_pc(self):
        all_helpers = AllHelpers()
        all_helpers.handle_write()
        os.mkdir("hello_5")

        # Move file to new folder
        shutil.move(TEST_TXT, FOLDER_HELLO5)
        # shutil.copy(TEST_D_TXT1, FOLDER_HELLO5)     # -----another directories

        # Delete txt file
        os.remove("hello_5/test.txt")
        os.rmdir("hello_5")
        print('TXT copied and deleted ')
