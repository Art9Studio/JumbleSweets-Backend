from django.conf import settings
from django.conf.urls import include, url
from django.urls import path
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.contrib.staticfiles.views import serve
from django.views.decorators.csrf import csrf_exempt
from django.views.i18n import JavaScriptCatalog, set_language

from jumblesweets.account.urls import urlpatterns as account_urls
from jumblesweets.checkout.urls import (
    cart_urlpatterns as cart_urls, checkout_urlpatterns as checkout_urls)
from jumblesweets.core.sitemaps import sitemaps
from jumblesweets.core.urls import urlpatterns as core_urls
from jumblesweets.dashboard.urls import urlpatterns as dashboard_urls
from jumblesweets.data_feeds.urls import urlpatterns as feed_urls
from jumblesweets.graphql.api import schema
from jumblesweets.graphql.file_upload.views import FileUploadGraphQLView
from jumblesweets.order.urls import urlpatterns as order_urls
from jumblesweets.page.urls import urlpatterns as page_urls
from jumblesweets.product.urls import urlpatterns as product_urls
from jumblesweets.search.urls import urlpatterns as search_urls

handler404 = 'jumblesweets.core.views.handle_404'

non_translatable_urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    url(r'^dashboard/',
        include((dashboard_urls, 'dashboard'), namespace='dashboard')),
    url(r'^graphql/', csrf_exempt(FileUploadGraphQLView.as_view(
        schema=schema, graphiql=settings.DEBUG)), name='api'),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^i18n/$', set_language, name='set_language'),
    url('', include('social_django.urls', namespace='social'))]

translatable_urlpatterns = [
    url(r'^', include(core_urls)),
    url(r'^cart/', include((cart_urls, 'cart'), namespace='cart')),
    url(r'^checkout/',
        include((checkout_urls, 'checkout'), namespace='checkout')),
    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    url(r'^order/', include((order_urls, 'order'), namespace='order')),
    url(r'^page/', include((page_urls, 'page'), namespace='page')),
    url(r'^products/',
        include((product_urls, 'product'), namespace='product')),
    url(r'^account/',
        include((account_urls, 'account'), namespace='account')),
    url(r'^feeds/',
        include((feed_urls, 'data_feeds'), namespace='data_feeds')),
    url(r'^search/', include((search_urls, 'search'), namespace='search')),
    url(r'', include('payments.urls'))]

urlpatterns = non_translatable_urlpatterns + i18n_patterns(
    *translatable_urlpatterns)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
        # static files (images, css, javascript, etc.)
        url(r'^static/(?P<path>.*)$', serve)] + static(
            settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.ENABLE_SILK:
    urlpatterns += [
        url(r'^silk/', include('silk.urls', namespace='silk'))]

# from django.conf import settings
# from django.urls import include, path
# from django.conf.urls.static import static
# from django.contrib import admin
# from django.views.generic import TemplateView
# from django.views import defaults as default_views
#
# urlpatterns = [
#     path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
#     path(
#         "about/",
#         TemplateView.as_view(template_name="pages/about.html"),
#         name="about",
#     ),
#     # Django Admin, use {% url 'admin:index' %}
#     path(settings.ADMIN_URL, admin.site.urls),
#     # User management
#     path(
#         "users/",
#         include("jumblesweets.users.urls", namespace="users"),
#     ),
#     path("accounts/", include("allauth.urls")),
#     # Your stuff: custom urls includes go here
# ] + static(
#     settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
# )
#
# if settings.DEBUG:
#     # This allows the error pages to be debugged during development, just visit
#     # these url in browser to see how these error pages look like.
#     urlpatterns += [
#         path(
#             "400/",
#             default_views.bad_request,
#             kwargs={"exception": Exception("Bad Request!")},
#         ),
#         path(
#             "403/",
#             default_views.permission_denied,
#             kwargs={"exception": Exception("Permission Denied")},
#         ),
#         path(
#             "404/",
#             default_views.page_not_found,
#             kwargs={"exception": Exception("Page not Found")},
#         ),
#         path("500/", default_views.server_error),
#     ]
#     if "debug_toolbar" in settings.INSTALLED_APPS:
#         import debug_toolbar
#
#         urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
