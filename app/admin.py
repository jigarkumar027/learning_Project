from django.contrib import admin
from .models import * 
# Register your models here.

class useradmin(admin.ModelAdmin):
    list_display = ('Username','Email','Role','is_varified','is_active')
    list_editable = ('is_active',)
    list_per_page = 4
    search_fields = ('Username',)
    list_filter = ('is_active',)

admin.site.register(User,useradmin)
admin.site.register(Student)
admin.site.register(Tutor)
admin.site.register(Category)
admin.site.register(Course)
admin.site.register(Cart)

