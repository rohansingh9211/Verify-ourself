from django.contrib import admin
from AuthUser import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from AuthUser.models import *
# Register your models here.
class AuthUserAdminModel(BaseUserAdmin):
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id","email", "name", "is_admin", "tc"]
    list_filter = ["is_admin","email"]
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("name", "tc")}),
        ("Permissions", {"fields": ("is_admin",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "tc", "password1", "password2"),
            },
        ),
    )
    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []


# Now register the new UserAdmin...
admin.site.register(AuthUser, AuthUserAdminModel)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
# admin.site.unregister(Group)
