
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest
import time

def logg(message, name=''):
    print('     -- logg:')
    print(name+': '+message)
    print('--------------------------------------')

class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        # time.sleep(5)
        self.browser.quit()
    
    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):

        # Edith has heard about a cool new online to-do app. She goes
        # to check out its homepage
        self.browser.get(self.live_server_url)              ## self.live_server_url -> http://localhost:8081
        # She notices the page title and header mention to-do lists
        self.assertIn('To-Do', self.browser.title)
        h1_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', h1_text)


    # She is invited to enter a to-do item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')

    # She types "Buy peacock feathers" into a text box (Edith's hobby
    # is tying fly-fishing lures)
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)              ## a lot of things happen here, which involve home.html, url.py, views.py, and another request as a result of redirect

    # When she hits enter, she is taken to a new URL,
    # and now the page lists "1: Buy peacock feathers" as an item in a to-do list table
        edith_list_url = self.browser.current_url
        logg(edith_list_url, 'edith_list_url')
        self.assertRegex(edith_list_url, '/lists/.+')
        self.check_for_row_in_list_table('1: Buy peacock feathers')

    # There is still a text box inviting her to add another item. She
    # enters "Use peacock feathers to make a fly" (Edith is very methodical)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)
    # The page updates again, and now shows both items on her list
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

    ###################################################################
    # Now a newuser, Francis comes along
        ## We use a new browser session to make sure that no information
        ## of Edith's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Firefox()

    # Francis visits the home page.  There is no sign of Edith's list
        self.browser.get(self.live_server_url)                          ## self.live_server_url -> http://localhost:8081
        body_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', body_text)
        self.assertNotIn('make a fly', body_text)

    # Francis starts a new list by entering a new item. He
    # is less interesting than Edith...
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

    # Francis gets his own unique url
        francis_list_url = self.browser.current_url
        logg(francis_list_url, 'francis_list_url')
        self.assertNotEqual(francis_list_url, edith_list_url)
        self.assertRegex(francis_list_url, '/lists/.+')
        self.check_for_row_in_list_table('Buy milk')

    # Again there is no trace of Edith's list
        page_text = self.browser.find_elements_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)




        # Satisfied they both go back to sleep
        self.fail('Finish the test!')
