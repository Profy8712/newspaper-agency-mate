from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Newspaper, Topic, Redactor

@admin.register(Redactor)
class RedactorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("years_of_experience",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": (
            "first_name",
            "last_name",
            "email",
            "years_of_experience",
        )}),
    )

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "published_date")
    list_filter = ("topic", "published_date")
    search_fields = ("title", "content")
    filter_horizontal = ("publishers",)
