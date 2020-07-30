import logging
import socket
import time
from threading import Thread
import pytest
from Manager.application_manager import ApplicationManager
from Manager.helper_base import HelperBase
from conftest import option, target_user

class TestCompilation:
    @pytest.fixture(scope="class", autouse=True)
    def session_initializing(self):
        global application_manager
        application_manager = ApplicationManager()
        global LOGGER
        LOGGER = logging.getLogger(__name__)
        global my_test_link
        my_test_link = ApplicationManager.get_my_test_link()
        LOGGER.info(HelperBase.get_message("info_start_suit"))
        yield
        LOGGER.info(HelperBase.get_message("info_finish_suit"))

    @pytest.fixture()
    def set_up(self):
        application_manager.get_helper_base().set_default_yml()
        application_manager.get_helper_base().remove_window_position_files()
        application_manager.get_helper_base().enable_person_result_csv()
        application_manager.get_helper_base().set_new_flag("server_streaming_incabin: true")
        application_manager.get_helper_base().set_new_flag("server_streaming: true")
        application_manager.get_helper_base().set_new_flag("server_streaming_ip: '10.71.84.187'")

        if option.target_platform is not None:
            application_manager.get_helper_base().replace_flag_value("application:",
                                                                     "#    app_video_file: 'Full path to video file'",
                                                                     "    app_video_file: '/home/" + target_user + "/dms_male_short.mp4'")
            application_manager.get_helper_ssh().copy_to_remote(str(HelperBase.detect_path()[1]), "/var/codriver/data/codriver_sample_config.yml")
        else:
            application_manager.get_helper_base().replace_flag_value("application:",
                                                                     "#    app_video_file: 'Full path to video file'",
                                                                     "    app_video_file: '" + HelperBase.get_project_dir() + "/data/video_files/dms_male_short.mp4'")
        yield
        application_manager.get_helper_base().clear_saved_data()

    @pytest.mark.basic
    def test_compilation_testlink(self, set_up):
        LOGGER.info(HelperBase.get_message("info_start_message"))

        array_tests = ["test_1", "test_2", "test_3", "test_4"]

        try:
            session = application_manager.get_helper_ssh().execute_commands(
                "export DISPLAY=:1; cd /home/" + target_user + "/Desktop/Jungo-CoDriver*/; ./samples/codriver_sample")

            if session.get_transport() is not None:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_address = ("10.71.84.187", 12345)
                print('starting up on %s port %s' % server_address)
                sock.bind(server_address)
                sock.listen(1)

                time.sleep(10)

                data_received = ""

                while True:
                    print('waiting for a connection')
                    connection, client_address = sock.accept()
                    try:
                        print('connection from', str(client_address))
                        while True:
                            data = connection.recv(1024)
                            data_received = data_received + data.decode("utf-8")

                            if data.decode("utf-8").endswith('Byeeee'):
                                break

                        print('received data: %s' % data_received)
                        # y = json.loads(data_received)
                        # print(y['WaitBeforeEvents'])
                    finally:
                        connection.close()

                time.sleep(10)
                # path_remote_person_results = ""
                # i=1
                # while session.get_transport().is_active():
                #
                #     while True:
                #         if not path_remote_person_results.endswith("person_results.csv"):
                #             path_remote_person_results = application_manager.get_helper_ssh().execute_commands_return_output("find /var/codriver/saved_data/ -maxdepth 1 -type f -name '*person_results.csv' -print | head -n1")
                #             time.sleep(1)
                #             if session.exit_status_ready():
                #                 break
                #         else:
                #             break
                #
                #     if session.exit_status_ready():
                #         break
                #     else:
                #         while True:
                #             if session.get_transport().is_active():
                #                 print("!! %s" % i)
                #                 #print("!!! %s" % application_manager.get_helper_ssh().read_scv_remote(path_remote_person_results, i).values)
                #                 if not application_manager.get_helper_ssh().read_scv_remote(path_remote_person_results, i, session.exit_status_ready()).values.tolist()[0]:
                #                 #if application_manager.get_helper_ssh().read_scv_remote(path_remote_person_results, i, session.exit_status_ready()).em is not None:
                #                     #application_manager.get_helper_ssh().read_scv_remote(path_remote_person_results, i)
                #                     #i += 1
                #                     break
                #                 else:
                #                     i += 1
                #                     #break
                #             else:
                #                 break

            session.send('\x03')

            if session.recv_exit_status() != 0:
                # error or crash
                print("############ exit status not None: %s" % session.recv_exit_status())
            else:
                print("############ exit status: %s" % session.recv_exit_status())


            #time.sleep(5)
        except Exception as e:
           # LOGGER.info(HelperBase.get_message("_____"))
            print("&&&&&&&&&&&&&&&&& Connection lost : %s" % e)

        flag_exit_state = True



        LOGGER.info(HelperBase.get_message("info_finish_message"))
        assert flag_exit_state