from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item,List

# Create your views here.
def home_page(request):		## url(r'^$', views.home_page, name='home')
	response = render(request, 'home.html')
	return response

def view_list(request):		## 	url(r'^lists/the_only_list_in_the_world/$', views.view_list, name='view_list')		
	items = Item.objects.all()
	response = render(request, 'list.html', {'items': items})
	return response

def new_list(request):		## 	url(r'^lists/new$', views.new_list, name='new_list'),
	list_ = List.objects.create()
	Item.objects.create(text=request.POST['item_text'],list=list_)
	response = redirect('/lists/the_only_list_in_the_world/')
	return response
