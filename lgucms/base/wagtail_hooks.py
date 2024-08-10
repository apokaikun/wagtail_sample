from wagtail.contrib.modeladmin.options import (
    ModelAdmin, modeladmin_register)

from lgucms.base.models import FooterText , HeaderText


class FooterTextAdmin(ModelAdmin):
    menu_label = 'Footer Settings'
    menu_icon = 'cog'
    model = FooterText
    search_fields = ('body',)

class HeaderTextAdmin(ModelAdmin):
    menu_label = 'Header Settings'
    menu_icon = 'cog'
    model = HeaderText
    search_fields = ('body',)

# class SiteModelAdmin(ModelAdminGroup):
#     menu_label = 'Admin Misc'
#     menu_icon = 'fa-cutlery'  # change as required
#     menu_order = 300  # will put in 4th place (000 being 1st, 100 2nd)
#     items = (PeopleModelAdmin, FooterTextAdmin)


# When using a ModelAdminGroup class to group several ModelAdmin classes together,
# you only need to register the ModelAdminGroup class with Wagtail:
modeladmin_register(FooterTextAdmin)
