from django.db import models
from django.db import connection, transaction


def get_next(sequence):
    cursor = connection.cursor()
    cursor.execute("select nextval('" + sequence + "')")
    return cursor.fetchone()


class ModelBase(models.Model):
    """
    Abstract class for all model classes
    """

    id = models.BigIntegerField(primary_key=True)

    class Meta:
        abstract = True
        managed = False


class Sensor(ModelBase):
    description = models.CharField(max_length=200)
    uuid = models.CharField(max_length=200)
    unit = models.ForeignKey('webapp.Unit', on_delete=models.CASCADE, related_name='sensor_unit')

    def __str__(self):
        return self.uuid

    class Meta:
        db_table = 'sensor'


class EnumItem(ModelBase):
    code = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    class Meta:
        db_table = 'enum_item'


class Unit(ModelBase):
    description = models.CharField(max_length=200)
    events = models.ForeignKey('webapp.Event', on_delete=models.CASCADE)
    positions = models.ForeignKey('webapp.Position', on_delete=models.CASCADE)
    sensor = models.ForeignKey('webapp.Sensor', on_delete=models.CASCADE, related_name='unit_sensor')

    class Meta:
        db_table = 'unit'


class Event(ModelBase):
    timestamp = models.DateTimeField('Timestamp')
    enumItem = models.ForeignKey('webapp.EnumItem', on_delete=models.CASCADE)
    enumStatusEntity = models.ForeignKey('webapp.EventStatus', on_delete=models.CASCADE)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    class Meta:
        db_table = 'event'


class EventStatus(ModelBase):
    code = models.CharField(max_length=200)
    description = models.CharField(max_length=200)

    events = models.ForeignKey('webapp.Event', on_delete=models.CASCADE)

    class Meta:
        db_table = 'event_status'


class Observation(ModelBase):
    timestamp = models.DateTimeField('Timestamp')
    value = models.FloatField()

    class Meta:
        db_table = 'observation'


class Phenomenon(ModelBase):
    pass


class Position(ModelBase):
    pass


class Privilege(ModelBase):
    pass


class PrivilegeGroup(ModelBase):
    pass


class SensorType(ModelBase):
    pass


class SystemConfig(ModelBase):
    pass


class UnitGroup(ModelBase):
    pass


class User(ModelBase):
    pass


class User2UnitGroup(ModelBase):
    pass
