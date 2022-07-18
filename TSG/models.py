from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone
from django.shortcuts import reverse
from ckeditor.fields import RichTextField

INN_MULTIPLIER_LIST = [2, 4, 10, 3, 5, 9, 4, 6, 8]
INN_LEN = 10


# Create your models here.
def validate_inn(value):
    if len(value) == INN_LEN and value.isdigit():
        control_sum = 0
        for i in range(INN_LEN - 1):
            control_sum += int(value[i]) * INN_MULTIPLIER_LIST[i]
        if control_sum % 11 % 10 == int(value[INN_LEN - 1]):
            return
    raise ValidationError(
        '%(value)s - невалидный ИНН',
        params={'value': value},
    )


def validate_int_greater_zero(value):
    if value < 1:
        raise ValidationError(
            '%(value)s - должно быть больше нуля',
            params={'value': value},
        )
    return


def validate_between_one_zero(value):
    if value < 0 or value > 1:
        raise ValidationError(
            '%(value)s - должно быть в пределах от 0 до 1',
            params={'value': value},
        )
    return


class User(AbstractUser):
    pass
    # todo M2M notification
    # todo positionID


class Tsg(models.Model):
    name = models.CharField(max_length=20, )
    legal_address = models.CharField(max_length=100, )
    inn = models.CharField(max_length=INN_LEN, validators=[validate_inn, ], )
    chairman = models.ForeignKey(settings.AUTH_USER_MODEL, models.PROTECT, related_name="chairTsg")
    bookkeeper = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.SET_NULL,
        null=True,
        blank=True,
        related_name="bookkeeperTsg",
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tsg', args=[str(self.id)])

    def get_announcement_creation_link(self):
        return reverse('create_announcement', args=[str(self.id)])

    def get_notification_creation_link(self):
        return reverse('create_notification', args=[str(self.id)])


class City(models.Model):
    name = models.CharField(max_length=15, )
    region = models.CharField(max_length=30, )

    class Meta:
        unique_together = ('name', 'region')

    def __str__(self):
        return self.name


class House(models.Model):
    TSG = models.ForeignKey(Tsg, models.CASCADE)
    address = models.CharField(max_length=100, )
    name = models.CharField(max_length=20, )
    city = models.ForeignKey(City, models.PROTECT)
    floor_count = models.IntegerField()

    def __str__(self):
        return self.TSG.name + ", " + self.address


class Entrance(models.Model):
    name = models.CharField(max_length=10)
    house = models.ForeignKey(House, models.CASCADE)


class Flat(models.Model):
    number = models.CharField(max_length=10)
    square = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    entrance = models.ForeignKey(Entrance, models.CASCADE)
    floor = models.IntegerField(validators=[validate_int_greater_zero, ])
    main_user = models.ForeignKey(settings.AUTH_USER_MODEL, models.SET_NULL, null=True, related_name='main_user_flats')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='UseRights', )

    def __str__(self):
        return self.entrance.house.__str__() + ", " + self.number


class ResourceType(models.Model):
    name = models.CharField(max_length=25)
    TSG = models.ForeignKey(Tsg, models.CASCADE)


class Meter(models.Model):
    flat = models.ForeignKey(Flat, models.CASCADE)
    serial_number = models.CharField(max_length=25)
    next_check_date = models.DateField(null=True)
    workability = models.BooleanField()
    resource_type = models.ForeignKey(ResourceType, models.PROTECT)


class MeterData(models.Model):
    meter = models.ForeignKey(Meter, models.CASCADE)
    send_date = models.DateField(default=timezone.now)
    value = models.DecimalField(max_digits=15, decimal_places=3, )


class UseRights(models.Model):
    flat = models.ForeignKey(Flat, models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE)
    own_part = models.DecimalField(max_digits=3, decimal_places=2, validators=[validate_between_one_zero], default=0)
    priority = models.IntegerField(default=1)


class NotificationSection(models.Model):
    tsg = models.ForeignKey(Tsg, models.CASCADE)
    name = models.CharField(max_length=20, )

    class Meta:
        unique_together = ('tsg', 'name')

    def __str__(self):
        return self.name


class Notification(models.Model):
    tsg = models.ForeignKey(Tsg, models.CASCADE)
    section = models.ForeignKey(NotificationSection, models.PROTECT)
    theme = models.CharField(max_length=20, null=True, blank=True, )
    preview_text = models.CharField(max_length=50, null=True, blank=True, )
    text = models.TextField()
    creation_date = models.DateField(default=timezone.now)
    recipients = models.ManyToManyField(Flat)
    users_viewed = models.ManyToManyField(User)

    @staticmethod
    def get_deletion_confirmation():
        return 'Вы уверены, что хотите удалить это уведомление?'

    @staticmethod
    def get_list_header():
        return 'История уведомлений'

    @staticmethod
    def get_creation_text():
        return 'Создать уведомление'

    @staticmethod
    def get_deletion_text():
        return 'Удалить уведомление'

    def get_tsg_detail_url(self):
        return reverse('notification_tsg_detail', kwargs={'tsg_pk': self.tsg.id, 'notification_pk': self.id}, )

    def get_flat_detail_url(self, flat_pk):
        return reverse('notification_flat_detail', kwargs={'flat_pk': flat_pk, 'notification_pk': self.id}, )

    def get_deletion_url(self):
        return reverse('notification_delete', kwargs={'tsg_pk': self.tsg.id, 'notification_pk': self.id}, )


class Announcement(models.Model):
    tsg = models.ForeignKey(Tsg, models.CASCADE)
    theme = models.CharField(max_length=50)
    text = RichTextField()
    creation_date = models.DateField(default=timezone.now)
    users_viewed = models.ManyToManyField(User)

    @staticmethod
    def get_deletion_confirmation():
        return 'Вы уверены, что хотите удалить это объявление?'

    @staticmethod
    def get_list_header():
        return 'История объявлений'

    @staticmethod
    def get_creation_text():
        return 'Создать объявление'

    @staticmethod
    def get_deletion_text():
        return 'Удалить объявление'

    def get_absolute_url(self):
        return reverse('announcement_detail', kwargs={'tsg_pk': self.tsg.id, 'announcement_pk': self.id}, )

    def get_deletion_url(self):
        return reverse('announcement_delete', kwargs={'tsg_pk': self.tsg.id, 'announcement_pk': self.id}, )
