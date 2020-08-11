from django.contrib import admin
from . import models

# Register your models here.
class GroupMemberInline(admin.TabularInline):
    model = models.GroupMembership
    extra = 1

class GroupAdmin(admin.ModelAdmin):
    fields = ['description','name','slug']
    search_fields = ['name','description']
    list_filter = ['members']
    list_display = ['name','slug','description']
    list_display_links = None
    list_editable = ['description']

    inlines = [
        GroupMemberInline,
    ]

admin.site.register(models.Group,GroupAdmin)

