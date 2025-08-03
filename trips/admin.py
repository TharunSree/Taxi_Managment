from django.contrib import admin

from trips.models import Package, Trip

class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'vehicle_type', 'vehicle_model', 'charges', 'extra_charge_per_km')
    list_filter = ('vehicle_type',)

admin.site.register(Package, PackageAdmin)
admin.site.register(Trip)
