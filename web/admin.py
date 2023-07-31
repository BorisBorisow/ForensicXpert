from django.contrib import admin
from django.contrib.auth import get_user_model

from web.models import Exhibit, ExhibitComponent, ExhibitDataImage, Client, ContactPerson, Mandate, \
    ClientCategory

# Register your models_pro here.
UserModel = get_user_model()


@admin.register(UserModel)
class UserModelAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_staff')


@admin.register(Exhibit)
class ExhibitAdmin(admin.ModelAdmin):
    pass


@admin.register(ExhibitComponent)
class ExhibitComponentAdmin(admin.ModelAdmin):
    list_display = ('denotation', 'exhibit')


@admin.register(ExhibitDataImage)
class ExhibitDataImageAdmin(admin.ModelAdmin):
    pass


@admin.register(ClientCategory)
class ClientCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'institution_client', 'division', 'user', 'role')


@admin.register(Mandate)
class MandateAdmin(admin.ModelAdmin):
    list_display = ('mandate_number', 'priority', 'denotation', 'description', 'client')
    search_fields = ["denotation", "description"]
    search_filter = ["priority", "investigation_group", "investigation_group_contact"]
    list_per_page = 10