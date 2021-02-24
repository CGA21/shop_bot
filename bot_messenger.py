import requests

def telegram(text,api,group_id):
    if api and group_id:
        message='https://api.telegram.org/bot'+api+'/sendMessage?chat_id=-'+group_id+'&text='+text
        try:
            requests.get(message)
        except:
            print('following telegram message failed to send- \n'+str(message))
    else:
        print('telegram bot api or group id is blank')