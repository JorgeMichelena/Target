from django.contrib.gis import admin
from targets.models import Topic, Target
from users.models import User

class TopicAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Name', {'fields': ['name']}),
    ]
    list_display = ['name']
    list_filter = ['name']
class TargetAdmin(admin.ModelAdmin):
    list_display = ['title', 'location', 'radius', 'topic', 'user']
    list_filter = ['topic']

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email','first_name', 'last_name', 
                    'gender', 'is_staff', 'is_superuser', 'date_joined']

admin.site.register(User, UserAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Target, TargetAdmin)
