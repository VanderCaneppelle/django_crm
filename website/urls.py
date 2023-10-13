from . import views
from django.urls import path


urlpatterns = [
    path('', views.home, name='home'),
    # path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('search_results', views.search_results, name='search_results'),
    path('create_tournament', views.create_tournament, name='create_tournament'),
    path('tournament_list', views.tournament_list, name='tournament_list'),
    path('view_tournament/<int:pk>', views.view_tournament, name='view_tournament'),

]
