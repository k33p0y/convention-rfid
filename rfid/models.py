import uuid
from django.db import models

class Society(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Society'
        verbose_name_plural = 'Societies'

    def __str__(self):
        return self.name

class Participant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fname = models.CharField('First name', max_length=100)
    mname = models.CharField('Middle name', max_length=100, blank=True)
    lname = models.CharField('Last name', max_length=100)
    prc_num = models.CharField('PRC#', max_length=15, unique=True)
    birthdate = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '%s %s' % (self.fname, self.lname)

class Rfid(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rfid_num = models.CharField('RFID', max_length=15, unique=True)
    participant = models.ForeignKey(Participant, on_delete=models.CASCADE)
    society = models.ForeignKey(Society, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    # class Meta:
    #     unique_together = ('rfid_num', 'society',)
    
    def __str__(self):
        return self.rfid_num

class Convention(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250)
    date_start = models.DateField()
    date_end = models.DateField(blank=True, null=True)
    venue = models.TextField(max_length=250)
    is_open = models.BooleanField(default=False)
    rfids = models.ManyToManyField(Rfid, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rfid = models.ForeignKey(Rfid, on_delete=models.CASCADE)
    convention = models.ForeignKey(Convention, on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    check_in = models.TimeField(auto_now_add=True)
    check_out = models.TimeField(blank=True, null=True)

    def __str__(self):
        return '%s-%s' % (self.rfid, self.convention)