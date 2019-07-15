
from django.conf.urls import url
from gongzhong import views

urlpatterns = [
    url(r'^$', views.index.as_view(), name='index'),

    url(r'^api/wx$', views.wx.as_view(), name='wx'),
]
