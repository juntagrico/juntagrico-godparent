from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.urls import reverse_lazy
from django.views.generic import ListView
from juntagrico.entity.member import Member
from juntagrico.view_decorators import highlighted_menu
from juntagrico.views.email import email_view

from juntagrico_godparent.forms import GodparentForm, GodchildForm, ContactForm

from juntagrico_godparent.models import Godchild, Godparent
from juntagrico_godparent import signals
from juntagrico_godparent.templatetags.jgo.config import can_be_godparent
from juntagrico_godparent.util.matches import all_possible_matches, get_matched, all_unmatchable
from juntagrico_godparent.util.utils import is_godparent, is_godchild, was_godchild


@login_required
@highlighted_menu('jgo')
def home(request):
    member = request.user.member
    if is_godparent(member):
        return godparent_signup(request)
    if was_godchild(member) and not can_be_godparent(request.user):
        return godchild_done(request)
    if is_godchild(member):
        return godchild_signup(request)
    return render(request, "jgo/home.html")


def _registration(request, template, form_class, exists_function, instance_attr):
    member = request.user.member
    exists = exists_function(member)
    initial = dict(
        areas=member.areas.values_list('id', flat=True),
        email=member.email,
        phone=member.mobile_phone or member.phone
    )
    if request.method == 'POST' or exists:
        form = form_class(request.POST or None, instance=getattr(request.user.member, instance_attr) if exists else None,
                          editing=exists, initial=initial)
        if request.method == 'POST' and form.is_valid():
            member = request.user.member
            form.instance.member = member
            form.save()
            # send signal
            if not exists:
                signals.created.send(form.instance.__class__, instance=form.instance)
            else:
                signals.changed.send(form.instance.__class__, instance=form.instance)
            # update member
            if member.mobile_phone:
                member.mobile_phone = form.cleaned_data['phone']
            else:
                member.phone = form.cleaned_data['phone']
            member.save()
            member.areas.set(form.cleaned_data['areas'])
            return redirect('jgo:home')
    else:
        form = form_class(initial=initial)
    return render(request, f"jgo/{template}.html", dict(form=form, exists=exists))


@login_required
@highlighted_menu('jgo')
def godparent_signup(request):
    return _registration(request, 'godparent', GodparentForm, is_godparent, 'godparent')


@login_required
@highlighted_menu('jgo')
def godchild_signup(request):
    return _registration(request, 'godchild', GodchildForm, is_godchild, 'godchild')


@login_required
@highlighted_menu('jgo')
def godchild_done(request):
    return render(request, "jgo/godchild_done.html")


@login_required
def increment_max_godchildren(request):
    if is_godparent(request.user.member):
        gp = request.user.member.godparent
        gp.max_godchildren += 1
        gp.save()
        signals.reactivated.send(gp.__class__, instance=gp)
    return redirect('jgo:home')


@login_required
def leave(request):
    if is_godparent(request.user.member):
        request.user.member.godparent.delete()
    elif is_godchild(request.user.member):
        request.user.member.godchild.delete()
    return redirect('jgo:home')


@login_required
def arranged(request, godchild_id):
    godchild = get_object_or_404(Godchild, id=godchild_id)
    if godchild.progress == godchild.OPEN:
        member = request.user.member
        if member in [godchild.member, godchild.godparent.member]:
            godchild.progress = godchild.ARRANGED
            godchild.save()
            # TODO: Send email
    return redirect('jgo:home')


@login_required
def done(request, godchild_id):
    godchild = get_object_or_404(Godchild, id=godchild_id)
    if godchild.progress == godchild.ARRANGED:
        member = request.user.member
        if member in [godchild.member, godchild.godparent.member]:
            godchild.progress = godchild.DONE
            godchild.save()
            godchild.godparent.max_godchildren -= 1
            godchild.godparent.save()
            # TODO: Send email
    return redirect('jgo:home')


class GodparentListView(PermissionRequiredMixin, ListView):
    permission_required = ['juntagrico_godparent.can_make_matches']
    extra_context = {'mail_url': reverse_lazy('jgo:contact')}


class MatchView(GodparentListView):
    template_name = 'jgo/manage/match_maker.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_godparents'] = Godparent.objects.available()
        context['remaining_godchildren'] = Godchild.objects.matched(False).count()
        return context

    def get_queryset(self):
        return all_possible_matches

    def post(self, request, *args, **kwargs):
        success = False
        for name, value in request.POST.items():
            if name.startswith('match-') and value == 'on':
                godparent, godchild = name.split('-')[1:]
                godchild = get_object_or_404(Godchild, id=godchild)
                godchild.godparent_id = godparent
                godchild.save()
                signals.matched.send(godchild.__class__, godchild=godchild, matcher=request.user.member)
                success = True
        if success:
            messages.success(request, 'Neumitglied und Gotte/Götti wurden vermittelt.')
        else:
            messages.error(request, 'Wähle mindestens eine passende Kombination aus')
        return redirect('jgo:manage-match')


class UnmatchableView(GodparentListView):
    template_name = 'jgo/manage/unmatchable.html'

    def get_queryset(self):
        return all_unmatchable

    def post(self, request, *args, **kwargs):
        if request.POST.get('godparent') and request.POST.get('godchild'):
            godchild = get_object_or_404(Godchild, id=request.POST.get('godchild'))
            godchild.godparent_id = request.POST.get('godparent')
            godchild.save()
            signals.matched.send(godchild.__class__, godchild=godchild, matcher=request.user.member)
            messages.success(request, 'Neumitglied und Gotte/Götti wurden vermittelt.')
        else:
            messages.error(request, 'Wähle ein Gotte/Götti und ein Neumitglied aus.')
        return redirect('jgo:manage-unmatchable')


class MatchedView(GodparentListView):
    template_name = 'jgo/manage/matched.html'

    def get_queryset(self):
        return get_matched


@permission_required('juntagrico_godparent.can_make_matches')
def unmatch(request, godchild_id):
    godchild = get_object_or_404(Godchild, id=godchild_id)
    godchild.godparent = None
    godchild.save()
    messages.success(request, 'Neumitglied und Gotte/Götti wurden wieder getrennt.')
    return redirect('jgo:manage-matched')


class CompletedView(GodparentListView):
    template_name = 'jgo/manage/completed.html'
    queryset = Godchild.objects.completed


@permission_required('juntagrico_godparent.can_make_matches')
def contact_member(request, member_id):
    member = get_object_or_404(Member, id=member_id)
    if not is_godparent(member) and not hasattr(member, 'godchild'):
        raise PermissionDenied
    return email_view(request, ContactForm, {
        'to_members': [member_id]
    })


@permission_required('juntagrico_godparent.can_make_matches')
def contact_members(request):
    member_ids = request.GET.get('members', '').split('-')
    members = Member.objects.filter(Q(godparent__isnull=False) | Q(godchild__isnull=False), id__in=member_ids)
    if not members:
        raise PermissionDenied
    return email_view(request, ContactForm, {
        'to_members': members.values_list('id', flat=True),
    })
