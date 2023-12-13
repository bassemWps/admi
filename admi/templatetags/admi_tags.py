import os
from datetime import date
from django import template
from django.db.models import Count
from admi.models import *

from datetime import datetime

register = template.Library()



@register.inclusion_tag('latest.html')
def get_dde():
    date = datetime.now()
    getp = PasserConge.objects.filter(Accepte=False,Refuse=False,DateDemande__year = date.year
 )


   
    return {'getp':getp}