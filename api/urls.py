from django.urls import path
from . import views

urlpatterns = [
    path('goods/', views.good_list),
    path('goods/<int:id>', views.good_detail)
]