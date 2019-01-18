from django.db import models
from django.db import connection, transaction

MAX_LENGTH_STRING = 255


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


class Unit(ModelBase):
    description = models.CharField(max_length=MAX_LENGTH_STRING)
    is_mobile = models.BooleanField()
    uuid = models.CharField(max_length=MAX_LENGTH_STRING)
    unit_group = models.ForeignKey('webapp.UnitGroup', on_delete=models.CASCADE, related_name='unit_unit_group')
    unit_type = models.ForeignKey('webapp.EnumItem', on_delete=models.CASCADE, related_name='unit_event')

    def __str__(self):
        return '%s - %s' % (self.uuid, self.description)

    class Meta:
        db_table = 'unit'


class Sensor(ModelBase):
    description = models.CharField(max_length=MAX_LENGTH_STRING)
    uuid = models.CharField(max_length=MAX_LENGTH_STRING)
    unit = models.ForeignKey('webapp.Unit', on_delete=models.CASCADE, related_name='sensor_unit')
    sensor_type = models.ForeignKey('webapp.SensorType', on_delete=models.CASCADE, related_name='sensor_sensor_type')

    def __str__(self):
        return '%s - %s' % (self.uuid, self.description)

    class Meta:
        db_table = 'sensor'


class SensorType(ModelBase):
    description = models.CharField(max_length=MAX_LENGTH_STRING)
    phenomenon = models.ForeignKey('webapp.Phenomenon', on_delete=models.CASCADE, related_name='sensor_type_phenomenon')

    class Meta:
        db_table = 'sensor_type'


class EnumItem(ModelBase):
    code = models.CharField(max_length=MAX_LENGTH_STRING)
    description = models.CharField(max_length=MAX_LENGTH_STRING)

    def __str__(self):
        return '%s - %s' % (self.code, self.description)

    class Meta:
        db_table = 'enum_item'


class Event(ModelBase):
    timestamp = models.DateTimeField('Timestamp')
    enumItem = models.ForeignKey('webapp.EnumItem', on_delete=models.CASCADE, related_name='event_enum_item')
    enumStatusEntity = models.ForeignKey('webapp.EventStatus', on_delete=models.CASCADE)
    unit = models.ForeignKey('webapp.Unit', on_delete=models.CASCADE)

    class Meta:
        db_table = 'event'


class EventStatus(ModelBase):
    code = models.CharField(max_length=MAX_LENGTH_STRING)
    description = models.CharField(max_length=MAX_LENGTH_STRING)

    class Meta:
        db_table = 'event_status'


class Observation(ModelBase):
    timestamp = models.DateTimeField('Timestamp')
    value = models.FloatField()
    sensor = models.ForeignKey('webapp.Sensor', on_delete=models.CASCADE, related_name='observation_sensor')

    class Meta:
        db_table = 'observation'


class Phenomenon(ModelBase):
    description = models.CharField(max_length=MAX_LENGTH_STRING)
    physical_unit = models.CharField(max_length=MAX_LENGTH_STRING)

    class Meta:
        db_table = 'phenomenon'


class Position(ModelBase):
    # TODO: see https://docs.djangoproject.com/en/2.1/ref/contrib/gis/model-api/
    # geometry = models.PointField()
    timestamp = models.DateTimeField('Timestamp')
    unit = models.ForeignKey('webapp.Unit', on_delete=models.CASCADE, related_name='position_unit')

    class Meta:
        db_table = 'position'


class Privilege(ModelBase):
    enum_item = models.ForeignKey('webapp.EnumItem', on_delete=models.CASCADE, related_name='privilege_enum_item')
    privilege_group = models.ForeignKey('webapp.PrivilegeGroup', on_delete=models.CASCADE,
                                        related_name='privilege_privilege_group')

    class Meta:
        db_table = 'privilege'


class PrivilegeGroup(ModelBase):
    description = models.CharField(max_length=MAX_LENGTH_STRING)
    group = models.ForeignKey('webapp.UnitGroup', on_delete=models.CASCADE, related_name='privilege_group_group')

    class Meta:
        db_table = 'privilege_group'


class SystemConfig(ModelBase):
    key = models.CharField(max_length=MAX_LENGTH_STRING)
    value = models.CharField(max_length=MAX_LENGTH_STRING)

    class Meta:
        db_table = 'system_config'


class UnitGroup(ModelBase):
    description = models.CharField(max_length=MAX_LENGTH_STRING)

    def __str__(self):
        return self.description

    class Meta:
        db_table = 'unit_group'


class User(ModelBase):
    email = models.CharField(max_length=MAX_LENGTH_STRING)
    name = models.CharField(max_length=MAX_LENGTH_STRING)
    password = models.CharField(max_length=MAX_LENGTH_STRING)

    class Meta:
        db_table = 'user'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)



class User2UnitGroup(ModelBase):
    privilege_group = models.ForeignKey('webapp.PrivilegeGroup', on_delete=models.CASCADE,
                                        related_name='user2unitgroup_privilege_group')
    unit_group = models.ForeignKey('webapp.UnitGroup', on_delete=models.CASCADE,
                                   related_name='user2unitgroup_unit_group')
    user = models.ForeignKey('webapp.User', on_delete=models.CASCADE, related_name='user2unitgroup_user')

    class Meta:
        db_table = 'user2unit_group'
