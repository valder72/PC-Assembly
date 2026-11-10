from django.urls import path
from catalog import views

urlpatterns = [
    path('categories/', views.CategoryList.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('manufacturers/', views.ManufacturerList.as_view(), name='manufacturer-list'),
    path('manufacturers/<int:pk>/', views.ManufacturerDetail.as_view(), name='manufacturer-detail'),
    path('parts/', views.PartList.as_view(), name='part-list'),
    path('parts/<int:pk>/', views.PartDetail.as_view(), name='part-detail'),
]