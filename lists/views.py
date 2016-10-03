from django.shortcuts import render, redirect
from django.http import HttpResponse
from lists.models import Item

# Create your views here.
def home_page(request):
	if request.method == 'POST':
		Item.objects.create(text=request.POST['item_text'])
		response = redirect('/lists/the_only_list_in_the_world/')
	else:
		items = Item.objects.all()
		response = render(request, 'home.html', {'items': items})
	return response

def view_list(request):
	items = Item.objects.all()
	response = render(request, 'home.html', {'items': items})
	return response
