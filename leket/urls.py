from django.urls import path
from . import views
from . views import LoginUserView
from django.contrib.auth import views as auth_views
urlpatterns = [
path('', views.shtepia, name='shtepia'),
    path('fitimet/', views.fitimet_list, name='fitimet_list'),
    path('fitimet/krijo/', views.krijoardhuraCreateView.as_view(), name='krijo_ardhura'),
    path('fitimet/redakto/<int:pk>/', views.redaktoardhuraUpdateView.as_view(), name='redakto_ardhura'),
    path('fitimet/fshi/<int:pk>/', views.fshiardhuraDeleteView.as_view(), name='fshi_ardhura'),
    #shpzimet urls
    path('shpenzimet/', views.shpenzimet_list, name='shpenzimet_list'),
    path('shpenzimet/krijo/', views.KrijoShpenzimeCreateView.as_view(), name='krijo_shpenzime'),
    path('shpenzimet/redakto/<int:pk>/', views.RedaktoShpenzimeUpdateView.as_view(), name='redakto_shpenzime'),
    path('shpenzimet/fshi/<int:pk>/', views.FshiShpenzimeDeleteView.as_view(), name='fshi_shpenzime'),
    path('statistikat/', views.statistikat, name='statistikat'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]