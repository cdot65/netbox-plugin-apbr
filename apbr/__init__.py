from extras.plugins import PluginConfig

class ApbrConfig(PluginConfig):
    name = 'apbr'
    verbose_name = 'Advanced Policy-Based Routing'
    description = 'A NetBox plugin for managing Juniper\'s APBR policies'
    version = '0.0.1'
    author = 'Calvin Remsburg'
    author_email = 'cremsburg@juniper.net'
    base_url = 'apbr'
    required_settings = []
    default_settings = {
        'loud': False
    }

config = ApbrConfig