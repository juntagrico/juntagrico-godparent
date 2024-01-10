from django.contrib import admin

from juntagrico_godparent.models import Godparent, Godchild


@admin.register(Godparent)
class GodparentAdmin(admin.ModelAdmin):
    search_fields = ('member__first_name', 'member__last_name')
    readonly_fields = ('creation_date', 'member',)
    raw_id_fields = ('member',)
    list_display = ('member', 'creation_date', 'languages', 'slots', 'children', 'max_godchildren')
    list_filter = ('creation_date', 'children')

    def get_readonly_fields(self, request, obj=None):
        if obj is not None:
            return super().get_readonly_fields(request, obj)
        return set()


@admin.register(Godchild)
class GodchildAdmin(GodparentAdmin):
    list_display = ('member', 'creation_date', 'languages', 'slots', 'children', 'godparent')
