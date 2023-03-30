from django.contrib import admin

from .models import *


@admin.register(WijzenInwinning)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("omschrijving",)

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Type)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("omschrijving", "soort")

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("omschrijving",)

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Metingtype)
class StatusAdmin(admin.ModelAdmin):
    list_display = ("omschrijving",)

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Merk)
class MerkAdmin(admin.ModelAdmin):
    list_display = ("omschrijving", "omschrijving_verkort")

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(Bron)
class BronAdmin(admin.ModelAdmin):
    list_display = ("omschrijving", "doel")

    def has_change_permission(self, request, obj=None):
        return False
