from django.urls import path
from .views import groups, group

urlpatterns = [
    path('<str:group_name>', group, name='group_chat'),
    path('', groups, name='groups')
]
