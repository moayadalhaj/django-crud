from django.http import response
from django.test import TestCase
from django.urls import reverse
from .models import Snack
from django.contrib.auth import get_user_model

# Create your tests here.

class test_for_all(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username = "moayad",
            email = 'moayad@moayd.com',
            password = 'asd123'
        )
        self.snack =Snack.objects.create(
                                         title = 'toast with egg',
                                         purchaser = self.user,
                                         description = 'Delicious food'
                                        )
        
    
    def test_snack_list_page_status_code(self):
        url = reverse('snack_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_snack_list_page_tepmlate(self):
        url = reverse('snack_list')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'snack_list.html')

    def test_snack_title(self):
        url = reverse('snack_list')
        response = self.client.get(url)
        self.assertContains(response, 'toast with egg')
    
    def test_details_view(self):
        response = self.client.get(reverse('snack_detail', args = '1'))
        self.assertContains(response,'toast with egg')
        self.assertTemplateUsed(response, 'snack_detail.html')
    
    def test_update_view(self):
        url = reverse('snack_update',args='1')
        response = self.client.post(url,{"title" : 'Shawerma',"purchaser" : self.user.pk,"description" : 'awesome food'})
        self.assertRedirects(response, reverse("snack_detail", args="1"))
    
    def test_delete_view(self):
        url = reverse('snack_delete',args='1')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)