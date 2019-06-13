import uuid
from django.db import models

class Society(models.Model):
    society_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Society'
        verbose_name_plural = 'Societies'

    def __str__(self):
        return self.name

class Membership(models.Model):
    membership_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Participant(models.Model):
    participant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rfid = models.CharField('RFID', max_length=15, unique=True)
    fname = models.CharField('First name', max_length=100)
    mname = models.CharField('Middle name', max_length=100, blank=True)
    lname = models.CharField('Last name', max_length=100)
    prc_num = models.CharField('PRC', max_length=15, unique=True)
    birthdate = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True)
    society = models.ForeignKey(Society, on_delete=models.SET_NULL, null=True, blank=True, related_name='participants')
    membership = models.ForeignKey(Membership, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.fname, self.lname)

class Convention(models.Model):
    convention_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    date_start = models.DateField()
    date_end = models.DateField()
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name