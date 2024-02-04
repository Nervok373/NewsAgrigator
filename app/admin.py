from django.contrib import admin

# Register your models here.
from .models import News

# Register your models here.
# admin.site.register(News)


class NewsAdmin(admin.ModelAdmin):
    # list_display = ['id', 'price', 'parse_datetime', 'description']
    # list_display_links = ['id', 'parse_datetime']
    search_fields = ['id', 'title', 'time', 'description']
    # list_editable = ['price']
    # list_filter = ['time', 'title']


admin.site.register(News, NewsAdmin)
