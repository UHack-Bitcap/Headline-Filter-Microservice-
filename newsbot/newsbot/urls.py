from django.conf.urls import patterns, include, url
from django.contrib import admin
import headlineclassifier.views as v 

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'newsbot.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^check$',v.check,name="check"),
)
