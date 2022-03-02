from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from juntagrico.util.views_admin import subscription_management_list

from juntagrico_godparent.forms import GodparentForm, GodchildForm
from juntagrico_godparent.mailer.membernotification import notify_matched_members

from juntagrico_godparent.models import Godchild
from juntagrico_godparent.util.matches import all_possible_matches, get_matched, all_unmatchable
from juntagrico_godparent.util.utils import is_godparent, is_godchild


@login_required
def home(request):
    if is_godparent(request.user.member):
        return godparent(request)
    if is_godchild(request.user.member):
        return godchild(request)
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
def godparent(request):
    return _registration(request, 'godparent', GodparentForm, is_godparent, 'godparent')


@login_required
def godchild(request):
    return _registration(request, 'godchild', GodchildForm, is_godchild, 'godchild')


@login_required
def increment_max_godchildren(request):
    if is_godparent(request.user.member):
        request.user.member.godparent.max_godchildren += 1
        request.user.member.godparent.save()
    return redirect('jgo:home')


@login_required
def leave(request):
    if is_godparent(request.user.member):
        request.user.member.godparent.delete()
    elif is_godchild(request.user.member):
        request.user.member.godchild.delete()
    return redirect('jgo:home')


@permission_required('juntagrico_godparent.can_make_matches')
def match(request):
    render_dict = {'change_date_disabled': True}
    if request.method == 'POST':
        for name, value in request.POST.items():
            if name.startswith('match-') and value == 'on':
                godparent, godchild = name.split('-')[1:]
                godchild = get_object_or_404(Godchild, id=godchild)
                godchild.godparent_id = godparent
                godchild.save()
                notify_matched_members(godchild, request.user.member)
                render_dict['form_result'] = 'success'
    return subscription_management_list(all_possible_matches(), render_dict,
                                        'jgo/match_maker.html', request)


@permission_required('juntagrico_godparent.can_make_matches')
def unmatchable(request):
    render_dict = {'change_date_disabled': True}
    if request.method == 'POST' and request.POST.get('godparent') and request.POST.get('godchild'):
        godchild = get_object_or_404(Godchild, id=request.POST.get('godchild'))
        godchild.godparent_id = request.POST.get('godparent')
        godchild.save()
        render_dict['form_result'] = 'success'
    return subscription_management_list(all_unmatchable(), render_dict,
                                        'jgo/unmatchable.html', request)


@permission_required('juntagrico_godparent.can_make_matches')
def matched(request, removed=False):
    render_dict = {'change_date_disabled': True, 'removed': removed}
    return subscription_management_list(get_matched(), render_dict,
                                        'jgo/matched.html', request)


@permission_required('juntagrico_godparent.can_make_matches')
def unmatch(request, godchild_id):
    godchild = get_object_or_404(Godchild, id=godchild_id)
    godchild.godparent = None
    godchild.save()
    return redirect('jgo:matched-removed')
