from django.conf.urls import url, include
from lists import urls as list_urls
from lists import views as list_views

urlpatterns = [
    url(r'^todo/$', list_views.home_page, name='home'),
    url(r'^todo/lists/', include(list_urls))
]