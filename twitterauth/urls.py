from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('twitterauth.views',
    url(r'^login/?$', 'twitter_login', name='login'),
    url(r'^logout/?$', 'twitter_logout', name='logout'),
    url(r'^login/authenticated/?$', 'twitter_authenticated',
        name='authenticated'),
)
