from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import Http404, HttpResponseRedirect
from blog.models import Article, Tag, Author, Category
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger


def blog_list(request):
    blog_list = Article.objects.all().order_by('-publish_time')
    tags = Tag.objects.all()
    categories = Category.objects.all()

    paginator = Paginator(blog_list, 5)
    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        blogs = paginator.page(1)
    except EmptyPage:
        blogs = paginator.page(paginator.num_pages)

    return render_to_response('blog/blog_list.html',
           {"blogs": blogs, "tags": tags, "categories": categories}, context_instance=RequestContext(request))

def index(request):

    return render_to_response('blog/index.html',{},context_instance = RequestContext(request))

def profile(request):

    return render_to_response('blog/profile.html',{},context_instance = RequestContext(request))

def blog_del(request, id=""):
    try:
        blog = Article.objects.get(id=id)
    except Exception:
        raise Http404
    if blog:
        blog.delete()
        return HttpResponseRedirect("/blog/bloglist/")
    blogs = Article.objects.all()
    return render_to_response("blog/blog_list.html", {"blogs": blogs})


def blog_show(request, id=''):
    try:
        blog = Article.objects.get(id=id)
        tags = Tag.objects.all()
        categories = Category.objects.all()
    except Article.DoesNotExist:
        raise Http404
    return render_to_response("blog/blog_show.html",
           {"blog": blog, "tags": tags, "categories": categories}, context_instance=RequestContext(request))


def blog_filter(request, id=''):
    tags = Tag.objects.all()
    tag = Tag.objects.get(id=id)
    blogs = tag.article_set.all().order_by('-publish_time')
    return render_to_response("blog/blog_filter.html", {"blogs": blogs, "tag": tag, "tags": tags})


def blog_category(request, id=''):
    categories = Category.objects.all()
    category = Category.objects.get(id=id)
    blogs = Article.objects.filter(category=category)
    return render_to_response("blog/blog_category_filter.html", {"blogs": blogs, "category": category, "categories": categories})


def blog_show_comment(request, id=''):
    blog = Article.objects.get(id=id)
    return render_to_response('blog/blog_comments_show.html', {"blog": blog})


def blog_search(request):
    tags = Tag.objects.all()
    if 'search' in request.GET:
        search = request.GET['search']
        blogs = Article.objects.filter(caption__icontains=search).order_by('-publish_time')
        categories = Category.objects.all()
        return render_to_response('blog/blog_search.html',
            {"blogs": blogs, "tags": tags, "categories": categories}, context_instance=RequestContext(request))
    else:
        blogs = Article.objects.order_by('-id')
        return render_to_response("blog/blog_list.html", {"blogs": blogs, "tags": tags},
            context_instance=RequestContext(request))