# response = my_test_link.getTestProjectByName("CoDriver_test")
        # print("!!!!!!! getTestProjectByName" + str(response))
        #
        # response = my_test_link.getProjectTestPlans(my_test_link.getTestProjectByName("CoDriver_test")['id'])
        # print("$$$$$$$ getProjectTestPlans", response)
        #
        # response = my_test_link.getTestCasesForTestPlan("33857")
        # print("^^^^^^ getTestCasesForTestPlan A failed ", response)
        #
        # response = my_test_link.getBuildsForTestPlan("33857")
        # print("%%%%%% getBuildsForTestPlan", response)
        #
        # response = my_test_link.getTestPlanByName(option.testlink_project, option.testlink_plan)
        # print("@@@@@@@@@ getTestPlanByName", response)
        #
        # response = my_test_link.getTestPlanByName(option.testlink_project, option.testlink_plan)[0]['id']
        # print("&&&&&&&& getTestPlanByName", response)

# if p.wait() != 0:
        #     flag_exit_state = False
        #     LOGGER.critical(HelperBase.get_message("failed_condition: Returned " + str(p.returncode) + " code"))
        #     if option.testlink_project is not None \
        #         and option.testlink_plan is not None \
        #         and option.testlink_build is not None \
        #         and option.testlink_platform is not None:
        #         my_test_link.reportTCResult(testcaseexternalid="CDT-1772", testplanid=my_test_link.getTestPlanByName(option.testlink_project, option.testlink_plan)[0]['id'], buildname=option.testlink_build,
        #                                     status='f', platformname=option.testlink_platform)
        #
        # else:
        #     pass
        #     if option.testlink_project is not None \
        #             and option.testlink_plan is not None \
        #             and option.testlink_build is not None \
        #             and option.testlink_platform is not None:
        #         my_test_link.reportTCResult(testcaseexternalid="CDT-1772", testplanid=my_test_link.getTestPlanByName(option.testlink_project, option.testlink_plan)[0]['id'], buildname=option.testlink_build,
        #                                     status='p', platformname=option.testlink_platform)
import socket
import time

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ("10.71.84.187", 12345)
print('starting up on %s port %s' % server_address)
sock.bind(server_address)
sock.listen(1)

time.sleep(10)
data_received = ''

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
        #y = json.loads(data_received)
        #print(y['WaitBeforeEvents'])
    finally:
        connection.close()