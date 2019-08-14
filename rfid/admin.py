from django.contrib import admin
from .models import Participant, Rfid, Convention, Society, Occupation

@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ('prc_num', 'fname', 'lname', 'mname', 'birthdate', 'address')
    search_fields = ('prc_num', 'fname', 'lname', 'mname')

@admin.register(Society)
class SocietyAdmin(admin.ModelAdmin):
    pass

@admin.register(Rfid)
class RfidAdmin(admin.ModelAdmin):
    list_display = ('rfid_num', 'participant', 'society')
    search_fields = ('rfid_num', 'participant__fname', 'participant_lname', 'participant_mname')

@admin.register(Convention)
class ConventionAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_start', 'date_end', 'venue', 'is_open')
    list_filter = ('is_open', )

@admin.register(Occupation)
class OccupationAdmin(admin.ModelAdmin):
    list_display = ('name', 'initials')