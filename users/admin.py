from django.contrib import admin
from .models import UserOrganizationMembership
from .models import UserOrganizationInvite

admin.site.register(UserOrganizationMembership)
admin.site.register(UserOrganizationInvite)
