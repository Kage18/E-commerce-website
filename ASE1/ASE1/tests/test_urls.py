from django.urls import reverse,resolve
from blog import urls

class TestUrls:

	def test_detail_url(self):
		path1=reverse('post_list')
		assert resolve(path1).view_name == 'post_list'

	def test_detail_url(self):
		path1=reverse('post_edit',kwargs={id:1})
		assert resolve(path1).view_name == 'post_edit'

	def test_detail_url(self):
		path1=reverse('post_delete',kwargs={id:2})
		assert resolve(path1).view_name == 'post_delete'

	def test_detail_url(self):
		path1=reverse('post_detail',kwargs={id:3})
		assert resolve(path1).view_name == 'post_detail'

	def test_detail_url(self):
		path1=reverse('post_create')
		assert resolve(path1).view_name == 'post_create'

	def test_detail_url(self):
		path1=reverse('like_post')
		assert resolve(path1).view_name == 'like_post'