from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from simple21.models import Page, SearchLog, GlobalConfig


def index(request):
    template = loader.get_template('simple21/index.html')
    query = get_query_from_request(request)
    queryset = get_queryset(query)
    create_search_log(request, query, queryset)
    return HttpResponse(template.render(dict(queryset=queryset), request))

def create_search_log(request, query, queryset):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = GlobalConfig.get().anonymous_user
    SearchLog.objects.create(query=query, user=user, result_count=queryset.count())

def get_query_from_request(request):
    if not request.GET:
        return ''
    return request.GET.get('q', '')

def get_queryset(query):
    return Page.objects.filter(Q(name__icontains=query)|Q(text__icontains=query)).distinct()

def page(request, id):
    template = loader.get_template('simple21/page.html')
    page = Page.objects.get(id=id)
    return HttpResponse(template.render(dict(page=page), request))
