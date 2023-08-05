from django.conf import settings
from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

from andablog.sitemaps import EntrySitemap

from profiles.sitemaps import UserProfileSitemap

admin.autodiscover()

sitemaps = {
    'profiles': UserProfileSitemap,
    'blog': EntrySitemap,
}

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='home.html')),
    url(r'^accounts/', include('allauth.urls')),  # All Auth
    url(r'^blog/', include('blog.urls')),
    url(r'^profile/', include('profiles.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^comments/', include('django_comments.urls')),

    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # Static media hosting in debug mode

if settings.DEBUG:
    import debug_toolbar
    urlpatterns.append(url(r'^__debug__/', include(debug_toolbar.urls)))
