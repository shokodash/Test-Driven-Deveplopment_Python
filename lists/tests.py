from django.core.urlresolvers import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.views import home_page
from lists.models import Item

# Create your tests here.
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

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()											# request.method = None
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'					# print(type(request.POST)) -> <class 'django.http.request.QueryDict'>

		response = home_page(request)									# <class 'django.http.response.HttpResponse'>

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

		expected_html = render_to_string('home.html', {'new_item_text': 'A new list item'})
		responded_html = response.content.decode()

		self.assertIn('A new list item', responded_html)
		self.assertEqual(responded_html, expected_html)

class ItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(second_saved_item.text, 'Item the second')

class HomePageTest(TestCase):
	def test_home_page_only_saves_items_when_necessary(self):
		request = HttpRequest()
		home_page(request)
		self.assertEqual(Item.objects.count(), 0)