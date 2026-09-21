from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils import timezone
from django.db.models import F
from blog.models import Post, Comment
from blog.forms import CommentForm
from django.contrib import messages


def blog_view(request, **kwargs):
    posts = Post.objects.filter(
        status=1,
        published_date__lte=timezone.now())
    if kwargs.get('cat_name') != None:
        posts = posts.filter(category__name=kwargs['cat_name'])
    if  kwargs.get('author_username') != None:
        posts = posts.filter(author__username=kwargs['author_username'])    
    if  kwargs.get('tag_name') != None:
        posts = posts.filter(tag__name__in=[kwargs['tag_name']])    
    posts = Paginator(posts, 3)  
    try:
        page_number = request.GET.get('page')  
        posts = posts.page(page_number)
    except PageNotAnInteger:
        posts = posts.get_page(1)
    except EmptyPage:
        posts = posts.get_page(1)
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)


def blog_single(request, pid):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Your comment submited successfully')
            return redirect('blog:single', pid=pid)
        else:
            messages.add_message(request, messages.ERROR, 'Your comment did not submited')   
    posts = Post.objects.filter(
        status=1,
        published_date__lte=timezone.now())
    post = get_object_or_404(posts, pk=pid)
    comments = Comment.objects.filter(post=post.id, approved=True)
    Post.objects.filter(pk=post.pk).update(counted_view=F('counted_view') + 1)
    post.refresh_from_db
    posts = list(posts)
    current_index = posts.index(post)
    previous_post = posts[current_index - 1] if current_index > 0 else None
    next_post = posts[current_index + 1] if current_index < len(posts) - 1 else None
    form = CommentForm
    context = {
        'post': post,
        'previous_post': previous_post,
        'next_post': next_post,
        'comments': comments,
        'form': form
    }
    return render(request, 'blog/blog-single.html', context)


def blog_category(request, cat_name):
    posts = Post.objects.filter(status=1)
    posts = posts.filter(category__name=cat_name)
    context = {'posts':posts}
    return render(request, 'blog/blog-home.html', context)


def blog_search(request):
    # print(request.__dict__)
    posts = Post.objects.filter(
        status=1,
        published_date__lte=timezone.now())
    if request.method == 'GET':
        if s:= request.GET.get('s'):
            posts = posts.filter(content__contains=s)      
    context = {'posts': posts}
    return render(request, 'blog/blog-home.html', context)



def test(request):
    return render(request, 'test.html')
