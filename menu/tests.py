from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Menu, Item, Ingredient


menu_data1 = {
    'season': 'Summer',
}

menu_data2 = {
    'season': 'Winter',
}


class MenuViewsTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(
            username="mister_tester",
            email="mister_teste@gmail.com",
            password="testtest"
        )
        ingredient1 = Ingredient(name="peach")
        ingredient1.save()
        ingredient2 = Ingredient(name="strawberry")
        ingredient2.save()
        self.item1 = Item(
            name="Item 1",
            description="testing items",
            chef=self.test_user
        )
        self.item1.save()
        self.item1.ingredients.add(ingredient1, ingredient2)
        self.menu1 = Menu.objects.create(**menu_data1)
        self.menu1.items.add(self.item1)
        self.menu2 = Menu.objects.create(**menu_data2)
        self.menu2.items.add(self.item1)

    def test_menu_list_view(self):
        resp = self.client.get(reverse("menu_list"))
        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.menu1, resp.context["menus"])
        self.assertIn(self.menu2, resp.context["menus"])
        self.assertTemplateUsed(resp, "menu/list_all_current_menus.html")
        self.assertContains(resp, self.menu1.season)

    def test_menu_detail_view(self):
        resp = self.client.get(reverse("menu_detail", kwargs={"pk": self.menu1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(self.menu1, resp.context["menu"])
        self.assertTemplateUsed(resp, "menu/menu_detail.html")

    def test_create_new_menu_view_GET(self):
        resp = self.client.get(reverse("menu_new"))
        self.assertEqual(resp.status_code, 200)

    def test_edit_menu_view_GET(self):
        resp = self.client.get(reverse("menu_edit", kwargs={"pk": self.menu1.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_edit_menu_view_POST(self):
        resp = self.client.post(reverse('menu_edit', kwargs={"pk": self.menu1.pk}))
        self.assertEqual(resp.status_code, 200)


class ItemViewsTest(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(
            username="mister_tester",
            email="mister_teste@gmail.com",
            password="testtest"
        )
        ingredient1 = Ingredient(name="peach")
        ingredient1.save()
        ingredient2 = Ingredient(name="strawberry")
        ingredient2.save()
        self.item1 = Item(
            name="Item 1",
            description="testing items",
            chef=self.test_user
        )
        self.item1.save()
        self.item1.ingredients.add(ingredient1, ingredient2)
        self.menu1 = Menu.objects.create(**menu_data1)
        self.menu1.items.add(self.item1)
        self.menu2 = Menu.objects.create(**menu_data2)
        self.menu2.items.add(self.item1)

    def test_item_detail_view(self):
        resp = self.client.get(reverse('item_detail', kwargs={"pk": self.item1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed('menu/detail_item.html')

    def test_item_detail_view_404(self):
        resp = self.client.get(reverse('item_detail', kwargs={'pk': 3}))
        self.assertEqual(resp.status_code, 404)
        self.assertTemplateUsed('menu/detail_item.html')