from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link='plugins:apbr:apbr_list',
        link_text='APBR Profiles',
        permissions=['apbr.view_apbr'],
        buttons=(
            PluginMenuButton(
                link='plugins:apbr:apbr_add',
                title='APBR Profiles',
                icon_class='mdi mdi-plus-thick',
                color=ButtonColorChoices.GREEN,
                permissions=['apbr.add_apbr'],
            ),
        ),
    ),
)