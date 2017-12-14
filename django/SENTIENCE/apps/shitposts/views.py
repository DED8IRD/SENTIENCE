# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.utils import timezone

from .models import Shitpost, Post_Comment


class IndexView(generic.ListView):
    template_name = 'shitposts/index.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        """
        Return the last four published posts (not including those set to be
        published in the future).
        """
        return Shitpost.objects.filter(
            created_on__lte=timezone.now()
        ).order_by('-created_on')
        # [:4]


# class DetailView(generic.DetailView):
#     model = Shitpost
#     template_name = 'shitposts/detail.html'


# def index(request):
#     post_list = Shitpost.objects.filter(
#         created_on__lte=timezone.now()
#     ).order_by('-created_on')[:4]
#     context = {
#         'post_list': post_list,
#     }
#     return render(request, 'shitposts/index.html', context)


def detail(request, shitpost_id):
    post = get_object_or_404(Shitpost, id=shitpost_id)
    comments = Post_Comment.objects.all().filter(shitpost=shitpost_id)
    context = {
        'id': post.id,
        'text_post': post.text_post,
        'image': post.image,
        'upvotes': post.upvotes,
        'created_on': post.created_on,
        'comments': comments
    }
    return render(request, 'shitposts/detail.html', context)


# def vote(request, shitpost_id):
#     return HttpResponse("Voting on shitpost #%s" % shitpost_id)
