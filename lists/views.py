from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_page(request):
	# if request.method == 'POST':
	# 	return HttpResponse(request.POST['item_text'])		# <class 'django.http.response.HttpResponse'>
	return render(request, 'home.html',	{'new_item_text': request.POST.get('item_text', '')})		# <class 'django.http.response.HttpResponse'>