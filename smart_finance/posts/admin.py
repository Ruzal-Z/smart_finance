"""Файл админ панели, где регистрируются модели"""

from django.contrib import admin

from .models import Comment, Follow, Group, Post


class PostAdmin(admin.ModelAdmin):
    """Регистрация модели Post"""

    list_display = ('pk', 'text', 'group', 'pub_date', 'author', 'image')
    list_editable = ('group',)
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Post, PostAdmin)


class GroupAdmin(admin.ModelAdmin):
    """Регистрация модели Group"""

    list_display = ('pk', 'title', 'slug', 'description')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title',)
    empty_value_display = '-пусто-'


admin.site.register(Group, GroupAdmin)


class CommentAdmin(admin.ModelAdmin):
    """Регистрация модели Comment"""

    list_display = ('pk', 'post', 'author', 'text', 'created')
    search_fields = ('post',)
    list_filter = ('post',)
    empty_value_display = '-пусто-'


admin.site.register(Comment, CommentAdmin)


class FollowAdmin(admin.ModelAdmin):
    """Регистрация модели Follow"""

    list_display = ('pk', 'user', 'author')
    search_fields = ('author',)
    list_filter = ('author',)
    empty_value_display = '-пусто-'


admin.site.register(Follow, FollowAdmin)
