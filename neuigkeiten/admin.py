from django.contrib import admin

from neuigkeiten.models import *

@admin.register(Beitrag)
class BeitragAdmin(admin.ModelAdmin):
    # admin list table view
    list_display = ['title', 'published_date', 'author']
    list_display_links = ['title']
    ordering = ('-published_date',)
    
    fieldsets = (
      ('', {
          'fields': ('title','author','content_text','published_date',)
      }),
    )


