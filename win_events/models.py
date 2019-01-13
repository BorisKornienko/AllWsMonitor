from django.db import models


class Event(models.Model):
    event_id = models.CharField(max_length=16)
    event_source = models.CharField(max_length=200)
    event_description = models.TextField()
    machine_name = models.CharField(max_length=32)
    events_count = models.IntegerField(null=True)
    event_user = models.CharField(max_length=64)
    event_date = models.DateField(auto_now=False, auto_now_add=False)

    class Meta:
        abstract = True
    
    def __str__(self):
        return "{} -- {}".format(self.event_id, self.machine_name)


class System_warning(Event):
    pass


class System_error(Event):
    pass


class System_critical(Event):
    pass


class App_warning(Event):
    pass


class App_error(Event):
    pass


class App_critical(Event):
    pass


class Proceed_date(models.Model):
    machine = models.CharField(max_length=36)
    date_time_proc = models.DateTimeField(auto_now=True)
    file_date = models.DateField(blank=True, null=True)
    file_count = models.IntegerField(default=0)

    def __str__(self):
        return '{} {}'.format(self.machine, self.date_time_proc)
