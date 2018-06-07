from django.test import TestCase

class PostModelTests(TestCase):
    def test_post_invalid_without_title(self):
        title = ""
        post = Post.objects.create(title=title)
        self.assertRaises(ValidationError, lambda: post.full_clean())

    def test_post_valid_without_tagline(self):
        pass

    def test_post_valid_without_photo(self):
        pass

    def test_post_valid_without_content(self):
        pass

    def test_title_greater_than_255_raises_DataError(self):
        pass

    def test_tagline_greater_than_255_raises_DataError(self):
        pass

    def test_printing_instance_of_Post_returns_title(self):
        pass

    def test_excerpt_returns_first_ten_words_of_content(self):
        pass

    def test_excerpt_returns_blank_string_if_no_content(self):
        pass

    def test_excerpt_appends_dots_if_content_greater_than_10_words(self):
        pass
