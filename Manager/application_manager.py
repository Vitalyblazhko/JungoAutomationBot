import getpass
import os
import platform
import subprocess
import sys
import time
import psutil
from testlink import TestLinkHelper, TestlinkAPIGeneric
from Manager.helper_base import HelperBase
from Manager.helper_ssh import HelperSsh

class ApplicationManager:

    def __init__(self):
        global platform_name
        platform_name = platform.system()

        global user_name
        user_name = getpass.getuser()

        self.helper_base = HelperBase()
        self.helper_ssh = HelperSsh()

        global TESTLINK_API_PYTHON_SERVER_URL
        TESTLINK_API_PYTHON_SERVER_URL = 'http://st-testlink/testlink/lib/api/xmlrpc/v1/xmlrpc.php'

    @staticmethod
    def get_testlink_api_python_devkey(user_name):
        if user_name == "vitalyb":
            return "52efcc0741dc68952bd6697ff9ce4567"
        elif user_name == "robertl":
            pass
        elif user_name == "alinab":
            pass
        elif user_name == "maxs":
            pass
        elif user_name == "katerynad":
            pass

    @staticmethod
    def get_testlink_delails(testlink_project, testlink_plan, testlink_build, testlink_platform):
        return

    @staticmethod
    def get_my_test_link():
        return TestLinkHelper(TESTLINK_API_PYTHON_SERVER_URL,
                              ApplicationManager.get_testlink_api_python_devkey(user_name)).connect(TestlinkAPIGeneric)

    def run_codriver_sample(self, returncode):
        path_to_execudable = None
        if platform_name == "Linux":
            path_to_execudable = self.get_helper_base().get_path_to_codriver_directory_linux() + "/samples/codriver_sample"
        elif platform_name == "Windows":
            pass
        p = subprocess.run(path_to_execudable, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            time.sleep(5)
        except:
            pass

        if returncode:
            return p.returncode
        else:
            pass

    @staticmethod
    def run_make_codriver_sample():
        path_to_execudable = None
        if platform_name == "Linux":
            path_to_execudable = HelperBase.get_path_to_codriver_directory_linux() + "/samples/"
        elif platform_name == "Windows":
            pass
        return subprocess.Popen(["make", "codriver_sample"], stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                                cwd=path_to_execudable)

    def run_codriver_sample_write_stdout(self):
        path_to_execudable = None
        if platform_name == "Linux":
            path_to_execudable = self.get_helper_base().get_path_to_codriver_directory_linux() + "/samples/codriver_sample"
        elif platform_name == "Windows":
            pass
        k = open(HelperBase.create_test_dir("output") + "/sdt_out.txt", "w")
        subprocess.run(path_to_execudable, stdin=subprocess.PIPE, stdout=k, stderr=subprocess.PIPE)
        return k

    def run_codriver_sample_return_process(self):
        path_to_execudable = None
        if platform_name == "Linux":
            path_to_execudable = self.get_helper_base().get_path_to_codriver_directory_linux() + "/samples/codriver_sample"
        elif platform_name == "Windows":
            pass
        return subprocess.Popen(path_to_execudable, stdout=subprocess.PIPE)

    # def maximize_incabin_window(self):
    #     title_menu_incabin = None
    #     title_menu_maximize_incabin = None
    #
    #     if platform_name == "Linux":
    #         title_menu_incabin = HelperBase.get_project_dir() +  "/data/images/initializing/linux/title_menu_incabin.png"
    #         title_menu_maximize_incabin = HelperBase.get_project_dir() + "/data/images/initializing/linux/title_menu_maximize_incabin.png"
    #     elif platform_name == "Windows":
    #         pass
    #
    #     while True:
    #         if pyautogui.locateOnScreen(title_menu_incabin, confidence=0.7) != None:
    #             pyautogui.click(pyautogui.locateCenterOnScreen(title_menu_maximize_incabin))
    #             break
    #         else:
    #             time.sleep(0.1)

    @staticmethod
    def get_project_dir():
        TEST_DIR = os.path.dirname(os.path.abspath(__file__))
        PROJECT_DIR = os.path.abspath(os.path.join(TEST_DIR, os.pardir))
        sys.path.insert(0, PROJECT_DIR)
        return PROJECT_DIR

    @staticmethod
    def check_if_process_running(process_name):
        for proc in psutil.process_iter():
            try:
                if process_name.lower() in proc.name().lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def get_helper_base(self):
        return self.helper_base

    def get_helper_ssh(self):
        return self.helper_ssh
