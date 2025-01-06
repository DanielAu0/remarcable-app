from django.test import TestCase
from django.test import RequestFactory
from remarcableapp.templatetags.custom_filter import update_query_params  

class UpdateQueryParamsTest(TestCase):
    def setUp(self):
        # Use RequestFactory to simulate an HTTP request
        self.factory = RequestFactory()

    def test_add_tag_no_filters(self):
        """Test the scenario where a new tag is added when there are no existing filters."""

        # Create a mock request with no query parameters
        request = self.factory.get('/')
        result = update_query_params(request, 'tag', 1)
        
        # Verify that 'tag=1' is added to the query string
        self.assertIn('tag=1', result)

    def test_add_tag_multiple_filters(self):
        """Test the scenario where a new tag is added when there are existing filters."""
        
        # Create a mock request with multiple tags: '?tag=1&tag=2'
        request = self.factory.get('/?tag=1&tag=2')
        result = update_query_params(request, 'tag', 3)
        
        # Verify that all three tags are present in the query string
        self.assertIn('tag=1', result)
        self.assertIn('tag=2', result)
        self.assertIn('tag=3', result)

    def test_remove_tag(self):
        """Test the scenario where an existing tag is removed from the query string."""
        
        # Create a mock request with two tags: '?tag=1&tag=2'
        request = self.factory.get('/?tag=1&tag=2')
        result = update_query_params(request, 'tag', 2)
        
        # Verify that 'tag=2' is removed from the query string
        self.assertNotIn('tag=2', result)
        # Verify that 'tag=1' remains in the query string
        self.assertIn('tag=1', result)

    def test_remove_last_tag(self):
        """Test the scenario where the last remaining tag is removed from the query string."""
        
        # Create a mock request with only one tag: '?tag=1'
        request = self.factory.get('/?tag=1')
        result = update_query_params(request, 'tag', 1)
        
        # Verify that 'tag=1' is removed from the query string
        self.assertNotIn('tag=1', result)
        # Verify that 'tag' is no longer in the query string
        self.assertNotIn('tag', result)

    def test_update_category(self):
        """Test the scenario where category is updated in the query string."""
        
        # Create a mock request with an initial query string '?category=1'
        request = self.factory.get('/?category=1')
        result = update_query_params(request, 'category', 2)
        
        # Verify that 'category=2' is added to the query string
        self.assertIn('category=2', result)
        # Verify that the old category value ('category=1') is no longer in the query string
        self.assertNotIn('category=1', result)

    def test_remove_category(self):
        """Test the scenario where category is removed in the query string."""
        
        # Create a mock request with an initial query string '?category=1'
        request = self.factory.get('/?category=1')
        result = update_query_params(request, 'category', 1)
        
        # Verify that 'category=1' is removed from the query string
        self.assertNotIn('category=1', result)
        # Verify that 'category' is no longer in the query string
        self.assertNotIn('category', result)
