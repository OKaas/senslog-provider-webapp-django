from django.contrib import admin

from .models import Sensor
from .models import Unit
from .models import EnumItem
from .models import Event
from .models import EventStatus
from .models import Observation

# Register your models here.
admin.site.register(Sensor)
admin.site.register(Unit)
admin.site.register(EnumItem)
admin.site.register(Event)
admin.site.register(EventStatus)
admin.site.register(Observation)