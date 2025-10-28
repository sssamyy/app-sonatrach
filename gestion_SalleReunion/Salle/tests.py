# from django.test import TestCase, Client
# from django.urls import reverse
# from .models import Salle
# from .forms import SalleForm

# class CreerSalleViewTest(TestCase):
#     def test_get_request(self):
#         response = self.client.get(reverse('creer_salle'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'creer.html')
#         self.assertIsInstance(response.context['form'], SalleForm)

#     def test_post_request_valid_data(self):
#         data = {'nom': 'Salle 1', 'capacite': 50}
#         response = self.client.post(reverse('creer_salle'), data)
#         self.assertEqual(response.status_code, 302)
#         self.assertEqual(Salle.objects.count(), 1)
#         self.assertEqual(Salle.objects.first().nom, 'Salle 1')

#     def test_post_request_invalid_data(self):
#         data = {'nom': '', 'capacite': 50}
#         response = self.client.post(reverse('creer_salle'), data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'creer.html')
#         self.assertIsInstance(response.context['form'], SalleForm)

# class DetailsSalleViewTest(TestCase):
#     def test_get_request(self):
#         salle = Salle.objects.create(nom='Salle 1', capacite=50)
#         response = self.client.get(reverse('details_salle', args=[salle.pk]))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'details_salle.html')
#         self.assertEqual(response.context['Salle'], salle)

# class ListSallesViewTest(TestCase):
#     def test_get_request(self):
#         Salle.objects.create(nom='Salle 1', capacite=50)
#         Salle.objects.create(nom='Salle 2', capacite=100)
#         response = self.client.get(reverse('list_salles'))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'SalleList.html')
#         self.assertEqual(len(response.context['salles']), 2)

#     def test_get_request_with_show_deleted(self):
#         Salle.objects.create(nom='Salle 1', capacite=50, isDeleted=True)
#         Salle.objects.create(nom='Salle 2', capacite=100, isDeleted=False)
#         response = self.client.get(reverse('list_salles') + '?show_deleted=True')
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'SalleList.html')
#         self.assertEqual(len(response.context['salles']), 2)

# class ModifierSalleViewTest(TestCase):
#     def test_get_request(self):
#         salle = Salle.objects.create(nom='Salle 1', capacite=50)
#         response = self.client.get(reverse('modifier_salle', args=[salle.pk]))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'modifierSalle.html')
#         self.assertIsInstance(response.context['form'], SalleForm)

#     def test_post_request_valid_data(self):
#         salle = Salle.objects.create(nom='Salle 1', capacite=50)
#         data = {'nom': 'Salle 1 updated', 'capacite': 75}
#         response = self.client.post(reverse('modifier_salle', args=[salle.pk]), data)
#         self.assertEqual(response.status_code, 302)
#         salle.refresh_from_db()
#         self.assertEqual(salle.nom, 'Salle 1 updated')
#         self.assertEqual(salle.capacite, 75)

#     def test_post_request_invalid_data(self):
#         salle = Salle.objects.create(nom='Salle 1', capacite=50)
#         data = {'nom': '', 'capacite': 75}
#         response = self.client.post(reverse('modifier_salle', args=[salle.pk]), data)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'modifierSalle.html')
#         self.assertIsInstance(response.context['form'], SalleForm)

# class SupprimerSalleViewTest(TestCase):
#     def test_get_request(self):
#         salle = Salle.objects.create(nom='Salle 1', capacite=50)
#         response = self.client.get(reverse('supprimer_salle', args=[salle.pk]))
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'supprimerSalle.html')
#         self.assertEqual(response.context['salle'], salle)

#     def test_post_request(self):
#         salle = Salle.objects.create(nom='Salle 1', capacite=50)
#         response = self.client.post(reverse('supprimer_salle', args=[salle.pk]))
#         self.assertEqual(response.status_code, 302)
#         salle.refresh_from_db()
#         self.assertTrue(salle.isDeleted)