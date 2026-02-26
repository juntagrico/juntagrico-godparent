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
    path('manage/match', views.MatchView.as_view(), name='manage-match'),
    path('manage/matched', views.MatchedView.as_view(), name='manage-matched'),
    path('manage/unmatchable', views.UnmatchableView.as_view(), name='manage-unmatchable'),
    path('manage/unmatch/<int:godchild_id>', views.unmatch, name='manage-unmatch'),
    path('manage/completed', views.CompletedView.as_view(), name='manage-completed'),
    path('contact/<int:member_id>', views.contact_member, name='contact-member'),
    path('contact', views.contact_members, name='contact'),
]
