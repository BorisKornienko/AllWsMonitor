from django.contrib import admin
from .models import System_warning, System_critical
from .models import System_error, App_warning
from .models import App_critical, App_error
from .models import Proceed_date

admin.site.register(System_warning)
admin.site.register(System_critical)
admin.site.register(System_error)
admin.site.register(App_critical)
admin.site.register(App_error)
admin.site.register(App_warning)
admin.site.register(Proceed_date)