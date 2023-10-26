from django.urls import path
from gym.views.users_views import user_list, create_user, user_detail, update_user, delete_user

urlpatterns = [
    path('users/', user_list, name='users.list'),
    path('users/create/', create_user, name='users.create'),
    path('users/<int:user_id>/', user_detail, name='users.getById'),
    path('users/<int:user_id>/update/', update_user, name='users.update'),
    path('users/<int:user_id>/delete/', delete_user, name='users.delete'),
]

