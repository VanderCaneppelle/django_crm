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
    path('delete_tournament/<int:pk>',
         views.delete_tournament, name='delete_tournament'),
    path('update_tournament/<int:pk>',
         views.update_tournament, name='update_tournament'),

    path('tournament/<int:pk>/create_teams/',
         views.create_teams, name='create_teams'),

    path('tournament/<int:pk>/get_teams_data/',
         views.get_teams_data, name='get_teams_data'),

    path('gen_1_phase_matches/<int:pk>',
         views.gen_1_phase_matches, name='gen_1_phase_matches'),

    path('save_match_scores/<int:pk>/',
         views.save_match_scores, name='save_match_scores'),







]
