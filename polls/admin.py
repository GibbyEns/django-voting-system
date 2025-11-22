from django.contrib import admin
from .models import Poll, Choice

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3  # show 3 empty choice fields by default

class PollAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')
    inlines = [ChoiceInline]

admin.site.register(Poll, PollAdmin)

