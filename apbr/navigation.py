from extras.plugins import PluginMenuButton, PluginMenuItem
from utilities.choices import ButtonColorChoices

menu_items = (
    PluginMenuItem(
        link='plugins:apbr:random_profile',
        link_text='Random APBR profile',
        buttons=(
            PluginMenuButton('home', 'Button A', 'fa fa-info', ButtonColorChoices.BLUE),
            PluginMenuButton('home', 'Button B', 'fa fa-warning', ButtonColorChoices.GREEN),
        )
    ),
)
