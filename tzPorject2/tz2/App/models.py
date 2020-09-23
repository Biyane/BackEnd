from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import signals


# Create your models here.
# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance, **kwargs)
#
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class Profile(models.Model):
    phone_number = models.IntegerField(blank=False)
    middle_name = models.CharField(blank=True, max_length=255, null=True)
    image = models.ImageField(blank=True, default='default.jpg', upload_to='medicines/')
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                blank=False,
                                related_name='profile',
                                verbose_name='user_Profile', )

    class Meta:
        verbose_name_plural = 'Profiles'
        verbose_name = 'Profile'


def is_available(available):
    return "available" if available is True else 'not available'


class Medicines(models.Model):
    user = models.ForeignKey(User,
                             related_name="medicines",
                             on_delete=models.CASCADE,
                             blank=True, null=True)
    name = models.CharField(max_length=100, blank=False)
    image = models.ImageField(upload_to='media', blank=True, null=True, default='default.jpg')

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Medicines'
        verbose_name = 'Medicine'

    def __str__(self):
        return self.name


class MedicinesInfo(models.Model):
    price = models.IntegerField(blank=False)
    created = models.DateTimeField(verbose_name='date_published', auto_now_add=True, blank=True)
    available = models.BooleanField(default=False, verbose_name='доступный')
    information = models.TextField(blank=False)
    medicine = models.OneToOneField(Medicines,
                                    related_name='medicines_info',
                                    on_delete=models.CASCADE,
                                    null=True)

    class Meta:
        ordering = ['-price']
        verbose_name_plural = 'Medicines Information'
        verbose_name = 'Medicine Information'

    def __str__(self):
        return '%s: price - %i. %s' % (self.medicine.name, self.price, is_available(self.available))

