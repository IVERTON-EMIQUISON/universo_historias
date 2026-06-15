from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.stories.urls', namespace='stories')),
    path('autor/', include('apps.author.urls', namespace='author')),
    path('conta/', include('apps.accounts.urls', namespace='accounts')),
    path('loja/', include('apps.store.urls', namespace='store')),
    path('premium/', include('apps.premium.urls', namespace='premium')),
    path('blog/', include('apps.blog.urls', namespace='blog')),
    path('painel/', include('apps.dashboard.urls', namespace='dashboard')),
    
    # API REST
    path('api/v1/', include([
        path('auth/', include('apps.accounts.api_urls')),
        path('stories/', include('apps.stories.api_urls')),
        path('store/', include('apps.store.api_urls')),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)