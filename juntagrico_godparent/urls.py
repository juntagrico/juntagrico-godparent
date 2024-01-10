from django.urls import path
from juntagrico_godparent import views

app_name = 'jgo'
urlpatterns = [
    # member urls
    path(app_name + '/home', views.home, name='home'),
    path(app_name + '/godparent', views.godparent_signup, name='godparent'),
    path(app_name + '/godparent/increment', views.increment_max_godchildren, name='increment-max-godchildren'),
    path(app_name + '/godchild', views.godchild_signup, name='godchild'),
    path(app_name + '/arranged/<int:godchild_id>', views.arranged, name='arranged'),
    path(app_name + '/done/<int:godchild_id>', views.done, name='done'),
    path(app_name + '/leave', views.leave, name='leave'),

    # admin urls
    path(app_name + '/manage/match', views.match, name='manage-match'),
    path(app_name + '/manage/matched', views.matched, name='manage-matched'),
    path(app_name + '/manage/matched/removed', views.matched, {'removed': True}, name='manage-matched-removed'),
    path(app_name + '/manage/unmatchable', views.unmatchable, name='manage-unmatchable'),
    path(app_name + '/manage/unmatch/<int:godchild_id>', views.unmatch, name='manage-unmatch'),
    path(app_name + '/manage/completed', views.completed, name='manage-completed'),
]
