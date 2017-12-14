# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import datetime

from .models import Shitpost, Post_Comment

response_404_msg = "S E N T I E N C E  unavailable."


def create_post(text_post, date):
    """
    Shitpost object constructor
    """
    time = timezone.now() + datetime.timedelta(days=date)
    return Shitpost.objects.create(text_post=text_post, image='img.png', created_on=time)


class ShitpostIndexViewTests(TestCase):

    def test_no_post(self):
        """
        If no posts exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('shitposts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, response_404_msg)
        self.assertQuerysetEqual(response.context['post_list'], [])

    def test_past_post(self):
        """
        Posts published in the past are displayed.
        """
        create_post(text_post='Old post', date=-30)
        response = self.client.get(reverse('shitposts:index'))
        self.assertQuerysetEqual(
            response.context['post_list'],
            ['<Shitpost: Text: Old post>']
        )

    def test_future_post(self):
        """
        Future posts are not displayed.
        """
        create_post(text_post='Future post', date=30)
        response = self.client.get(reverse('shitposts:index'))
        self.assertContains(response, response_404_msg)        
        self.assertQuerysetEqual(response.context['post_list'], [])


    def test_past_and_future_posts(self):
        """
        Only posts published in the past are displayed when both past and future posts exist.
        """
        create_post(text_post='Old post', date=-30)
        create_post(text_post='Future post', date=30)        
        response = self.client.get(reverse('shitposts:index'))
        self.assertQuerysetEqual(
            response.context['post_list'],
            ['<Shitpost: Text: Old post>']
        )


    def test_mult_past_posts(self):
        """
        The index page may display multiple posts.
        """
        create_post(text_post='Old post 1', date=-2)
        create_post(text_post='Old post 2', date=-1)        
        response = self.client.get(reverse('shitposts:index'))
        self.assertQuerysetEqual(
            response.context['post_list'],
            ['<Shitpost: Text: Old post 2>', 
             '<Shitpost: Text: Old post 1>']
        )


class ShitpostDetailViewTests(TestCase):

    def test_past_post(self):
        """
        Posts published in the past are displayed.
        """
        post = create_post(text_post='Old post', date=-30)
        url = reverse('shitposts:detail', args=(post.id,))
        response = self.client.get(url)
        self.assertContains(response, post.text_post)


class VoteTests(TestCase):

    def test_upvote(self):
        """
        A user can upvote a post.
        """
        pass

    def test_downvote(self):
        """
        A user can downvote a post.
        """
        pass

    def test_mult_upvotes(self):
        """
        A user can only place a single upvote.
        """
        pass        

    def test_mult_downvotes(self):
        """
        A user can only place a single downvote.
        """
        pass

    def test_negate_vote(self):
        """
        A user can only place a single upvote.
        """
        pass        