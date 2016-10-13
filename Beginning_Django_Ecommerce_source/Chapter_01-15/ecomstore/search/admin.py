from django.contrib import admin
from ecomstore.search.models import SearchTerm

class SearchTermAdmin(admin.ModelAdmin):
    list_display = ('__unicode__','ip_address','search_date')
    list_filter = ('ip_address','user','q')
    exclude = ('user',)
admin.site.register(SearchTerm, SearchTermAdmin)