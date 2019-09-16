from django.shortcuts import render
from django.views.generic import View
from hashlib import sha1
from django.http import JsonResponse, HttpResponse
import requests
import datetime
import time
import xmltodict
import urllib.request
import json


from django.views.decorators.csrf import csrf_exempt


APP_ID = 'wx44f11c5a2d62aded'
SECRET = '25c7a4892a2f4e81d1e2f423629dba86'
code = None
# Create your views here.

class index(View):

    def get(self, request):
        print(9999)

        return JsonResponse({'code': 200, 'message': '这是首页'})



class wx(View):
    '''

    signature
    微信加密签名，signature结合了开发者填写的token参数和请求中的timestamp参数、nonce参数。
    timestamp
    时间戳
    nonce
    随机数
    echostr
    随机字符串
    '''

    def get(self, request):
        params = ['zjp_ctt']
        timestamp = request.GET.get('timestamp')
        signature = request.GET.get('signature')
        nonce = request.GET.get('nonce')
        echostr = request.GET.get('echostr')

        if not all([signature, timestamp, nonce, echostr]):
            return 'gun'

        params.append(str(timestamp))

        params.append(str(nonce))

        # params.append(echostr)
        params.sort()
        str1 = "".join(params)

        result = self.get_hash(str1)
        print('----------------')

        print('time ' + timestamp)
        print('signature ' + signature)
        print('nonce ' + nonce)

        # print(result)
        if (signature == result):
            return HttpResponse(echostr)

        else:
            return JsonResponse({'code': 200, 'message': 'false'})

    def get_hash(self, strt):  # salt 盐

        sh = sha1()
        sh.update(strt.encode('utf-8'))
        return sh.hexdigest()

        # return JsonResponse({'code': 200, 'message': 'sucess'})

    def post(self,request):

        print(request.POST)
        print('----')
        # return HttpResponse('ok')
        xml_str = request.body
        if not xml_str:
            return HttpResponse('not weixin')

        # 对xml字符串进行解析
        xml_str = xml_str.decode()
        xml_dict = xmltodict.parse(xml_str)
        xml_dict = xml_dict.get("xml")

        # 提取消息类型
        msg_type = xml_dict.get("MsgType")
        ToUserName = xml_dict.get("FromUserName")
        FromUserName = xml_dict.get("ToUserName")
        content = "i love you"
        if msg_type == "text":
            # 表示发送的是文本消息
            # 构造返回值，经由微信服务器回复给用户的消息内容
            # resp_dict = {
            #     "xml": {
            #         "ToUserName": "<![CDATA[" + xml_dict.get("FromUserName") + "]]",
            #         "FromUserName": "<![CDATA[" + xml_dict.get("ToUserName") + "]]",
            #         "CreateTime": int(time.time()),
            #         "MsgType": "<![CDATA[" + "text" + "]]",
            #         "Content": "<![CDATA[" + xml_dict.get("Content") + "]]"
            #     }
            # }

            resp_dict= """
               <xml>
               <ToUserName><![CDATA[%s]]></ToUserName>
               <FromUserName><![CDATA[geeks_at_qdu]]></FromUserName>
               <CreateTime>12345678</CreateTime>
               <MsgType><![CDATA[text]]></MsgType>
               <Content><![CDATA[%s]]></Content>
               </xml>"""%(ToUserName, FromUserName, content)

        else:
            # resp_dict = {
            #     "xml": {
            #         "ToUserName": xml_dict.get("FromUserName"),
            #         "FromUserName": xml_dict.get("ToUserName"),
            #         "CreateTime": int(time.time()),
            #         "MsgType": "text",
            #         "Content": "i love u"
            #     }
            # }
            resp_dict = {
                "xml": {
                    "ToUserName": "<![CDATA[" + xml_dict.get("FromUserName") + "]]",
                    "FromUserName": "<![CDATA[" + xml_dict.get("ToUserName") + "]]",
                    "CreateTime": int(time.time()),
                    "MsgType": "<![CDATA[text]]",
                    "Content": "<![CDATA[i love u]]"
                }
            }

        # 将字典转换为xml字符串
        resp_xml_str = xmltodict.unparse(resp_dict)
        # 返回消息数据给微信服务器
        return resp_xml_str



    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(wx, self).dispatch(*args, **kwargs)


