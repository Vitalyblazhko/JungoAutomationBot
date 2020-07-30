import mimetypes
import os
import platform
import smtplib

import email_conf
#from Manager.helper_base import HelperBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.audio import MIMEAudio
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
import mimetypes
from email import encoders
import distro

class EmailReport:

    def __init__(self):
        self.smtp_ssl_host = email_conf.smtp_ssl_host
        self.smtp_ssl_port = email_conf.smtp_ssl_port
        self.username = email_conf.username
        self.password = email_conf.app_password
        self.sender = email_conf.sender
        self.targets = email_conf.targets
        global os_version
        global os_platform
        os_platform = platform.system()
        if os_platform == "Linux":
            os_version = distro.linux_distribution(full_distribution_name=False)[0] + \
                         distro.linux_distribution(full_distribution_name=False)[1]
        elif os_platform == "Windows":
            os_version = os_platform + platform.release()


    def get_test_report_data(self,html_body_flag= True,report_file_path= 'default'):
        from Manager.helper_base import HelperBase
        if html_body_flag == True and report_file_path == 'default':
            test_report_file = HelperBase.get_project_dir()+"/outputs/reports/report_"+os_version+".html"
        elif html_body_flag == False and report_file_path == 'default':
            test_report_file = HelperBase.get_project_dir()+"/outputs/reports/report_"+os_version+".html"
        else:
            test_report_file = report_file_path
        if not os.path.exists(test_report_file):
            raise Exception("File '%s' does not exist. Please provide valid file"%test_report_file)

        with open(test_report_file, "r") as in_file:
            testdata = ""
            for line in in_file:
                testdata = testdata + '\n' + line
        return testdata

    def get_attachment(self,attachment_file_path = 'default'):
        from Manager.helper_base import HelperBase
        if attachment_file_path == 'default':
            #attachment_report_file = HelperBase.get_project_dir()+"/outputs/reports/report_"+platform+".html"
            attachment_report_file = HelperBase.get_project_dir()+"/outputs/reports/report_"+os_version+".html"
        else:
            attachment_report_file = attachment_file_path
        if not os.path.exists(attachment_report_file):
            raise Exception("File '%s' does not exist. Please provide valid file"%attachment_report_file)

        ctype, encoding = mimetypes.guess_type(attachment_report_file)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'

        maintype, subtype = ctype.split('/', 1)
        if maintype == 'text':
            fp = open(attachment_report_file)
            attachment = MIMEText(fp.read(), subtype)
            fp.close()
        elif maintype == 'image':
            fp = open(attachment_report_file, 'rb')
            attachment = MIMEImage(fp.read(), subtype)
            fp.close()
        elif maintype == 'audio':
            fp = open(attachment_report_file, 'rb')
            attachment = MIMEAudio(fp.read(), subtype)
            fp.close()
        else:
            fp = open(attachment_report_file, 'rb')
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
        attachment.add_header('Content-Disposition',
                   'attachment',
                   filename=os.path.basename(attachment_report_file))
        return attachment

    def send_test_report_email(self,html_body_flag = True,attachment_flag = False,report_file_path = 'default'):
        from Manager.helper_base import HelperBase
        if html_body_flag == True and attachment_flag == False:
            testdata = self.get_test_report_data(html_body_flag,report_file_path)
            message = MIMEText(testdata,"html")

        elif html_body_flag == False and attachment_flag == False:
            testdata = self.get_test_report_data(html_body_flag,report_file_path)
            message  = MIMEText(testdata)

        elif html_body_flag == True and attachment_flag == True:
            message = MIMEMultipart()
            html_body = MIMEText('''<p>Hello,</p>
                                     <p>&nbsp; &nbsp; &nbsp; &nbsp; Please check the attachments to see test built report and log file.</p>
                                     <p><strong>Note: For best UI experience, download the built report and open using Chrome browser.</strong></p>
                                 ''',"html")
            message.attach(html_body)
            attachment = self.get_attachment(report_file_path)
            attachment_log = self.get_attachment(HelperBase.get_project_dir()+"/Tests/jungo_bot.log")
            message.attach(attachment)
            message.attach(attachment_log)
        else:
            message = MIMEMultipart()
            plain_text_body = MIMEText('''Hello,\n\tPlease check the attachments to see test built report and log file.
                                       \n\nNote: For best UI experience, download the built report and open using Chrome browser.''')
            message.attach(plain_text_body)
            attachment = self.get_attachment(report_file_path)
            attachment_log = self.get_attachment(HelperBase.get_project_dir() + "/Tests/jungo_bot.log")
            message.attach(attachment)
            message.attach(attachment_log)

        message['From'] = self.sender
        message['To'] = ', '.join(self.targets)
        message['Subject'] = 'Script generated test report'

        server = smtplib.SMTP_SSL(self.smtp_ssl_host, self.smtp_ssl_port)
        server.login(self.username, self.password)
        server.sendmail(self.sender, self.targets, message.as_string())
        server.quit()