from django.db import models
import datetime
from django.utils.timezone import localtime


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def get_duration(visit):
    entered_time = localtime(visit.entered_at)
    leaved_time = localtime(visit.leaved_at)
    delta = leaved_time - entered_time
    return delta.total_seconds()


def format_duration(delta):
    seconds_in_minute = 60
    seconds_in_hour = 3600
    hours = delta // seconds_in_hour
    minutes = (delta % seconds_in_hour) // seconds_in_minute
    return f'{int(hours):02}:{int(minutes):02}'


def is_visit_long(visit):
    hours_threshold = 1
    delta = get_duration(visit)
    seconds_in_hour = datetime.timedelta(hours=hours_threshold).total_seconds()
    return delta > seconds_in_hour
