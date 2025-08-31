from django.urls import path
from . import views
from .upload_views import upload_images, delete_image, get_optimized_url

app_name = 'items'

urlpatterns = [
    path('', views.ItemListView.as_view(), name='item-list'),
    path('create/', views.ItemCreateView.as_view(), name='item-create'),
    path('upload-images/', upload_images, name='upload-images'),
    path('delete-image/', delete_image, name='delete-image'),
    path('optimize-image/', get_optimized_url, name='optimize-image'),
    path('my-items/', views.MyItemsView.as_view(), name='my-items'),
    path('search/', views.search_items, name='search-items'),
    path('<uuid:pk>/', views.ItemDetailView.as_view(), name='item-detail'),
    path('<uuid:pk>/update/', views.ItemUpdateView.as_view(), name='item-update'),
    path('<uuid:pk>/delete/', views.ItemDeleteView.as_view(), name='item-delete'),
]
