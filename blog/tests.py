from django.test import TestCase
from django.urls import reverse
from .models import *
from django.contrib.auth.models import User
from django.utils.text import slugify
# Create your tests here.


def create_post(author, title, slug, category, tag):
    description = 'descryption'
    body = 'body'

    post = Post.objects.create(
        author=author, slug=slug, title=title, description=description, body=body,
    )
    category.post_set.add(post)
    tag.post_set.add(post)
    return post


def create_user(username, password):
    return User.objects.create(username=username, password=password)


def create_category(name, slug):
    return Category.objects.create(name=name, slug=slug)


def create_tag(name, slug):
    return Tag.objects.create(name=name, slug=slug)


class PostListIndexTest(TestCase):
    def test_no_post(self):
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['post_list'], [])

    def test_one_post(self):
        author = create_user('user', 'senha')
        title = 'post title'
        slug = slugify(title)

        category = create_category('category name', slugify('category name'))
        tag = create_tag('tag name', slugify('tag name'))

        create_post(author, title, slug, category, tag)

        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['post_list'], ['<Post: post title>'])

    def test_many_post(self):
        author = create_user('user', 'senha')
        title = 'post title'
        title2 = 'post title2'
        title3 = 'post title3'

        slug = slugify(title)
        slug2 = slugify(title2)
        slug3 = slugify(title3)

        category = create_category('category name', slugify('category name'))
        tag = create_tag('tag name', slugify('tag name'))

        create_post(author, title, slug, category, tag)
        create_post(author, title2, slug2, category, tag)
        create_post(author, title3, slug3, category, tag)

        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['post_list'],
            [
                '<Post: post title>',
                '<Post: post title2>',
                '<Post: post title3>',
            ]
        )

    def test_no_search_field_and_no_post(self):
        url = reverse('blog:index')
        response = self.client.get(url, {'search': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('search'), None)

    def test_no_search_field_and_one_post(self):
        author = create_user('user', 'senha')
        title = 'post title'
        slug = slugify(title)

        category = create_category('category name', slugify('category name'))
        tag = create_tag('tag name', slugify('tag name'))

        create_post(author, title, slug, category, tag)

        url = reverse('blog:index')
        response = self.client.get(url, {'search': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('search'), None)
        self.assertQuerysetEqual(response.context['post_list'], ['<Post: post title>'])

    def test_no_search_field_and_many_post(self):
        author = create_user('user', 'senha')
        title = 'post title'
        title2 = 'post title2'
        title3 = 'post title3'

        slug = slugify(title)
        slug2 = slugify(title2)
        slug3 = slugify(title3)

        category = create_category('category name', slugify('category name'))
        tag = create_tag('tag name', slugify('tag name'))

        create_post(author, title, slug, category, tag)
        create_post(author, title2, slug2, category, tag)
        create_post(author, title3, slug3, category, tag)

        url = reverse('blog:index')
        response = self.client.get(url, {'search': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get('search'), None)
        self.assertQuerysetEqual(
            response.context['post_list'],
            [
                '<Post: post title>',
                '<Post: post title2>',
                '<Post: post title3>',
            ]
        )

    def test_search_not_found(self):
        url = reverse('blog:index')
        response = self.client.get(url, {'search': 'test'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['post_list'], [])

    def test_search_one_found(self):
        author = create_user('user', 'senha')
        title = 'post title'
        slug = slugify(title)

        category = create_category('category name', slugify('category name'))
        tag = create_tag('tag name', slugify('tag name'))

        create_post(author, title, slug, category, tag)

        url = reverse('blog:index')
        response = self.client.get(url, {'search': 'post title'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['post_list'], ['<Post: post title>'])

    def test_search_many_found(self):
        author = create_user('user', 'senha')
        title = 'post title'
        title2 = 'post title2'
        title3 = 'post title3'

        slug = slugify(title)
        slug2 = slugify(title2)
        slug3 = slugify(title3)

        category = create_category('category name', slugify('category name'))
        tag = create_tag('tag name', slugify('tag name'))

        create_post(author, title, slug, category, tag)
        create_post(author, title2, slug2, category, tag)
        create_post(author, title3, slug3, category, tag)

        url = reverse('blog:index')
        response = self.client.get(url, {'search': 'post title'})
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['post_list'],
            [
                '<Post: post title>',
                '<Post: post title2>',
                '<Post: post title3>',
            ]
        )


'''     self.assertQuerysetEqual(response.context['post_list'], [])

    def test_one_post(self):
        create_post(
            author=create_user('user', 'senha'),
            title='title', text='texto',
            category=create_category('categoria'),
            tag=create_tag('tag')
        )
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertQuerysetEqual(response.context['post_list'], ['<Post: title>'])

    def test_many_post(self):
        create_post(
            author=create_user('user', 'senha'),
            title='title', text='texto',
            category=create_category('categoria'),
            tag=create_tag('tag')
        )
        create_post(
            author=create_user('user1', 'senha'),
            title='title', text='texto',
            category=create_category('categoria'),
            tag=create_tag('tag')
        )
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertQuerysetEqual(
            response.context['post_list'],
            ['<Post: title>',
             '<Post: title>'],
            ordered=False
        )

    def test_post_search(self):
        post = create_post(
            author=create_user('user', 'senha'),
            title='title', text='texto',
            category=create_category('categoria'),
            tag=create_tag('tag')
        )

        url = reverse('blog:index')
        search = '?search='+post.title
        response = self.client.get(url+search)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['post_list'],
            ['<Post: title>', ]
        )

    def test_post_search_not_found(self):
        post = create_post(
            author=create_user('user', 'senha'),
            title='title', text='texto',
            category=create_category('categoria'),
            tag=create_tag('tag')
        )

        url = reverse('blog:index')
        search = '?search=' + 'no_pattern'
        response = self.client.get(url + search)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['post_list'],
            []
        )

    def test_post_search_none(self):
        create_post(
            author=create_user('user', 'senha'),
            title='title', text='texto',
            category=create_category('categoria'),
            tag=create_tag('tag')
        )
        create_post(
            author=create_user('user1', 'senha'),
            title='title', text='texto',
            category=create_category('categoria'),
            tag=create_tag('tag')
        )
        url = reverse('blog:index')
        search = '?search='
        response = self.client.get(url + search)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            response.context['post_list'],
            [
                '<Post: title>',
                '<Post: title>',
            ],
            ordered=False
        )


class PostView(TestCase):
    def test_post_found(self):
        post = create_post(
            author=create_user('user', 'senha'),
            title='title', text='texto',
            category=create_category('categoria'),
            tag=create_tag('tag')
        )
        url = reverse('blog:post', args=(post.id,))
        response = self.client.get(url)
        self.assertEqual(response.context['post'], post)

    def test_post_not_found(self):
        post = create_post(
            author=create_user('user', 'senha'),
            title='title', text='texto',
            category=create_category('categoria'),
            tag=create_tag('tag')
        )
        url = reverse('blog:post', args=(2,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class PostByCategoryTest(TestCase):
    def test_category_does_not_found(self):
        post = create_post(
            author=create_user('user', 'senha'),
            title='title', text='texto',
            category=create_category('categoria'),
            tag=create_tag('tag')
        )
        url = reverse('blog:post_category', args=('any', ))
        response = self.client.get(url)
        self.assertQuerysetEqual(
            response.context['post_list'], []
        )

    def test_post_category_found(self):
        post = create_post(
            author=create_user('user', 'senha'),
            title='title', text='texto',
            category=create_category('categoria'),
            tag=create_tag('tag')
        )
        url = reverse('blog:post_category', args=('categoria',))
        response = self.client.get(url)
        self.assertQuerysetEqual(
            response.context['post_list'],
            [
                '<Post: title>',
            ]
        )
'''







