# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils import timezone

class Shitpost(models.Model):
    text_post = models.TextField()
    image = models.TextField()
    upvotes = models.IntegerField(default=0)
    created_on = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return ("Text: " + self.text_post + "\n" +
                "File: " + self.image + "\n" +
                "Upvotes: " + str(self.upvotes) + "\n" +
                "Date: " + self.created_on.strftime('%Y-%m-%d %H:%M:%S') + "\n")


class Post_Comment(models.Model):
    shitpost = models.ForeignKey(
        Shitpost, 
        on_delete=models.CASCADE,
        verbose_name="reference post")
    # user_email = models.EmailField(unique=True)
    # username = models.User()
    comment_content = models.TextField()
    created_on = models.DateTimeField(default=timezone.now) 
    updated_on = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return ("Post: " +  str(self.shitpost.id) + "\n" +
                # "Author: " + self.username + "\n" +
                "Comment: " + self.comment_content + "\n" +
                "Created on: " + self.created_on.strftime('%Y-%m-%d %H:%M:%S') + "\n" +
                "Updated on: " + ("N/A" if not self.updated_on else self.updated_on.strftime('%Y-%m-%d %H:%M:%S')) + "\n")


# class Votelog(models.Model):
    # user_email = models.EmailField(
    #   default=request.User if request.User else None)
    # shitpost = models.ForeignKey(
    #   Shitpost,
    #   on_delete=models.CASCADE,
    #   verbose_name="reference post")
    # is_upvote = models.Boolean(default=True)