from django.contrib import admin
from website.models import Customer,Admin
from auth.extras import delete_patient_data
# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    # name of our db
    using = 'default'
    list_display = ('id','owner','username',)
    list_display_link = ('id','owner','username',)
    list_filter = ('owner','username',)
    search_fields = ('username',)
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        # where to save
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        email = obj.owner
        print(email)
        obj.delete(using=self.using)
        delete_patient_data(email)

        
    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, using=self.using **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, using=self.using,**kwargs)

admin.site.register(Customer,AccountAdmin)
admin.site.register(Admin)