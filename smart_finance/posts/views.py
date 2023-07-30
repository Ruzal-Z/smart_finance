"""Представления приложения Posts"""
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

from .forms import CommentForm, PostForm
from .models import Comment, Follow, Group, Post, User
from .utils import get_page


@cache_page(20)
@vary_on_cookie
def index(request):
    """View-функция для главной страницы"""
    return render(
        request,
        'posts/index.html',
        {'page_obj': get_page(Post.objects.all(), request)},
    )


def group_posts(request, slug: str):
    """View-функция для страницы сообщества"""
    group = get_object_or_404(Group, slug=slug)
    return render(
        request,
        'posts/group_list.html',
        {
            'group': group,
            'page_obj': get_page(group.posts.all(), request),
        },
    )


def profile(request, username: str):
    """View-функция для страницы пользователья"""
    author = get_object_or_404(User, username=username)
    context = {
        'author': author,
        'following': request.user.is_authenticated
        and (
            author != request.user
            and Follow.objects.filter(
                user=request.user, author=author
            ).exists()
        ),
        'page_obj': get_page(
            author.posts.all(),
            request,
        ),
        'author_posts_comments_count': Comment.objects.filter(
            post__author=author
        ).count(),
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request: str, post_id: int):
    """View-функция для страницы с деталями поста"""
    return render(
        request,
        'posts/post_detail.html',
        {
            'post': get_object_or_404(Post, pk=post_id),
            'form': CommentForm(request.POST or None),
        },
    )


@login_required
def post_create(request: str):
    """View-функция для страницы создания поста"""
    form = PostForm(request.POST or None, files=request.FILES or None)
    if not form.is_valid():
        return render(request, 'posts/create_post.html', {'form': form})
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', username=request.user)


@login_required
def post_edit(request: str, post_id: int):
    """View-функция для страницы редактирования поста"""
    post = get_object_or_404(Post, pk=post_id)
    if post.author != request.user:
        return redirect('posts:post_detail', post_id=post.pk)
    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post.pk)
    return render(
        request, 'posts/create_post.html', {'form': form, 'is_edit': True}
    )


@login_required
def post_delete(request: str, post_id: int):
    """
    Удаляет пост с указанным ID и перенаправляет пользователя на его профиль.
    """
    get_object_or_404(Post, pk=post_id).delete()
    return redirect('posts:profile', request.user)


@login_required
def add_comment(request, post_id):
    """View-функция для страницы добавления комментария"""
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('posts:post_detail', post_id=post_id)
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    """View-функция для страницы отображения постов, избранных авторов"""
    return render(
        request,
        'posts/follow.html',
        {
            'page_obj': get_page(
                Post.objects.filter(author__following__user=request.user),
                request,
            )
        },
    )


@login_required
def profile_follow(request, username):
    """View-функция подписки на автора"""
    if request.user.username != username:
        Follow.objects.get_or_create(
            user=request.user,
            author=get_object_or_404(User, username=username),
        )
    return redirect('posts:profile', username=username)


@login_required
def profile_unfollow(request, username):
    """View-функция отписки на автора"""
    get_object_or_404(
        Follow, user=request.user, author__username=username
    ).delete()
    return redirect("posts:profile", username=username)
