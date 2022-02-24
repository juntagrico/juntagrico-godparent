from django.urls import path
from juntagrico_godparent import views

app_name = 'jgo'
urlpatterns = [
    # member urls
    path(app_name + '/home', views.home, name='home'),
    path(app_name + '/godparent', views.godparent, name='godparent'),
    path(app_name + '/godparent/increment', views.increment_max_godchildren, name='increment-max-godchildren'),
    path(app_name + '/godchild', views.godchild, name='godchild'),
    path(app_name + '/leave', views.leave, name='leave'),

    # admin urls
    path(app_name + '/match', views.match, name='match'),
    path(app_name + '/matched', views.matched, name='matched'),
    path(app_name + '/matched/removed', views.matched, {'removed': True}, name='matched-removed'),
    path(app_name + '/unmatchable', views.unmatchable, name='unmatchable'),
    path(app_name + '/unmatch/<int:godchild_id>', views.unmatch, name='unmatch')
]
