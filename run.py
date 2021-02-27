import requests
import requests
from bs4 import BeautifulSoup

def initialize(s):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    response = s.get('https://ksa.hs.kr/Account/Login', headers=headers)

def get_login_token(s):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://www.ksa.hs.kr/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    response = s.get('https://www.ksa.hs.kr/Account/Login', headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    result = soup.find_all('input', {"name":"__RequestVerificationToken"})[-1]["value"]

    return result


def make_data(login_token,id,password):
    return f'''-----------------------------325333128821718686562724141506
Content-Disposition: form-data; name="__RequestVerificationToken"

{login_token}
-----------------------------325333128821718686562724141506
Content-Disposition: form-data; name="UserId"

{str(id)}
-----------------------------325333128821718686562724141506
Content-Disposition: form-data; name="Password"

{str(password)}
-----------------------------325333128821718686562724141506
Content-Disposition: form-data; name="UserType"

학생
-----------------------------325333128821718686562724141506--
'''

def login(s,login_token,id,password):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'multipart/form-data; boundary=---------------------------325333128821718686562724141506',
        'Origin': 'https://ksa.hs.kr',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Referer': 'https://ksa.hs.kr/Account/Login',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    response = s.post('https://ksa.hs.kr/Account/Login', data = make_data(login_token,id,password).encode("utf-8"), headers=headers)

    # print(response.cookies)

    # print(response.text)

def get_check_token(s):

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
        'Referer': 'https://www.ksa.hs.kr/',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    response = s.get('https://www.ksa.hs.kr/SelfHealthCheck/Index/200', headers=headers)

    soup = BeautifulSoup(response.text, 'html.parser')

    result = soup.find_all('input', {"name":"__RequestVerificationToken"})[-1]["value"]

    return result

def check(s,check_token,okay):

    okay_data = {
    '__RequestVerificationToken': check_token,
    'SelfCheckItemDatas[0].Order': '1',
    'SelfCheckItemDatas[1].Order': '2',
    'SelfCheckItemDatas[2].Order': '3',
    'survey_q1': 'False',
    'SelfCheckItemDatas[0].CheckResultValues[0]': '0',
    'survey_q2': 'False',
    'SelfCheckItemDatas[1].CheckResultValues[0]': '0',
    'survey_q3': 'False',
    'SelfCheckItemDatas[2].CheckResultValues[0]': '0'
    }

    not_okay_data = {
    '__RequestVerificationToken': check_token,
    'SelfCheckItemDatas[0].Order': '1',
    'SelfCheckItemDatas[1].Order': '2',
    'SelfCheckItemDatas[2].Order': '3',
    'survey_q1': 'True',
    'SelfCheckItemDatas[0].CheckResultValues[0]': '1',
    'survey_q2': 'True',
    'SelfCheckItemDatas[1].CheckResultValues[0]': '1',
    'survey_q3': 'True',
    'SelfCheckItemDatas[2].CheckResultValues[0]': '1'
    }

    if okay:
        data = okay_data
    elif not okay:
        data = not_okay_data

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
        'Accept': '*/*',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://www.ksa.hs.kr',
        'Connection': 'keep-alive',
        'Referer': 'https://www.ksa.hs.kr/SelfHealthCheck/Index/200',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }

    response = s.post('https://www.ksa.hs.kr/SelfHealthCheck/index/200', headers=headers, data=data)
    return response.json()


def run(id,password):

    with requests.Session() as s:
        initialize(s)
        login_token = get_login_token(s)
        login(s,login_token,id,password)
        check_token = get_check_token(s)
        result = check(s, check_token, True)
    return result
