from django.test import TestCase
from django.urls import reverse
from .models import *
from django.contrib.auth.models import User
# Create your tests here.


def create_post(author, title, text, category, tag):
    post = Post.objects.create(author=author, title=title, text=text)
    category.post_set.add(post)
    tag.post_set.add(post)
    return post


def create_user(username, password):
    return User.objects.create(username=username, password=password)


def create_category(name):
    return Category.objects.create(name=name)


def create_tag(name):
    return Tag.objects.create(name=name)


class PostListIndexTest(TestCase):
    def test_no_post(self):
        url = reverse('blog:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['post_list'], [])

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








