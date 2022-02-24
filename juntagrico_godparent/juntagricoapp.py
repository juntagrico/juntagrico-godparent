from juntagrico.util import addons
import juntagrico_godparent


addons.config.register_user_menu('jgo/menu/member.html')
addons.config.register_admin_menu('jgo/menu/admin.html')
addons.config.register_version(juntagrico_godparent.name, juntagrico_godparent.version)
