from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
from random import randint
client = AcsClient('******', '******', 'cn-hangzhou')

def send_sms(phonenum,code):
    request = CommonRequest()
    request.set_accept_format('json')
    request.set_domain('dysmsapi.aliyuncs.com')
    request.set_method('POST')
    request.set_protocol_type('https') # https | http
    request.set_version('2017-05-25')
    request.set_action_name('SendSms')

    request.add_query_param('RegionId', "cn-hangzhou")
    request.add_query_param('PhoneNumbers', phonenum)
    request.add_query_param('SignName', "yoursignname")
    request.add_query_param('TemplateCode', "yourtemplatecode")
    request.add_query_param('TemplateParam', {"code":code})

    response = client.do_action(request)
# python2:  print(response)
    print(str(response, encoding = 'utf-8'))

if __name__=='__main__':
    send_sms()
