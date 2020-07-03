from locust import HttpUser,SequentialTaskSet,task, between
from random import randrange
import json
import csv
import sys, logging

#constants
email_password = []
#mocktest_bundle_path= "/mock-test/jee-main/full-test/predicted-jee-main-2019-april"
mocktest_bundle_path= "/mock-test/jee-main/mini-test/mini-test"
host = "https://preprodms.embibe.com"


#functions
with open('email_password_embibe.csv', 'r') as csvfile:
        email_password = list (csv.reader(csvfile, delimiter=','))


#Payload Values       
body = {}

class UserBehaviour(SequentialTaskSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    #Declarations
        self.headers = {
            'Connection':'keep-alive',
            'Accept':'application/json, text/plain, */*',
            'Content-Type':'application/json;charset=UTF-8',
        }
        self.starttime=None
        self.sessionid=None               

    # @task
    # def login(self):
        # rnum = randrange(len(email_password)-1)
       
        # login_data={
                    # "login":email_password[rnum][0],
                    # "password":email_password[rnum][1],
                    # "password_confirmation":email_password[rnum][1]
                   # }
        # response = self.client.post('/user_ms/auth/sign_in', data=json.dumps(login_data), name="login",headers=self.headers)
           
        # #logging.info('Response for Checkuserexists API is %s',response.headers)
        # headers ['embibe-token']= response.headers['embibe-token']
        
    # Revised Login API
    
    @task
    def login(self):
        rnum = randrange(len(email_password)-1)
       
        login_data={
                    "login":email_password[rnum][0],
                    "password":email_password[rnum][1]
                   }
        response = self.client.post('/user_auth/auth/sign_in', data=json.dumps(login_data), name="login",headers=self.headers)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(response.content)
            print(response.headers)
            print("------------------------------------------------------------------------------------------------------")
                              
        #logging.info('Response for login API is %s',response.content)
        self.headers ['embibe-token']= response.headers['embibe-token']
     

    # @task
    # def TestSelection(self):
      
    #     response = self.client.get(url = "/content_ms/v2/mocktest-bundles/get-latest-version-meta?mocktest_bundle_path="+ mocktest_bundle_path,
    #     name="TestSelection",headers=self.headers, data = body)
        
    #     if (response.status_code != 200):
    #         print(response.request.headers)
    #         print(response.headers)
    #         print(f"TestSelection -{host}/content_ms/v2/mocktest-bundles/get-latest-version-meta?mocktest_bundle_path=/mock-test/jee-main/full-test/predicted-jee-main-2019-april")
    #         print(response.content)
    #         print("------------------------------------------------------------------------------------------------------")
                    
    #     #logging.info('Response for TestSelection API is %s',response.content)
        
    @task
    def StartTest(self):  
        
        response = self.client.get(url = "/testsubmission_ms_lt/now", headers=self.headers, name="StartTest",data = body)

        
        self.starttime = "".join(chr(x) for x in response.content)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(response.headers)
            print(f"StartTest -{host}/testsubmission_ms_lt/now")
            print(response.content)
            print("------------------------------------------------------------------------------------------------------")
        
        #logging.info('Response for StartTest API is %s',response.content)
        
    @task
    def TestWindow(self):    
    
        response = self.client.get(url = "/testsubmission_ms_lt/v1/test/mb118/session", headers=self.headers,name="TestWindow", data = body)
        self.headers ['browser-id']= '1588163045400.5'
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(response.headers)
            print(f"TestWindow -{host}/testsubmission_ms_lt/v1/test/mb118/session")
            print(response.content)
            print("------------------------------------------------------------------------------------------------------")
        
        #logging.info('Response for TestWindow API is %s',response.content)
    
    @task
    def TestSession(self):    
        
        TestSession_data = '{"mocktest_session":{"goal_code":"engineering","t_started":'+self.starttime+'}}'
        
        response = self.client.post(url = "/testsubmission_ms_lt/v1/test/mb118/session", headers=self.headers,name="TestSession", data = TestSession_data)
        
       
        self.sessionid = response.json().get("id","")
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(response.headers)
            print(f"TestSession -{host}/testsubmission_ms_lt/v1/test/mb118/session")
            print(response.content)
            print("------------------------------------------------------------------------------------------------------")
        
        #logging.info('Response for TestSession API is %s',response.content)
        
    @task
    def TestAnswer(self):
            
        TestAnswer_data= "[{\"eorder\":1,\"event_type\":\"load_paper\",\"sequence\":\"\",\"sent\":false,\"section\":\"\",\"event_info\":\"\",\"t\":1588163054.363,\"question_code\":\"\"},{\"eorder\":2,\"event_type\":\"view_question\",\"sequence\":1,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"\",\"t\":1588163054.769,\"question_code\":\"EM0076224\"},{\"eorder\":3,\"event_type\":\"select_answer\",\"sequence\":1,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0076224-b\",\"t\":1588163060.747,\"question_code\":\"EM0076224\"},{\"eorder\":4,\"event_type\":\"save_attempt\",\"sequence\":1,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0076224-b\",\"t\":1588163062.573,\"question_code\":\"EM0076224\"},{\"eorder\":5,\"event_type\":\"view_question\",\"sequence\":2,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"\",\"t\":1588163062.574,\"question_code\":\"EM0079578\"},{\"eorder\":6,\"event_type\":\"select_answer\",\"sequence\":2,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0079578-d\",\"t\":1588163063.3915,\"question_code\":\"EM0079578\"},{\"eorder\":7,\"event_type\":\"save_attempt\",\"sequence\":2,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0079578-d\",\"t\":1588163064.1645,\"question_code\":\"EM0079578\"},{\"eorder\":8,\"event_type\":\"view_question\",\"sequence\":3,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"\",\"t\":1588163064.1665,\"question_code\":\"EM0017239\"},{\"eorder\":9,\"event_type\":\"select_answer\",\"sequence\":3,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0017239-d\",\"t\":1588163064.8975,\"question_code\":\"EM0017239\"},{\"eorder\":10,\"event_type\":\"save_attempt\",\"sequence\":3,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0017239-d\",\"t\":1588163065.4985,\"question_code\":\"EM0017239\"},{\"eorder\":11,\"event_type\":\"view_question\",\"sequence\":4,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"\",\"t\":1588163065.5005,\"question_code\":\"EM0131889\"},{\"eorder\":12,\"event_type\":\"select_answer\",\"sequence\":4,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0131889-c\",\"t\":1588163066.0635,\"question_code\":\"EM0131889\"},{\"eorder\":13,\"event_type\":\"save_attempt\",\"sequence\":4,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0131889-c\",\"t\":1588163066.6655,\"question_code\":\"EM0131889\"},{\"eorder\":14,\"event_type\":\"view_question\",\"sequence\":5,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"\",\"t\":1588163066.6665,\"question_code\":\"EM0040436\"},{\"eorder\":15,\"event_type\":\"select_answer\",\"sequence\":5,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0040436-d\",\"t\":1588163067.1775,\"question_code\":\"EM0040436\"},{\"eorder\":16,\"event_type\":\"save_attempt\",\"sequence\":5,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0040436-d\",\"t\":1588163067.6725,\"question_code\":\"EM0040436\"},{\"eorder\":17,\"event_type\":\"view_question\",\"sequence\":6,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"\",\"t\":1588163067.6745,\"question_code\":\"EM0006429\"},{\"eorder\":18,\"event_type\":\"select_answer\",\"sequence\":6,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0006429-c\",\"t\":1588163068.2625,\"question_code\":\"EM0006429\"},{\"eorder\":19,\"event_type\":\"save_attempt\",\"sequence\":6,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"EM0006429-c\",\"t\":1588163068.9175,\"question_code\":\"EM0006429\"},{\"eorder\":20,\"event_type\":\"view_question\",\"sequence\":7,\"sent\":false,\"section\":\"ms41\",\"event_info\":\"\",\"t\":1588163068.9195,\"question_code\":\"EM0016877\"}]"
        
        response = self.client.post(url = f"/testsubmission_ms_lt/v1/test/{self.sessionid}/events", headers=self.headers,name="TestAnswer", data = TestAnswer_data)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(response.headers)
            print(f"TestAnswer -{host}/testsubmission_ms_lt/v1/test/{self.sessionid}/events")
            print(response.content)
            print("------------------------------------------------------------------------------------------------------")
            
        #logging.info('Response for TestAnswer API is %s',response.content)
        
    # @task
    # def TestResume(self):   
    
    #     response = self.client.post(url = "/testsubmission_ms_lt/v1/test/mb118/resume", headers=self.headers,name="TestResume", data = body)
        
    #     if (response.status_code != 200):
    #         print(response.request.headers)
    #         print(response.headers)
    #         print(f"TestResume -{host}/testsubmission_ms_lt/v1/test/mb118/resume")
    #         print(response.content)
    #         print("------------------------------------------------------------------------------------------------------")
            
    #     #logging.info('Response for TestResume API is %s',response.content)
        
    # @task
    # def TestCheck(self):
    
    #     response = self.client.get(url = "/testsubmission_ms_lt/v1/test/mb118/check", headers=self.headers,name="TestCheck", data = body)
        
    #     if (response.status_code != 200):
    #         print(response.request.headers)
    #         print(response.headers)
    #         print(f"TestCheck -{host}/testsubmission_ms_lt/v1/test/mb118/check")
    #         print(response.content)
    #         print("------------------------------------------------------------------------------------------------------")
            
    #     #logging.info('Response for TestCheck API is %s',response.content)
        
    @task
    def TestEvent(self):
    
        TestEvent_data = "[{\"eorder\":6,\"event_type\":\"user_active\",\"sequence\":\"\",\"sent\":false,\"section\":\"\",\"event_info\":\"\",\"t\":1588430261.484,\"question_code\":\"\"},{\"eorder\":7,\"event_type\":\"select_answer\",\"sequence\":1,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"EM0131893-b\",\"t\":1588430262.243,\"question_code\":\"EM0131893\"},{\"eorder\":8,\"event_type\":\"save_attempt\",\"sequence\":1,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"EM0131893-b\",\"t\":1588430264.2805,\"question_code\":\"EM0131893\"},{\"eorder\":9,\"event_type\":\"view_question\",\"sequence\":2,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"\",\"t\":1588430264.2815,\"question_code\":\"EM0132079\"},{\"eorder\":10,\"event_type\":\"select_answer\",\"sequence\":2,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"EM0132079-d\",\"t\":1588430265.8865,\"question_code\":\"EM0132079\"},{\"eorder\":11,\"event_type\":\"save_attempt\",\"sequence\":2,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"EM0132079-d\",\"t\":1588430267.7745,\"question_code\":\"EM0132079\"},{\"eorder\":12,\"event_type\":\"view_question\",\"sequence\":3,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"\",\"t\":1588430267.7755,\"question_code\":\"EM0017321\"},{\"eorder\":13,\"event_type\":\"select_answer\",\"sequence\":3,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"EM0017321-b\",\"t\":1588430268.8505,\"question_code\":\"EM0017321\"},{\"eorder\":14,\"event_type\":\"save_attempt\",\"sequence\":3,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"EM0017321-b\",\"t\":1588430269.8185,\"question_code\":\"EM0017321\"},{\"eorder\":15,\"event_type\":\"view_question\",\"sequence\":4,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"\",\"t\":1588430269.8195,\"question_code\":\"EM0132187\"}]"
        
        response = self.client.post(url = f"/testsubmission_ms_lt/v1/test/{self.sessionid}/events", headers=self.headers,name="TestEvent", data = TestEvent_data)

        if (response.status_code != 200):
            print(response.request.headers)
            print(response.headers)
            print(f"TestEvent -{host}/testsubmission_ms_lt/v1/test/{self.sessionid}/events")
            print(response.content)
            print("------------------------------------------------------------------------------------------------------")
            
        #logging.info('Response for TestEvent API is %s',response.content)
        
    @task
    def TestEvent1(self):
    
        TestEvent1_data = "[{\"eorder\":19,\"event_type\":\"save_attempt\",\"sequence\":5,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"\",\"t\":1588430294.1555,\"question_code\":\"EM0131900\"},{\"eorder\":20,\"event_type\":\"view_question\",\"sequence\":6,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"\",\"t\":1588430294.1565,\"question_code\":\"EM0016143\"},{\"eorder\":21,\"event_type\":\"select_answer\",\"sequence\":6,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"EM0016143-c\",\"t\":1588430295.1745,\"question_code\":\"EM0016143\"},{\"eorder\":22,\"event_type\":\"save_attempt\",\"sequence\":6,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"EM0016143-c\",\"t\":1588430296.1545,\"question_code\":\"EM0016143\"},{\"eorder\":23,\"event_type\":\"view_question\",\"sequence\":7,\"sent\":false,\"section\":\"ms1255\",\"event_info\":\"\",\"t\":1588430296.1545,\"question_code\":\"EM0131903\"}]"
        response = self.client.post(url = f"/testsubmission_ms_lt/v1/test/{self.sessionid}/events", headers=self.headers,name="TestEvent1", data = TestEvent1_data)
        
        if (response.status_code != 200):
            print(response.request.headers)
            print(response.headers)
            print(f"TestEvent1 -{host}/testsubmission_ms_lt/v1/test/{self.sessionid}/events")
            print(response.content)
            print("------------------------------------------------------------------------------------------------------")
            
        #logging.info('Response for TestEvent1 API is %s',response.content)
        
    @task
    def TestEventFreeze(self):
    
        TestEventFreeze_data = "[{\"eorder\":24,\"event_type\":\"freeze\",\"sequence\":\"\",\"sent\":false,\"section\":\"\",\"event_info\":\"\",\"t\":1588430329.112,\"question_code\":\"\"}]"
        response = self.client.post(url = f"/testsubmission_ms_lt/v1/test/{self.sessionid}/events", headers=self.headers,name="TestEventFreeze", data = TestEventFreeze_data)

        if (response.status_code != 200):
            print(response.request.headers)
            print(response.headers)
            print(f"TestEventFreeze -{host}/testsubmission_ms_lt/v1/test/{self.sessionid}/events")
            print(response.content)
            print("------------------------------------------------------------------------------------------------------")
            
        #logging.info('Response for TestEventFreeze API is %s',response.content)
     
class WebsiteTest(HttpUser):
    tasks = [UserBehaviour]
    wait_time = between(2, 5)
    host = "https://preprodms.embibe.com"
        

               
              
        

