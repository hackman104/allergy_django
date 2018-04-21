from django.contrib import admin
from .models import Link, Request
from . import forms
import inspect

# Customize and register models
class LinkAdmin(admin.ModelAdmin):
    list_display = ("restaurant_name", "rest_link")
    fieldsets = [
        ('Information',     {'fields': ['restaurant_name', 'rest_link']}),
        ('Date',            {'fields': ['add_date']}),
    ]

admin.site.register(Link, LinkAdmin)

class RequestAdmin(admin.ModelAdmin):
    list_display = ("request_name", "request_date")
    fieldsets = [
        ('Information',     {'fields': ['request_name', 'request_link']}),
        ('Date',            {'fields': ['request_date']}),
    ]

admin.site.register(Request,RequestAdmin)
