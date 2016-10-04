from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item,List

def logg(var, name=''):
    print(' ->-> '+ name +' <value -> type>:')
    print(' ->-> '+ str(var) + ' -> ' + str(type(var)))
    print(' ->->------------------------------------')
# Create your views here.
def home_page(request):     
    response = render(request, 'home.html')
    return response

def view_list(request,list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    response = render(request, 'list.html', {'items': items})
    return response

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'],list=list_)
    response = redirect('/lists/%d/'%(list_.id))
    return response
def add_item(request):
    response = HttpResponse('some content')
    logg(response, 'response')
    return response   