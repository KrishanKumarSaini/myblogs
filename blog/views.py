from django.shortcuts import render, redirect, get_object_or_404
from .forms import PostForm, EmailPostForm, CommentForm
from .models import post, Author, Comments
from django.db.models import Count, Q
from django.core.mail import send_mail
from myblogs.settings import EMAIL_HOST_USER
from taggit.models import Tag

def get_author(user):
    author = Author.objects.filter(user=user)
    if author.exists():
        return author[0]
    return None

def home(request):
    author = get_author(request.user)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    context = {
        'form': form
    }
    return render(request, 'blog/base.html', context)

def display(request, tag_slug=None):
    p = post.objects.filter(status='published').order_by('-updated')
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        p = p.filter(tags__in=[tag])
    
    context = {
        'posts': p,
        'tag': tag
    }
    return render(request, 'blog/main.html', context)

def profile(request):
    logged_in_user = request.user
    author = Author.objects.filter(user=logged_in_user)
    p = post.objects.filter(status='published', author=author[0]).order_by('-updated')[:6]
    context = {
        'posts': p
    }

    return render(request, 'blog/profile/profile.html', context)

def search(request):
    query = request.GET.get('search', None)
    blog_lists = post.objects.none()
    blog_list = post.objects.none()

    if query:
        blog_list = post.objects.filter(title__istartswith=query)
        """
        user.username->query
        Author<-user.instance
        post<-Author.instance        
        """
        blog_content_list = post.objects.filter(content__istartswith=query)
        blog_lists = (blog_list | blog_content_list).distinct()
    
    context = {
        'posts': blog_lists
    }
    return render(request, 'blog/search.html', context)    

def post_share(request, id):
    get_post = get_object_or_404(post, id=id)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            to = form.cleaned_data['to']
            subject = form.cleaned_data['subject']
            Email = EMAIL_HOST_USER
            msg = "Title: " + get_post.title + "\nAuthor: " + get_post.author.user.username + "\nBlog: " + get_post.content
            send_mail(subject, msg, Email, [to])
            sent = True
    else:
        form = EmailPostForm()

    context = {
        #'get_post': get_post,
        'form': form,
        'sent': sent
    }

    return render(request, 'blog/share.html', context)


def detail(request):
    id = request.GET.get('id')
    get_post = get_object_or_404(post, id=id)
    comment = Comments.objects.filter(posts=get_post, active=True)
    new_comment = None
    
    #getting data from comment post
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if  comment_form.is_valid():
            new_comment = comment_form.save(commit=False)

            new_comment.posts = get_post

            new_comment.save()
            
    else:
        comment_form = CommentForm()

    #List of similar posts
    post_tags_ids = post.objects.filter(id=get_post.id).values_list('tags', flat=True)
    similar_posts = post.objects.filter(tags__in=post_tags_ids).exclude(id=get_post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:4]
    
    context = {
        'post': get_post,
        'comment': comment,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'similar_posts': similar_posts,
    }

    return render(request, 'blog/detail.html', context)

def update(request, id):
    p = get_object_or_404(post, id=id)
    form = PostForm(request.POST or None, request.FILES or None, instance=p)        
    author = get_author(request.user)

    if request.method == "POST":

        if form.is_valid():
            form.instance.author = author
            form.save()
            
            return redirect('/blogs')
    
    context = {
        'form': form
    }
    return render(request, 'blog/update.html', context)

def delete(request, id):
    post.objects.filter(id=id).delete()
    return redirect('/blogs')
 