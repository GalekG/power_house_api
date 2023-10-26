from django.urls import path
from gym.views import users_views, machines_views


urlpatterns = [
    path('users/', users_views.user_list, name='users.list'),
    path('users/create/', users_views.create_user, name='users.create'),
    path('users/<int:user_id>/', users_views.user_detail, name='users.getById'),
    path('users/<int:user_id>/update/', users_views.update_user, name='users.update'),
    path('users/<int:user_id>/delete/', users_views.delete_user, name='users.delete'),
    path('machines/', machines_views.machine_list, name='machines.list'),
    path('machines/create/', machines_views.create_machine, name='machines.create'),
    path('machines/<int:machine_id>/', machines_views.machine_detail, name='machines.getById'),
    path('machines/<int:machine_id>/update/', machines_views.update_machine, name='machines.update'),
    path('machines/<int:machine_id>/delete/', machines_views.delete_machine, name='machines.delete'),

]

