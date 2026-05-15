from django.contrib import admin

from .models import Legend, LegendLevel


class LegendLevelInline(admin.TabularInline):
    model = LegendLevel
    extra = 1


@admin.register(Legend)
class LegendAdmin(admin.ModelAdmin):
    inlines = [LegendLevelInline]

