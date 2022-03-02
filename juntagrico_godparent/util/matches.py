from django.db.models import Count, F

from juntagrico_godparent.models import Godchild, Godparent


def member_depot(member):
    if member.subscription_future:
        return member.subscription_future.future_depot or member.subscription_future.depot
    elif member.subscription_current:
        return member.subscription_current.future_depot or member.subscription_current.depot
    return None


def match(godparent, godchild):
    # TODO: add more conditions?
    return set(godparent.languages) & set(godchild.languages) and set(godparent.slots) & set(godchild.slots)


def available_godparents():
    return Godparent.objects.annotate(number_of_godchildren=Count('godchild')).filter(
        number_of_godchildren__lt=F('max_godchildren'))


def get_matches_dict(godparent, godchild):
    godparent.depot = member_depot(godparent.member)
    godchild.depot = member_depot(godchild.member)
    return dict(
        godparent=godparent,
        godchild=godchild,
        same_depot=godparent.depot == godchild.depot,
        matching_areas=(godparent.member.areas.all() & godchild.member.areas.all()).count()
    )


def all_possible_matches():
    for godchild in Godchild.objects.filter(godparent__isnull=True):
        matches = []
        for godparent in available_godparents():
            if match(godparent, godchild):
                matches.append(get_matches_dict(godparent, godchild))
        godchild.num_options = len(matches)
        yield from matches


def all_unmatchable():
    unmatched_godparents = available_godparents()
    unmatched_godchildren = Godchild.objects.filter(godparent__isnull=True)
    matchable_godchildren = []
    for godchild in unmatched_godchildren:
        for godparent in unmatched_godparents:
            if match(godparent, godchild):
                matchable_godchildren.append(godchild)
                break
    return dict(
        godparents=unmatched_godparents,
        godchildren=set(unmatched_godchildren) - set(matchable_godchildren),
    )


def get_matched():
    for godchild in Godchild.objects.filter(godparent__isnull=False):
        yield get_matches_dict(godchild.godparent, godchild)
