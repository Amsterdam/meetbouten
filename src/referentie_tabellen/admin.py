from django.contrib import admin

from .models import *


class ReferentieTabelAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(WijzenInwinning)
class StatusAdmin(ReferentieTabelAdmin):
    list_display = ("omschrijving",)


@admin.register(Type)
class StatusAdmin(ReferentieTabelAdmin):
    list_display = ("omschrijving", "soort")


@admin.register(Status)
class StatusAdmin(ReferentieTabelAdmin):
    list_display = ("omschrijving",)


@admin.register(Metingtype)
class StatusAdmin(ReferentieTabelAdmin):
    list_display = ("omschrijving",)


@admin.register(Merk)
class MerkAdmin(ReferentieTabelAdmin):
    list_display = ("omschrijving", "omschrijving_verkort")


@admin.register(Bron)
class BronAdmin(ReferentieTabelAdmin):
    list_display = ("omschrijving", "doel")
