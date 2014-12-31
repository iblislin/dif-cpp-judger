from django.conf.urls import patterns, url


urlpatterns = patterns('judge.views',
    url(r'^list(?:/(\d+))?/$', 'list', name='list'),
    url(r'^detail(?:/(?P<qid>\d+))?/$', 'detail', name='detail'),
    url(r'^upload(?:/(?P<qid>\d+))?/$', 'upload', name='upload'),
    url(r'^result(?:/(?P<code_id>\d+))?/$', 'result', name='result'),
)
