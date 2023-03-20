from django.contrib import admin
from website.models import Customer,Admin,Category,Cart,CartItem,Order,Product,ProductImage
from authentication.extras import delete_customer_data
# Register your models here.

class AccountAdmin(admin.ModelAdmin):
    # name of our db
    using = 'default'
    list_display = ('id','customer','username',)
    list_display_link = ('id','customer','username',)
    list_filter = ('customer','username',)
    search_fields = ('username',)
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        # where to save
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        email = obj.customer
        print(email)
        obj.delete(using=self.using)
        delete_customer_data(email)

        
    def get_queryset(self, request):
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return super().formfield_for_foreignkey(db_field, request, using=self.using **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return super().formfield_for_manytomany(db_field, request, using=self.using,**kwargs)

admin.site.register(Customer,AccountAdmin)
admin.site.register(Admin)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductImage)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)