import requests
import execjs
from bs4 import BeautifulSoup as BS
import re

requests.packages.urllib3.disable_warnings()

def login(user, password):
    session = requests.Session()
    login_url = "http://cas.upc.edu.cn/cas/login"
    response = session.get(url=login_url)
    soup = BS(response.content,'lxml')
    LT = re.findall('value="(.*?)"/',str(soup.find_all('input',id="lt")[0]))[0]
    execution = re.findall('value="(.*?)"/',str(soup.find_all('input',attrs={'name': "execution"})[0]))[0]
    _eventId = re.findall('value="(.*?)"/',str(soup.find_all('input',attrs={'name': "_eventId"})[0]))[0]

    des = execjs.compile(open("./des.js").read())
    rsa = des.call("strEnc",user+password+LT,"1","2","3")

    data = {
        "rsa": rsa,
        "ul": len(user),
        "pl": len(password),
        "lt": LT,
        "execution": execution,
        "_eventId": _eventId
    }
    response = session.post(url=login_url,data=data,verify=False)
    if response.status_code == 200 :
        print("登陆成功")
        return session
    else: print("登陆失败")