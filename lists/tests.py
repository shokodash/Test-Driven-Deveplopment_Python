from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest,HttpResponse
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item, List

def logg(message, name=''):
    print('     -- logg:')
    print(name+': '+message)
    print('--------------------------------------')

class SmokeTest(TestCase):

	def test_root_resolves_to_home_page_view(self):
		found = resolve('/')											# <class 'django.core.urlresolvers.ResolverMatch'>
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct__html(self):
		request = HttpRequest()											# <class 'django.http.request.HttpRequest'>
		response = home_page(request)									# <class 'django.http.response.HttpResponse'>
		expected_html = render_to_string('home.html')					# <class 'django.utils.safestring.SafeText'>
		responded_html = response.content.decode()						# <class 'str'>
		self.assertEqual(responded_html, expected_html)



class ListandItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		list_ = List()
		list_.save()
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.list = list_
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.list = list_
		second_item.save()

		saved_lists = List.objects.first()
		self.assertEqual(saved_lists, list_)

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.text, 'Item the second')
		self.assertEqual(second_saved_item.list, list_)



class ListViewTest(TestCase):

	def test_uses_list_template(self):
		response = self.client.get('/lists/the_only_list_in_the_world/')
		self.assertTemplateUsed(response,'list.html')

	def test_displays_all_items(self):
		list_ = List.objects.create()
		Item.objects.create(text='itemey 1', list=list_)
		Item.objects.create(text='itemey 2', list=list_)

		response = self.client.get('/lists/the_only_list_in_the_world/')
		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 2')

class NewListTest(TestCase):

	def test_redirects_after_POST(self):
		response = self.client.post('/lists/new', data={'item_text': 'A new list item'})

		self.assertRedirects(response, 'lists/the_only_list_in_the_world/')		

	def test_saving_a_POST_request(self):
		self.client.post('/lists/new', data={'item_text': 'A new list item'})
		
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')
