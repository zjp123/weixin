
from django.conf.urls import url
from gongzhong import views

urlpatterns = [
    url(r'^$', views.index.as_view(), name='index'),

    url(r'^wx/*', views.wx.as_view(), name='wx'),
    url(r'^gettoken', views.gettoken.as_view(), name='gettoken'),
    url(r'^weixinhtml', views.weixinhtml.as_view(), name='weixinhtml'),
]
