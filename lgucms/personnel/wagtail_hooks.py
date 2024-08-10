from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)

from lgucms.personnel.models import Personnel


class PersonnelModelAdmin(ModelAdmin):
    model = Personnel
    menu_icon = 'group'  # change as required
    list_display = ('first_name', 'middle_name', 'last_name', 'designation', 'thumb_image')
    list_filter = ('designation', )
    search_fields = ('first_name', 'last_name', 'designation')
    inspect_view_enabled = True


# See base for reference comments.
modeladmin_register(PersonnelModelAdmin)
