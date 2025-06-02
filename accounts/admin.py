from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)  # cleaner way to register
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # 1️⃣ Fields that will show in the user LIST page
    list_display = ("username", "email", "phone_number", "is_staff", "is_active")

    # 2️⃣ Fields you can SEARCH by (top right search bar)
    search_fields = ("username", "email", "phone_number")

    # 3️⃣ Filters you can use on the right side
    list_filter = ("is_staff", "is_active", "date_joined")

    # 4️⃣ Add phone number field to user form
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("phone_number",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("phone_number",)}),)

    ordering = ("-date_joined",)
    readonly_fields = ("last_login",)
