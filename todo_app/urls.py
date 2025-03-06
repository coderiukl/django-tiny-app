from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.home, name='home'),
    path('signin/',views.signin, name='signin'),
    path('signup/',views.signup, name='signup'),
    path('logout/',views.logout_view, name='logout'),
    path('add_task/',views.add_task, name='add'),
    path('archieved/',views.archieve_task, name='archieved'),
    path('deleted/',views.delete_task, name='deleted'),
    path('<int:pk>/edit/',views.update_task, name='update'),
    path('empty_recycle_bin/', views.empty_recycle_bin, name='empty_recycle_bin'),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

