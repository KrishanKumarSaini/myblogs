from django.contrib import admin
from .models import post, Author, Comments

admin.site.register(post)
admin.site.register(Author)

@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'posts', 'created_on', 'active')
    list_filter = ('active', 'created_on', 'updated_on')
    search_fields = ('name', 'body')
