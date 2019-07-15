from django.shortcuts import render
from django.views.generic import View
from hashlib import sha1
from django.http import JsonResponse, HttpResponse
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
