# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Shitpost, Post_Comment

class ShitpostAdmin(admin.ModelAdmin):
	list_filter = ['created_on']
	search_fields = ['text_post']


class CommentAdmin(admin.ModelAdmin):
	list_filter = ['created_on']
	search_fields = ['comment_content', ]
					 # 'user_email', 
					 # 'username' ]


admin.site.register(Shitpost, ShitpostAdmin)
admin.site.register(Post_Comment, CommentAdmin)