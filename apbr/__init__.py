from extras.plugins import PluginConfig
from .version import __version__

class ApbrConfig(PluginConfig):
    name = 'apbr'
    verbose_name = 'Advanced Policy-Based Routing'
    description = 'A NetBox plugin for managing Juniper\'s APBR policies'
    version = __version__
    author = 'Calvin Remsburg'
    author_email = 'cremsburg@juniper.net'
    base_url = 'apbr'
    required_settings = []
    min_version = '3.0.0'
    max_version = '3.0.19'
    default_settings = {
        'device_ext_page': 'right',
        'asdot': False
    }

config = ApbrConfig
