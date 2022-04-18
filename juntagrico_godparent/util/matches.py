from juntagrico_godparent.models import Godchild, Godparent


def match(godparent, godchild):
    # TODO: add more conditions?
    return set(godparent.languages) & set(godchild.languages) and set(godparent.slots) & set(godchild.slots)


def get_matches_dict(godparent, godchild):
    return dict(
        godparent=godparent,
        godchild=godchild,
        same_depot=godparent.depot == godchild.depot,
        matching_areas=(godparent.member.areas.all() & godchild.member.areas.all()).count()
    )


def all_possible_matches():
    for godchild in Godchild.objects.matched(False):
        matches = []
        for godparent in Godparent.objects.available():
            if match(godparent, godchild):
                matches.append(get_matches_dict(godparent, godchild))
        godchild.num_options = len(matches)
        yield from matches


def all_unmatchable():
    unmatched_godparents = Godparent.objects.available()
    unmatched_godchildren = Godchild.objects.matched(False)
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
    for godchild in Godchild.objects.matched():
        yield get_matches_dict(godchild.godparent, godchild)
