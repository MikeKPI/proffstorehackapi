
import requests
import json


def Access_token( mail , pas):


     # return text["access_token"]
    url = 'https://proffstore.com/api/v1/token'
    client_code = "a34f65b2c464"
    payload = {"email": mail , "pass": pas }
    headers = {'Content-Type':'application/json', 'x-client-code':client_code }
    r = requests.post(url, headers=headers , data= json.dumps(payload))
    print( r.json()["access_token"] )
    return r.json()["access_token"]


def to_do_task( access_token ):

    url = 'https://proffstore.com/api/v1/user/tasks'
    client_code = "a34f65b2c464"
    #Access_Token = {"x-access-token": access_token }
    headers = {'Content-Type':'application/json', 'x-client-code':client_code ,"x-access-token": access_token }
    r = requests.get(url, headers=headers )
    print( r.json())

def order_task( access_token ):

    url = 'https://proffstore.com/api/v1/user/projects'
    client_code = "a34f65b2c464"
    #Access_Token = {"x-access-token": access_token }
    headers = {'Content-Type':'application/json', 'x-client-code':client_code ,"x-access-token": access_token }
    r = requests.get(url, headers=headers )
    print( r.json())



print ("1.Access_token")
ACCESS_TOKEN = Access_token("mrkiril@ukr.net","123ss456")
print ("2. to_do_task")
order_task(ACCESS_TOKEN)
