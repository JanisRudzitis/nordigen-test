import webbrowser
import requests
import json


def getaccesstoken():
    url = 'https://sandbox.handelsbanken.com/openbanking/oauth2/token/1.0'

    body = "client_id=c01c36a1-59f1-44c3-9589-7870c0201846&grant_type=client_credentials&scope=AIS"

    headers = {
        'Accept': "application/json",
        'Content-Type': "application/x-www-form-urlencoded",
        }

    response = requests.post(url, data=body, headers=headers,)

    access_token = (json.loads(response.text)['access_token'])

    return access_token


def getconsent():
    url = 'https://sandbox.handelsbanken.com/openbanking/psd2/v1/consents'

    body = "{\"access\":\"ALL_ACCOUNTS\"}"

    headers = {
        'X-IBM-Client-Id': "c01c36a1-59f1-44c3-9589-7870c0201846",
        'Authorization': "Bearer " + getaccesstoken(),
        'Country': "SE",
        'PSU-IP-Address': "192.102.28.2",
        'TPP-Transaction-ID': "6b24ce42-237f-4303-a917-cf778e5013d6",
        'TPP-Request-ID': "c8271b81-4229-5a1f-bf9c-758f11c1f5b1",
        'content-type': "application/json",
        'accept': "application/json"
    }

    response = requests.post(url, data=body, headers=headers,)

    consent = (json.loads(response.text)['consentId'])
    return consent


def getinitauthorization():
    url = f'https://sandbox.handelsbanken.com/openbanking/redirect/oauth2/authorize/1.0?response_type=code&scope=AIS:{getconsent()}&client_id=c01c36a1-59f1-44c3-9589-7870c0201846&state=bc4b933c-bfc2-44c8-b858-eba90f559f91&redirect_uri=http://localapp.me/redirect/result'

    headers = {'accept': "application/json"}

    response = requests.get(url, headers=headers)
    webbrowser.open(response.url)




def requestgranttoken():
    url = 'https://sandbox.handelsbanken.com/openbanking/redirect/oauth2/token/1.0'

    body = {
        'grant_type': "authorization_code",
        'scope': "AIS:" + getconsent(),
        'client_id': "c01c36a1-59f1-44c3-9589-7870c0201846",
        'code': "360ad5ce-ecfe-4ad4-83d1-9254e89a3ccc",
        'redirect_uri': "http://localapp.me/redirect/result"
    }

    headers = {
        'Accept': "application/json",
        'Content-Type': "application/x-www-form-urlencoded",
    }

    response = requests.post(url, data=body, headers=headers,)

    account_access_token = (json.loads(response.text)['access_token'])
    account_refresh_token = (json.loads(response.text)['refresh_token'])

    return account_access_token, account_refresh_token


def getaccounts():
    url = 'https://sandbox.handelsbanken.com/openbanking/psd2/v2/accounts'

    headers = {
        'X-IBM-Client-Id': "c01c36a1-59f1-44c3-9589-7870c0201846",
        'Authorization': "Bearer " + requestgranttoken()[0],
        'PSU-IP-Address': "192.102.28.2",
        'TPP-Transaction-ID': "c8271b81-4229-5a1f-bf9c-758f11c1f5b1",
        'TPP-Request-ID': "6b24ce42-237f-4303-a917-cf778e5013d6",
        'accept': "application/json",
    }
    response = requests.get(url, headers=headers,)
    return response.text


def gettransactions():

    url = 'https://sandbox.handelsbanken.com/openbanking/psd2/v2/accounts/ae57e780-6cf3-11e9-9c41-e957ce7d7d69/transactions'

    headers = {
        'X-IBM-Client-Id': "c01c36a1-59f1-44c3-9589-7870c0201846",
        'Authorization': "Bearer " + requestgranttoken()[0],
        'PSU-IP-Address': "192.102.28.2",
        'TPP-Transaction-ID': "c8271b81-4229-5a1f-bf9c-758f11c1f5b1",
        'TPP-Request-ID': "6b24ce42-237f-4303-a917-cf778e5013d6",
        'accept': "application/json",
    }
    response = requests.get(url, headers=headers)

    print(response.text)
    return response.text

gettransactions()
getinitauthorization()