import platform
from pathlib import Path
import distro
import pytest

option = None
target_platform = None
target_user = None
application_manager1 = None
from Manager.helper_email_report import EmailReport

@pytest.fixture(scope="class", autouse=True)
def set_up_session(request):
    from Manager.helper_base import HelperBase
    from Manager.application_manager import ApplicationManager
    application_manager = ApplicationManager()

    if request.config.getoption("--target_platform") is not None:
        path_test_directory = HelperBase.create_test_directory(request.config.getoption("--target_platform"))
        path_remote_distribution = application_manager.get_helper_ssh().execute_commands_return_output("find /home/`whoami`/Desktop/ -maxdepth 1 -type d -name 'Jungo-CoDriver-*' -print | head -n1")
        application_manager.get_helper_ssh().copy_from_remote(str(path_remote_distribution)+"/data/codriver_sample_config.yml", path_test_directory)
        # copy video files to platform
        application_manager.get_helper_ssh().copy_to_remote(str(HelperBase.get_project_dir()) + "/data/video_files/dms_male_short.mp4", "/home/"+str(request.config.getoption("--target_user"))+"/dms_male_short.mp4")
    yield
    application_manager.get_helper_ssh().disconnect()

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    os_platform = platform.system()
    global os_version

    if os_platform == "Linux":
        os_version = distro.linux_distribution(full_distribution_name=False)[0] + \
                     distro.linux_distribution(full_distribution_name=False)[1]
    elif os_platform == "Windows":
        os_version = os_platform + platform.release()

    global option
    option = config.option
    global target_platform
    target_platform = option.target_platform
    global target_user
    target_user = option.target_user

    from Manager.helper_base import HelperBase

    config._links = None
    if not config.option.htmlpath:
        reports_dir = Path(HelperBase.get_project_dir()+"/outputs/", "reports")
        reports_dir.mkdir(parents=True, exist_ok=True)
        report = str(reports_dir)+"/"+ f"report_"+str(os_version)+".html"
        config.option.htmlpath = report
        config.option.self_contained_html = True

def pytest_html_results_table_header(cells):
    cells.pop()

def pytest_html_results_table_row(report, cells):
    cells.pop()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)

@pytest.fixture
def email_pytest_report(request):
    return request.config.getoption("--email_pytest_report")

def pytest_addoption(parser):
    parser.addoption("--email_pytest_report",
                     dest="email_pytest_report",
                     help="Email pytest report: Y or N",
                     default="N")
    parser.addoption("--target_platform", action="store",
                     default=None)
    parser.addoption("--testlink_project", action="store",
                     default=None)
    parser.addoption("--testlink_plan", action="store",
                     default=None)
    parser.addoption("--testlink_build", action="store",
                     default=None)
    parser.addoption("--testlink_platform", action="store",
                     default=None)
    parser.addoption("--target_host", action="store",
                     default=None)
    parser.addoption("--target_user", action="store",
                     default=None)
    parser.addoption("--target_password", action="store",
                     default=None)

def pytest_terminal_summary(terminalreporter):
    if terminalreporter.config.getoption("--email_pytest_report").lower() == 'y':
        email_obj = EmailReport()
        email_obj.send_test_report_email(html_body_flag=True, attachment_flag=True, report_file_path='default')