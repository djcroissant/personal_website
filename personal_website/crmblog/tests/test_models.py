from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import DataError

from crmblog.models import Post

class PostModelTests(TestCase):
    def test_post_invalid_without_title(self):
        title = ""
        post = Post.objects.create(title=title)
        self.assertRaises(ValidationError, lambda: post.full_clean())

    def test_post_valid_with_only_title(self):
        title = "hello"
        post = Post.objects.create(title=title)
        try:
            post.full_clean()
        except:
            self.fail("full_clean() raised an error unexpectedly!")

    def test_title_greater_than_255_raises_DataError(self):
        title = "x" * 256
        test = lambda: Post.objects.create(title=title)
        self.assertRaises(DataError, test)

    def test_tagline_greater_than_255_raises_DataError(self):
        title = "title"
        tagline = "x" * 256
        test = lambda: Post.objects.create(title=title, tagline=tagline)
        self.assertRaises(DataError, test)

    def test_printing_instance_of_Post_returns_title(self):
        title = "hello"
        post = Post.objects.create(title=title)
        self.assertEqual(str(post), "hello")

    def test_excerpt_returns_first_ten_words_of_content(self):
        title = "hello"
        content = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11"
        post = Post.objects.create(title=title, content=content)
        self.assertTrue("1, 2, 3, 4, 5, 6, 7, 8, 9, 10," in post.excerpt)
        self.assertTrue("11" not in post.excerpt)

    def test_excerpt_returns_blank_string_if_no_content(self):
        title = "hello"
        post = Post.objects.create(title=title)
        self.assertEqual(post.excerpt, "")

    def test_excerpt_appends_dots_if_content_gt_10_words(self):
        title = "hello"
        content = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11"
        post = Post.objects.create(title=title, content=content)
        self.assertEqual(post.excerpt[-3:], "...")

    def test_excerpt_does_not_append_dots_if_content_lte_10_words(self):
        title = "hello"
        content = "1, 2, 3, 4, 5, 6, 7, 8, 9, 10,"
        post = Post.objects.create(title=title, content=content)
        self.assertEqual(post.excerpt[-3:], "10,")
