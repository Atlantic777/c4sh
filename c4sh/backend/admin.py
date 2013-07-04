from c4sh.backend.models import *
from django.contrib import admin

class CustomHonoraryMemberAdmin(admin.ModelAdmin):
    list_display = ('membership_number', 'full_name')
    search_fields = ['membership_number', 'full_name']

admin.site.register(UserProfile)
admin.site.register(Ticket)
admin.site.register(Cashdesk)
admin.site.register(CashdeskSession)
admin.site.register(HonoraryMember, CustomHonoraryMemberAdmin)
admin.site.register(Pass)
admin.site.register(CashdeskSessionPass)