class weixinhtml(View):
    # def get(self, request):
    #     code = request.GET.get('code')
    #
    #     print('----8----')
    #     if not code:
    #         return HttpResponse('error')
    #
    #     req_url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (
    #     APP_ID, SECRET, code)
    #     print('----9----')
    #
    #     reso = requests.get(url=req_url, timeout=10)
    #     reso = reso.json()
    #     print(reso)
    #
    #     if 'errcode' in reso:
    #         return HttpResponse('error noonooo')
    #
    #     print('----3----')
    #
    #     openid = reso['openid']
    #     access_token = reso['access_token']
    #
    #     req_user = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN" % (
    #     access_token, openid)
    #     print('----5----')
    #
    #     res2 = requests.get(url=req_user, timeout=10)
    #     user = res2.json()
    #     print(user)
    #     if "errcode" in user:
    #         return HttpResponse("获取用户信息失败")
    #
    #     else:
    #         print('----6----')
    #
    #         return render(request, 'user.html', {'user': user})
    #
    def get(self, request):
        """让用户通过微信访问的网页页面视图"""
        # 从微信服务器中拿去用户的资料数据
        # 1. 拿去code参数
        global code
        if code:
            return self.getUserIngo(code, request)

        code = request.GET.get("code")

        if not code:
            return HttpResponse("确实code参数")




    def getUserIngo(self, code, request):

        # 2. 向微信服务器发送http请求，获取access_token
        url = "https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code" % (
        APP_ID, SECRET, code)

        # 使用urllib2的urlopen方法发送请求
        # 如果只传网址url参数，则默认使用http的get请求方式, 返回响应对象
        response = urllib.request.urlopen(url)

        # 获取响应体数据,微信返回的json数据
        json_str = response.read()
        resp_dict = json.loads(json_str)

        # 提取access_token
        if "errcode" in resp_dict:
            return HttpResponse("获取access_token失败")

        access_token = resp_dict.get("access_token")
        open_id = resp_dict.get("openid")  # 用户的编号

        # 3. 向微信服务器发送http请求，获取用户的资料数据
        url = "https://api.weixin.qq.com/sns/userinfo?access_token=%s&openid=%s&lang=zh_CN" % (access_token, open_id)

        response = urllib.request.urlopen(url)

        # 读取微信传回的json的响应体数据
        user_json_str = response.read()
        user_dict_data = json.loads(user_json_str)
        user_dict_data = {'headimgurl': 'http://thirdwx.qlogo.cn/mmopen/vi_32/3xho39jD8bYBENcFXY9B6Ph04kW5AicVeTRdkIcEI8TVpkeic7u3ffeeo3S1aYaqL4lKKjgxYeOv76J4HED1icHCw/132', 'city': 'æ\x9c\x9dé\x98³', 'privilege': [], 'province': 'å\x8c\x97äº¬', 'country': 'ä¸\xadå\x9b½', 'sex': 1, 'nickname': 'ç¨»éº¦ç©\x97', 'openid': 'owzD_ts-Np5OKc8gIFetpwhy5wDY', 'language': 'zh_CN'}

        if "errcode" in user_dict_data:
            return HttpResponse("获取用户信息失败")
        else:
            # 将用户的资料数据填充到页面中
            # return render_template("index.html", user=user_dict_data)
            return render(request, "userinfo.html", {"headimgurl":user_dict_data['user_dict_data'], "nickname":user_dict_data['nickname']})

    class gettoken(View):

    # nowtime = datetime.datetime.now()



        def get(self, req):


            # return HttpResponse(888)
            '''
            # https://api.weixin.qq.com
            # /cgi-bin/token?grant_type=client_credential
            # &appid=wx44f11c5a2d62aded&secret=25c7a4892a2f4e81d1e2f423629dba86
            '''

            return self.reqtoken()

        def reqtoken(self, tokenObj = { 'expires_in': 7200, 'nowtime': datetime.datetime.now(), 'token': None   } ):
             # print(gettoken.tokenObj)


             # print(cachetime2-cachetime)
             def protecttoken():

                 cachetime = datetime.datetime.now()

                 # print('---')

                 a = tokenObj['token']
                 b = (cachetime - tokenObj['nowtime']).seconds <= 7200
                 # print(a)
                 if ( a and b):

                     print('aaa')
                     print( tokenObj['token'] )

                     return JsonResponse({'access_token': tokenObj['token'] })
                 else:
                     print('bbbb')
                     tokenHost = 'https://api.weixin.qq.com/cgi-bin/token'
                     params = {'grant_type': 'client_credential',
                               'appid': 'wx44f11c5a2d62aded',
                               'secret': '25c7a4892a2f4e81d1e2f423629dba86'}
                     res = None
                     try:
                         res = requests.get(url=tokenHost, timeout=10, params=params)
                     except Exception as e:
                         print('出错了')

                     print('------------')

                     print(res.json())

                     # return JsonResponse(res.json())

                     tokenObj['token'] = res.json()['access_token']

                     return JsonResponse({'code':200 , 'access_token': tokenObj['token'] })

             return protecttoken()






