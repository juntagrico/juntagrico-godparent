from django.db.models import QuerySet, Count, F, Sum, Q


class GodparentQuerySet(QuerySet):
    def annotate_number_of_godchildren(self):
        from juntagrico_godparent.models import Godchild
        return self.annotate(
            number_of_godchildren=Count('godchild', filter=~Q(godchild__progress=Godchild.DONE))
        )

    def available(self):
        return self.annotate_number_of_godchildren().filter(
            number_of_godchildren__lt=F('max_godchildren')
        )

    def remaining_capacity(self):
        qs = self.annotate_number_of_godchildren()
        return (qs.aggregate(m=Sum('max_godchildren'))['m'] or 0) - \
               (self.aggregate(u=Sum('number_of_godchildren'))['u'] or 0)


class GodchildQuerySet(QuerySet):
    def matched(self, invert=True):
        return self.filter(godparent__isnull=not invert).exclude(progress=self.model.DONE)

    def completed(self):
        return self.filter(progress=self.model.DONE, godparent__isnull=False)
