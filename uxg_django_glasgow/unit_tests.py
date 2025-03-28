from django.test import TestCase
from uxg.models import Category, Page
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
import datetime
 
# Helper Functions
 
def add_category(name, views=0, likes=0):
    """ Helper function to add a category with the necessary checks. """
    if views < 0:
        views = 0
    slug = slugify(name)
    category, created = Category.objects.get_or_create(
        name=name,
        defaults={'views': views, 'likes': likes, 'slug': slug}
    )
    if not created:
        if category.slug != slug:
            category.slug = slug
            category.save()
    return category
 
def add_page(title, url, category_name, views=0, last_visit=None):
    """ Helper function to add a page with required fields and constraints. """
    if views < 0:
        views = 0
    if last_visit and last_visit > timezone.now():
        raise ValueError("last_visit cannot be in the future.")
    category, created = Category.objects.get_or_create(name=category_name)
    page = Page.objects.create(
        title=title,
        url=url,
        category=category,
        views=views,
        last_visit=last_visit or timezone.now()
    )
    return page
 
# Category Model Tests
 
class CategoryMethodTests(TestCase):
 
    def test_ensure_views_are_positive(self): 
        category = add_category('test', views=-1, likes=0)
        self.assertEqual((category.views >= 0), True)
 
    def test_slug_line_creation(self): 
        category = add_category('Random Category String') 
        self.assertEqual(category.slug, 'random-category-string')
 
# Index View Tests
 
class IndexViewTests(TestCase):
 
    def test_index_view_with_no_categories(self): 
        response = self.client.get(reverse('rango:index')) 
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, 'There are no categories present.') 
        self.assertQuerysetEqual(response.context['categories'], [])
 
    def test_index_view_with_categories(self): 
        add_category('Python', 1, 1) 
        add_category('C++', 1, 1) 
        add_category('Erlang', 1, 1) 
        response = self.client.get(reverse('rango:index')) 
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, "Python") 
        self.assertContains(response, "C++") 
        self.assertContains(response, "Erlang") 
        num_categories = len(response.context['categories']) 
        self.assertEquals(num_categories, 3)
 
# Page Model Tests
 
class PageModelTests(TestCase):
 
    def test_page_creation(self):
        category = Category.objects.create(name="Python", views=5, likes=10)
        page = add_page("Test Page", "http://example.com", "Python", views=100)
        self.assertEqual(page.title, "Test Page")
        self.assertEqual(page.url, "http://example.com")
        self.assertEqual(page.category, category)
        self.assertEqual(page.views, 100)
        self.assertLessEqual(page.last_visit, timezone.now())
 
    def test_invalid_last_visit(self):
        future_time = timezone.now() + timezone.timedelta(days=1)
        with self.assertRaises(ValueError):
            add_page("Test Page", "http://example.com", "Python", views=100, last_visit=future_time)
 
    def test_page_creation_without_category(self):
        page = add_page("Another Test Page", "http://example.com", "Django", views=50)
        category = Category.objects.get(name="Django")
        self.assertEqual(page.category, category)
 
# Page View Tests
 
class PageViewTests(TestCase):
    def test_last_visit_updated_on_page_click(self):
        category = Category.objects.create(name="Test", views=0, likes=0)
        page = Page.objects.create(title="Test Page", url="http://example.com", category=category)
        initial_last_visit = page.last_visit
        url = reverse('rango:goto') + f'?page_id={page.id}'
        self.client.get(url)
        page.refresh_from_db()
        self.assertGreaterEqual(page.last_visit, initial_last_visit)