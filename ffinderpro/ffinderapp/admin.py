from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Listing, CustomUser, PlayerProfile, TeamProfile, PlayerListing

# Register your models here
admin.site.register(Listing)
admin.site.register(PlayerListing)
admin.site.register(PlayerProfile)
admin.site.register(TeamProfile)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'is_player', 'is_team', 'photo')
    list_filter = ('is_player', 'is_team')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                   'groups', 'user_permissions')}),
        ('Personal info', {'fields': ('photo',)}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'is_player', 'is_team', 'photo'),
        }),
    )
    search_fields = ('username',)
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)