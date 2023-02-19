from django.contrib import admin
from .models import Article, Person, Comment


admin.site.register(Article)
admin.site.register(Person)
admin.site.register(Comment)
