from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include

from blogapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("accounts.urls")),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('', views.home), 
    path('list/' ,views.List_view.as_view()),
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),
    path('create/' ,views.Create_view.as_view()),
    path('detail/<int:id>/' , views.Detail_view.as_view()),
    path('edit/<int:id>/' , views.Edit_view.as_view()),
    path('delete/<int:id>/' , views.Delete_view.as_view()),
    path('like/<int:id>/', views.like_blog, name='like'),
    path("comment/update/<int:id>/", views.update_comment, name="update_comment"),
    path('comment/delete/<int:id>/', views.DeleteCommentView.as_view(), name='delete_comment'),
    path("logout/",auth_views.LogoutView.as_view(next_page="/list/"),name="logout",),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL ,document_root = settings.MEDIA_ROOT)
