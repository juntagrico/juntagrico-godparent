from django.urls import path
from juntagrico_godparent import views

app_name = 'jgo'
urlpatterns = [
    # member urls
    path('home', views.home, name='home'),
    path('godparent', views.godparent_signup, name='godparent'),
    path('godparent/increment', views.increment_max_godchildren, name='increment-max-godchildren'),
    path('godchild', views.godchild_signup, name='godchild'),
    path('arranged/<int:godchild_id>', views.arranged, name='arranged'),
    path('done/<int:godchild_id>', views.done, name='done'),
    path('leave', views.leave, name='leave'),

    # admin urls
    path('manage/match', views.match, name='manage-match'),
    path('manage/matched', views.matched, name='manage-matched'),
    path('manage/matched/removed', views.matched, {'removed': True}, name='manage-matched-removed'),
    path('manage/unmatchable', views.unmatchable, name='manage-unmatchable'),
    path('manage/unmatch/<int:godchild_id>', views.unmatch, name='manage-unmatch'),
    path('manage/completed', views.completed, name='manage-completed'),
    path('contact/<int:member_id>', views.contact, name='contact'),
]
