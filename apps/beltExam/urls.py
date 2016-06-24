from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index ),
    url(r'^register$', views.register ),
    url(r'^login$', views.login),
     url(r'^pokes$', views.pokes, name = "pokes"),
    url(r'^logoff$', views.logoff, name = "logoff"),
    url(r'^clickpoke/(?P<id>\d+)$', views.clickpoke, name = "clickpoke"),
    url(r'^check$', views.check),

]
