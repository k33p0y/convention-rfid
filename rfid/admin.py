from django.contrib import admin
from .models import Participant, Rfid, Convention, Society, Occupation

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('prc_num', 'fname', 'lname', 'mname', 'birthdate', 'address')

@admin.register(Society)
class SocietyAdmin(admin.ModelAdmin):
    pass

@admin.register(Rfid)
class RfidAdmin(admin.ModelAdmin):
    list_display = ('rfid_num', 'participant', 'society')

@admin.register(Convention)
class ConventionAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_start', 'date_end', 'venue', 'is_open')
    list_filter = ('is_open', )

@admin.register(Occupation)
class OccupationAdmin(admin.ModelAdmin):
    list_display = ('name', 'initials')