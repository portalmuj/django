
from django.contrib import admin
from .models import ( Employer, Offer, Form, Question, )


admin.site.register(Employer)
admin.site.register(Offer)
admin.site.register(Form)
admin.site.register(Question)
