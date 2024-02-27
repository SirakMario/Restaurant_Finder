from django.contrib import admin
from .models import Restaurant, Comment

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name','rating','opening_time','closing_time','is_published')
    list_display_links = ('name','rating','opening_time','closing_time')
    list_filter = ('rating',)
    list_editable = ('is_published',)
    search_fields = ('name','address','rating','opening_time','closing_time','type_of_food')
    list_per_page = 25
class CommentAdmin(admin.ModelAdmin):
    list_display= ('restaurant','commenter_name','date_added')
    list_display_links = ('restaurant','commenter_name','date_added')

# Register your models here.
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Comment, CommentAdmin)