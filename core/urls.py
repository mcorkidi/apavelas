
from django.contrib import admin
from django.urls import path, include
from apavelas import views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import TemplateView

urlpatterns = [
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.index, name='index'),
    path('register/<email_id>', user_views.register, name='register'),
    path('pre_register/', user_views.pre_register, name='pre_register'),
    path('profile/', user_views.profile, name='profile'),
    path('logout/', views.LogOutView, name='logout'),
    path('card/', views.card, name='card'),
    path('qrscan/<qrscan>', views.qrscan, name='qrscan'),
    path('members/', views.members, name='members'),
    path('benefits/', views.benefits, name='benefits'),
    path('events/', views.events, name='events'),
    path('places/<type_of_service>', views.places, name='places'),
    # path('gallery/', views.gallery, name='gallery'),
    path('accounting/', views.accounting, name='accounting'),
    path('statement/', views.statement, name='statement'),
    path('market/', views.market, name='market'),
    path('market/new_listing/<category>', views.newListing, name='new_listing'),
    path('category_pick/', views.categoryPick, name='category_pick'),
    path('add_images/<product>', views.addImages, name='add_images'),
    path('market/listing/<product_id>', views.listing, name='listing'),
    path('market/search/<keyword>', views.searchResults, name='search_results'),
    path('market/my_products/', views.myProducts, name='my_products'),
    path('market/edit_listing/<product_id>', views.editListing, name='edit_listing')

]



urlpatterns += [
    # ... the rest of your URLconf goes here ...
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)