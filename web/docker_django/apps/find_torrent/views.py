import json
import logging
import re
import os
from urllib.parse import urlparse

from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render, render_to_response
from django_tables2 import RequestConfig
from haystack.inputs import AutoQuery, Clean
from haystack.query import SearchQuerySet
from django.db.models import F

from .forms import TorrentSearchForm
from .models import Torrent, Trend
from .tables import TorrentTable

from redis import Redis


redis = Redis(host=os.environ['REDIS_HOST'], port=6379, password=os.environ['REDIS_PSWD'], db=2)

# Get an instance of a logger
logging.basicConfig(format='%(asctime)s %(message)s', filename='search.log')
logger = logging.getLogger(__name__)

# Create your views here.


# searchqueryset to queryset
def sqs_to_qs(search_qs):
    for item in search_qs:
        yield item.object


def index(request):
    return render_to_response('find_torrent/index.html')


def torrent_search_form(request):

    q = Clean(request.GET.get('q', '')).__str__().lower()
    print(q)
    q = q.replace(' ', '_')
    if len(q) >= 2:
        return redirect('/torrents/{}'.format(q))

    form = TorrentSearchForm(request.GET)
    torrents = form.search()[:50]

    # print(torrents)
    context = {
        'torrents': torrents,
        'get': request.GET,
    }
    # print(context)

    logger.info(request.GET)
    # return render_to_response('find_torrent/torrents.html', context)
    return render_to_response('find_torrent/torrent_search.html', context)


def url_parse_search(request, trend):
    # if trend != slugify(trend):
    #     print(slugify(trend))
    #     return redirect('/torrent/{}'.format(slugify(trend)))

    trend = Clean(trend).__str__().replace('_', ' ')
    # redis.incr(trend)
    print(trend)

    try:
        Trend.objects.create(title=trend, priority=1)
    except Exception as e:
        Trend.objects.filter(title=trend).update(priority=F('priority')+1)

    # get q in Elastic
    torrents = SearchQuerySet().values('pk').filter(title=AutoQuery(trend))[:200]
    # torrents = SearchQuerySet().values('pk').filter(content=trend)[:200]

    # fields include
    values = ('id', 'title', 'provider', 'provider_url', 'peers', 'seeds', 'complete', 'magnet')

    # Elastic return list to django SQS
    torrents = [i['pk'] for i in torrents]
    torrents = Torrent.objects.values(*values).filter(pk__in=torrents)

    # SQS to table (django-table2)
    torrents = TorrentTable(torrents)

    RequestConfig(request).configure(torrents)
    torrents.paginate(page=request.GET.get('page', 1), per_page=20)

    context = {
        'torrents': torrents,
        'trend': trend
    }

    logger.info(request.GET)
    return render(request, 'find_torrent/torrents.html', context)


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:10]
    suggestions = [result.title for result in sqs]

    q = [request.GET.get('q', '')]

    # split word in suggestions and find most match word
    s = set()
    s_all = []

    for i in suggestions:
        splited_suggestion = re.split('\.|-| |_', i.lower())
        s.update(set(splited_suggestion))
        s_all.extend(splited_suggestion)

    d = {}
    for i in s:
        if len(i) >= len(q[0]) and s_all.count(i) > 2:
            d[i] = s_all.count(i)

    most_match = [i[0] for i in sorted(d.items(), key=lambda x: x[1], reverse=True)]

    # suggestions include q and most_match
    suggestions = most_match + suggestions
    # print(suggestions)

    suggestions = [{'title': i} for i in suggestions]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps(suggestions)
    return HttpResponse(the_data, content_type='application/json')

"""
def stats(request):

    path = Clean(urlparse(request.META['HTTP_REFERER']).path).__str__()
    trend = path.split('/')[-1].replace('_', ' ')

    redis.incr(trend)
    # try:
    #     Trend.objects.create(title=trend, priority=1)
    # except Exception as e:
    #     Trend.objects.filter(title=trend).update(priority=F('priority')+1)

    return HttpResponse("ok", content_type='application/json')
"""