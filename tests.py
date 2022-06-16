from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(first_name="test_first",
                                    last_name="test_last",
                                    image_url=None)

        second_user = User(first_name="test_first_two", last_name="test_last_two",
                           image_url=None)

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # Add test post
        test_post = Post(title="Test Title", content="Test Content", 
                          user_id=test_user.id)

        db.session.add(test_post)
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id
        self.post_id = test_post.id

    def tearDown(self):
            """Clean up any fouled transaction."""
            db.session.rollback()


    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)


    def test_user_listing_page(self):
        """Make sure all users display on users page"""
        
        with self.client as client:
            response = client.get('/users')

        html = response.get_data(as_text=True)
        user = User.query.get_or_404(self.user_id)

        self.assertEqual(response.status_code, 200)
        self.assertIn('<!-- Marker tag for user_listing page -->', html)
        self.assertIn(user.first_name, html)


    def test_user_detail_page(self):
        """Make sure user detail page displays correctly"""

        with self.client as client:
            response = client.get(f'/users/{self.user_id}')

        html = response.get_data(as_text=True)
        user = User.query.get_or_404(self.user_id)
        post = Post.query.get_or_404(self.post_id)

        self.assertEqual(response.status_code, 200)
        self.assertIn('<!-- Marker tag for user_detail page -->', html)
        self.assertIn(user.first_name, html)
        self.assertIn(post.title,html)


    def test_user_detail_page_failure(self):
        """Make sure user detail page fails when requesting user_id that is
            incorrect
        """

        with self.client as client:
            response = client.get(f'/users/xxx')

        self.assertEqual(response.status_code, 404)


    def test_user_edit_page(self):
            """Test that edit user form populates"""

            with self.client as client:
                response = client.get(f'/users/{self.user_id}/edit')

            html = response.get_data(as_text=True)
            user = User.query.get_or_404(self.user_id)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<!-- Marker tag for user_editing page -->', html)
            self.assertIn(user.first_name, html)


    def test_user_edit_feature(self):
        """Test editing a user"""
        
        user = User.query.get_or_404(self.user_id)

        with self.client as client:
            response = client.post(
                f"/users/{user.id}/edit",
                data={
                    'first_name':'new_first', 
                    'last_name':user.last_name,
                    'image_url':user.image_url,
                }
            )

        updated_user = User.query.get_or_404(self.user_id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('new_first', updated_user.first_name)
        self.assertEqual('test_last', updated_user.last_name)


    def test_user_edit_redirect(self):
        """Test that submitting edit to user redirects to /users"""

        user = User.query.get_or_404(self.user_id)

        with self.client as client:
            response = client.post(
                f"/users/{self.user_id}/edit",
                data={
                    'first_name':user.first_name, 
                    'last_name':user.last_name,
                    'image_url':user.image_url,
                },
                follow_redirects=True,
                )

        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('<!-- Marker tag for user_listing page -->', html)

    #Update to POST!
    def test_user_detail_page(self):
        """Make sure user detail page displays correctly"""

        with self.client as client:
            response = client.get(f'/users/{self.user_id}')

        html = response.get_data(as_text=True)
        user = User.query.get_or_404(self.user_id)
        post = Post.query.get_or_404(self.post_id)

        self.assertEqual(response.status_code, 200)
        self.assertIn('<!-- Marker tag for user_detail page -->', html)
        self.assertIn(user.first_name, html)
        self.assertIn(post.title,html)

    #Update to Post!!
    def test_user_detail_page_failure(self):
        """Make sure user detail page fails when requesting user_id that is
            incorrect
        """

        with self.client as client:
            response = client.get(f'/users/xxx')

        self.assertEqual(response.status_code, 404)

    
    def test_post_edit_page(self):
            """Test that edit post form populates"""

            with self.client as client:
                response = client.get(f'/posts/{self.post_id}/edit')

            html = response.get_data(as_text=True)
            post = Post.query.get_or_404(self.post_id)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<!-- Marker tag for post_edit page -->', html)
            self.assertIn(post.title, html)


    def test_post_edit_feature(self):
        """Test editing a post"""
        
        post = Post.query.get_or_404(self.post_id)

        with self.client as client:
            response = client.post(
                f"/posts/{post.id}/edit",
                data={
                    'title':'new_title', 
                    'content':post.content,
                }
            )

        updated_post = Post.query.get_or_404(self.post_id)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('new_title', updated_post.title)
        self.assertEqual('Test Content', updated_post.content)


    def test_post_edit_redirect(self):
        """Test that submitting edit to post redirects to /users"""

        post = Post.query.get_or_404(self.post_id)

        with self.client as client:
            response = client.post(
                f"/posts/{post.id}/edit",
                data={
                    'title':post.title, 
                    'content':post.content,
                    'user_id':post.user_id,
                },
                follow_redirects=True,
                )

        html = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn('<!-- Marker tag for user_detail page -->', html)
   
