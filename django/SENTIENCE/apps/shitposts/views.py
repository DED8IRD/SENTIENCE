# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.contrib.auth.decorators import permission_required
from django.utils import timezone
from django.contrib.staticfiles.storage import staticfiles_storage as static
import os
import json

from .models import Shitpost, Post_Comment
from modules.text_generator import sentence_generator
from modules.image_generator import image_generator

# @permission_required('')
def generate_post(request):
    """
    Generates shitpost.
    """
    sp = Shitpost(text_post=generate_text(),
                  image=generate_image())
    sp.save()
    return render(request, 'shitposts/index.html')

def generate_text():
    """
    NLP Markov-chain text generation.
    """
    src_path = static.path('nlp/post_compilation.json')
    with open(src_path) as post_comp:
        ngrams = json.load(post_comp)
        gen = sentence_generator(ngrams)
        return gen().encode('utf-8')


def generate_image():
    """
    Generates original image
    """
    bkgd_path = static.path('images/src/bkgd')
    back_overlay_path = static.path('images/src/back overlays')
    overlay_path = static.path('images/src/')
    vector_path = static.path('images/src/vectors')
    dest_path = static.path('images/gen')
    gen = image_generator(bkgd_path, back_overlay_path, overlay_path, vector_path, dest_path)
    return gen()


class IndexView(generic.ListView):
    template_name = 'shitposts/index.html'
    context_object_name = 'post_list'
    paginate_by = 5

    def get_queryset(self):
        """
        Return the last four published posts (not including those set to be
        published in the future).
        """
        return Shitpost.objects.filter(
            created_on__lte=timezone.now()
        ).order_by('-created_on')
        # [:4]


class DetailView(generic.DetailView):
    model = Shitpost
    template_name = 'shitposts/detail.html'

    def get_queryset(self):
        """
        Only display posts published in the past.
        """
        return Shitpost.objects.filter(
            created_on__lte=timezone.now()
        )


    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(DetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet to get comments
        comments = Post_Comment.objects.all().filter(shitpost=context['shitpost'])
        context['comments'] = comments
        return context        


# def vote(request, shitpost_id):
#     return HttpResponse("Voting on shitpost #%s" % shitpost_id)


# def index(request):
#     post_list = Shitpost.objects.filter(
#         created_on__lte=timezone.now()
#     ).order_by('-created_on')[:4]
#     context = {
#         'post_list': post_list,
#     }
#     return render(request, 'shitposts/index.html', context)


# def detail(request, shitpost_id):
#     post = get_object_or_404(Shitpost, id=shitpost_id)
#     comments = Post_Comment.objects.all().filter(shitpost=shitpost_id)
#     context = {
#         'id': post.id,
#         'text_post': post.text_post,
#         'image': post.image,
#         'upvotes': post.upvotes,
#         'created_on': post.created_on,
#         'comments': comments
#     }
#     return render(request, 'shitposts/detail.html', context)

