from django.contrib import admin
from core.models import Account, Pair


class AccountAdmin(admin.ModelAdmin):
    pass


class PairAdmin(admin.ModelAdmin):
    pass


admin.site.register(Account, AccountAdmin)
admin.site.register(Pair, PairAdmin)
