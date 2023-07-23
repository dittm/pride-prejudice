from django.urls import path, include
from . import views
from .views import book_list
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='library-home'),
    path('about/', views.about, name='library-about'),
    path('books/', book_list, name='book_list'),
    path('accounts/', include('accounts.urls')),
    path('borrow-book/<str:isbn>/', views.borrow_book, name='borrow_book'),
    path('return-book/<str:isbn>/', views.return_book, name='return_book'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
