from django import template
from ..models import post
from django.db.models import Count

register = template.Library()

@register.simple_tag
def total_posts():
    lp = post.objects.filter(status="published").count()
    return lp

@register.inclusion_tag('latest_posts.html')
def show_latest_posts(count=5):
    p = post.objects.filter(status="published").order_by('-created')[:count]
    print(p)
    return {'p': p}

@register.simple_tag
def get_most_commented_posts(count=5):
    return post.objects.filter(status="published").annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]