from django.db.models import QuerySet, Count, F, Sum


class GodparentQuerySet(QuerySet):
    def annotate_number_of_godchildren(self):
        return self.annotate(
            number_of_godchildren=Count('godchild')
        )

    def available(self):
        return self.annotate_number_of_godchildren().filter(
            number_of_godchildren__lt=F('max_godchildren')
        )

    def remaining_capacity(self):
        qs = self.annotate_number_of_godchildren()
        return qs.aggregate(m=Sum('max_godchildren'))['m'] - self.aggregate(u=Sum('number_of_godchildren'))['u']


class GodchildQuerySet(QuerySet):
    def matched(self, f=True):
        return self.filter(godparent__isnull=not f)
