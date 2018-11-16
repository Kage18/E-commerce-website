from django.contrib import admin
from .models import Post,Comment
# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','slugthing','author','status',)
    list_filter = ('status','created','updated',)
    search_fields = ('author__username','title',)
    prepopulated_fields = {'slugthing':('title',)}
    list_editable = ('status',)
    date_hierarchy = ('created')


admin.site.register(Post,PostAdmin)
admin.site.register(Comment)
