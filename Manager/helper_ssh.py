import time

import logger
import paramiko
import scp
from pandas.errors import EmptyDataError
from paramiko import AuthenticationException
import pandas as pd
from conftest import option

class HelperSsh:
    def __init__(self):
        self.target_host = option.target_host
        self.target_user = option.target_user
        self.target_password = option.target_password
        #self.ssh_key_filepath = ssh_key_filepath
        #self.remote_path = remote_path
        self.ssh_client = None
        self.scp_client = None
        self.ssh_connection = None
        self.sftp_client = None

    def initialize_connection(self):
        print("!!!!!!   0 " + str(self.ssh_connection))
        if self.ssh_connection is None:
            try:
                self.ssh_client = paramiko.SSHClient()
                self.ssh_client.load_system_host_keys()
                self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh_client.connect(hostname=self.target_host, username=self.target_user, password=self.target_password,
                                   key_filename="/home/vitalyb/.ssh/id_rsa", look_for_keys=False)
                self.scp_client = scp.SCPClient(self.ssh_client.get_transport())
                #self.sftp_client = paramiko.SFTPClient.from_transport(self.ssh_client.get_transport())
                #self.sftp_client = self.scp_client.open_sftp()
            except AuthenticationException as error:
                logger.error(f'Authentication failed: \
                    did you remember to create an SSH key? {error}')
                raise error
        return self.ssh_client

    def disconnect(self):
        #print("!!!!!!   1 " + str(self.ssh_connection))
        if self.ssh_client:
            self.ssh_client.close()
            #print("!!!!!!   2 " + str(self.ssh_client))
        if self.ssh_connection:
            self.ssh_connection.close()
            #print("!!!!!!   3 " + str(self.ssh_connection))
        if self.sftp_client:
            self.sftp_client.close()
            #print("!!!!!!   3 " + str(self.ssh_connection))
        if self.scp_client:
            self.scp_client.close()

        print("!!!!!!   4 " + str(self.ssh_connection))
        # if self.scp:
        #     self.scp.close()

    def execute_commands(self, commands):
        if self.ssh_connection is None:
            print("!!!!!!   execute_commands if ssh_connection is None")
            self.ssh_connection = self.initialize_connection()

        transport = self.ssh_client.get_transport()
        session = transport.open_session()
        # session.set_combine_stderr(True)
        session.get_pty()
        session.exec_command(commands)
        return session

    #TODO: should exit from loop
    def read_scv_remote(self, path, skip_rows, is_run_completed):
        global df
        if self.ssh_connection is None:
            print("!!!!!!   execute_commands if ssh_connection is None")
            self.ssh_connection = self.initialize_connection()

        sftp_client = self.ssh_client.open_sftp()
        # f = sftp_client.open(path)

        while True:
            f = sftp_client.open(path)
            try:
                df1 = pd.read_csv(f)
                print("!!!!! %s" % is_run_completed)

                if df1.shape[0] >= skip_rows:
                    f1 = sftp_client.open(path)
                    df = pd.read_csv(f1, skiprows=skip_rows, nrows=1, header=None, index_col=False)
                    print("!! %s" % df.values.tolist()[0])
                    f1.close()
                    break
                elif is_run_completed:
                    break
            except EmptyDataError:
                print("Found empty file : {file}".format(file=path))

            f.close()
            time.sleep(1)

        sftp_client.close()
        return df

    def execute_command(self, commands):
        if self.ssh_connection is None:
            print("!!!!!!   Enter run codriver")
            self.ssh_connection = self.initialize_connection()

        # transport = self.ssh_client.get_transport()
        # session = transport.open_session()
        # # session.set_combine_stderr(True)
        # session.get_pty()
        #stdin, stdout, stderr = session.exec_command(commands)
        stdin, stdout, stderr = self.ssh_client.exec_command(commands)
        exit_status = stdout.channel.recv_exit_status()  # Blocking call
        # if exit_status == 0:
        #     print("File Deleted")
        # else:
        #     print("Error", exit_status)
        #return session, exit_status

    def execute_commands_return_output(self, command):
        if self.ssh_connection is None:
            print("!!!!!!   Entered 1")
            self.ssh_connection = self.initialize_connection()
        output = ""
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        stdout = stdout.read().decode('ascii').strip("\n")
        #self.ssh_connection.close()
        for line in stdout:
            output = output + line
        #self.ssh_connection.close()
        return output

    def execute_commands_return_stdin(self, command):
        if self.ssh_connection is None:
            print("!!!!!!   Entered 1")
            self.ssh_connection = self.initialize_connection()
        output = ""
        stdin, stdout, stderr = self.ssh_client.exec_command(command)

        exit_status = stdout.channel.recv_exit_status()  # Blocking call
        if exit_status == 0:
            print("File Deleted")
        else:
            print("Error", exit_status)


        return output

    def copy_from_remote(self, path_file_remote, path_file_local):
        if self.ssh_connection is None:
            print("!!!!!!   Entered 2")
            self.ssh_connection = self.initialize_connection()
        print("!!!!!!   Entered 2 ssh_connection not none")
        self.scp_client.get(path_file_remote, path_file_local)

    def copy_to_remote(self, path_file_local, path_file_remote):
        if self.ssh_connection is None:
            print("!!!!!!   Entered 3")
            self.ssh_connection = self.initialize_connection()
        print("!!!!!!   Entered 3 ssh_connection not none")
        self.scp_client.put(path_file_local, path_file_remote)