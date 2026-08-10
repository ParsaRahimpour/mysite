from django.shortcuts import render, get_object_or_404
from blog.models import Post

def blog_view(request):
    posts = Post.objects.filter(status=1)
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)

# def blog_single(request, pid):
#     posts = Post.objects.filter(status=1)
#     post = get_object_or_404(posts, pk=pid)
#     context = {'post':post}
#     return render(request, 'blog/blog-single.html', context)


def blog_single(request, pid):
    posts = Post.objects.filter(status=1)
    post = get_object_or_404(posts, pk=pid)
    posts = list(posts)
    current_index = posts.index(post)
    previous_post = posts[current_index - 1] if current_index > 0 else None
    next_post = posts[current_index + 1] if current_index < len(posts) - 1 else None
    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
    }
    return render(request, 'blog/blog-single.html', context)


def test(request, pid):
    # post = Post.objects.all()
    post = get_object_or_404(Post, pk=pid)
    context = {'post':post}
    return render(request, 'test.html', context)
