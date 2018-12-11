from datetime import datetime
from django.shortcuts import redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import *
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from blog.models import Post
from django.template.loader import render_to_string
# Create your views here.
def post_list(request):
    posts = Post.published.all()
    query = request.GET.get('q')
    # print(query)
    if query:
        posts = Post.published.filter(
            Q(title__icontains=query) |
            Q(author__username__icontains=query) |
            Q(body__icontains=query)
        )
    context = {
        "posts":posts,
    }
    return render(request,'blog/post_list.html',context)

@login_required
def user_posts(request):
    user = None
    try:
        user = User.objects.get(username=request.user.username)
    except:
        return HttpResponse("No user with this id")
    posts = Post.objects.filter(author=user,status__exact="published")
    context = {
        'posts':posts,
    }
    return render(request,"blog/my_posts.html",context)

@login_required
def user_drafts(request):
    user = None
    try:
        user = User.objects.get(username=request.user.username)
    except:
        return HttpResponse("No user with this id")
    posts = Post.objects.filter(author=user,status__exact="draft")
    context = {
        'posts':posts,
    }
    return render(request,"blog/my_drafts.html",context)

def post_detail(request, id, slug):
    post=get_object_or_404(Post,id=id,slugthing=slug)
    comments = Comment.objects.filter(post=post).order_by('-id')
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(user=request.user,content=content,post=post)
            comment.save()
            return HttpResponseRedirect(post.get_absolute_url())
    else:
        comment_form = CommentForm()
    # post.comment_set.all().order_by('-id')
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True
    context = {
        'post': post,
        'is_liked':is_liked,
        'comments':comments,
        'total_likes':post.total_likes(),
        'comment_form':comment_form,
    }
    return render(request, 'blog/post_detail.html' ,context)

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostCreationForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('blog:post_list')
    else:
        form = PostCreationForm()
    context = {
        'form': form,
    }
    return render(request,'blog/post_create.html',context)


def user_logout(request):
    logout(request)
    return redirect('blog:post_list')



@login_required
def like_post(request):
    post = get_object_or_404(Post,id = request.POST.get('id'))
    is_liked = True
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes':post.total_likes(),
    }
    if request.is_ajax():
        html = render_to_string('blog/like_section.html',context,request=request)
        return JsonResponse({'form':html})

def post_edit(request, id):
    print('check 1')
    post = get_object_or_404(Post, id=id)
    print('check 2')
    if post.author != request.user:
        return HttpResponse("Not your post to Edit")
    if request.method == 'POST':
        print('check 3')
        form = PostEditForm(request.POST,instance=post)
        print('check 4')
        if form.is_valid():
            form.save()
            return redirect(post.get_absolute_url())
    else:
        form = PostEditForm(instance=post)
    context = {
        'form':form,
        'post':post,
    }
    return render(request,'blog/post_edit.html',context)

def post_delete(request,id):
    post = get_object_or_404(Post,id=id)
    if request.user != post.author:
        return HttpResponse('It is not your Post to delete')
    post.delete()
    return redirect('blog:post_list')
