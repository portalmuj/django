from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Employer(models.Model):
    companyName = models.CharField(max_length=50)
    user = models.OneToOneField(User, related_name='employer', on_delete=models.CASCADE, null=True, )
    description = models.TextField()
    def __str__(self):
        return self.companyName
    def get_absolute_url(self):
        return reverse('offer_list_by_employer', args=[str(self.id)])



class Offer(models.Model):
    company = models.ForeignKey(Employer, models.CASCADE)
    position = models.CharField(max_length=50)
    branch = models.CharField(max_length=50, default="Inne")
    description = models.TextField()
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    def get_url(self):
        return reverse('offer', args=[str(self.id)])
    def __str__(self):
        return "%s: %s " %(self.company.companyName, self.position)



class Question(models.Model):
    offer = models.ForeignKey(Offer, models.CASCADE)
    text = models.TextField(max_length=1000, verbose_name=('Pytanie'))
    def __str__(self):
        return "%s: %s " %(self.offer, self.text[:50])



class Form(models.Model):
    offer = models.ForeignKey(Offer, models.CASCADE)
    forename = models.CharField(max_length=50, verbose_name=('Imię'))
    surname = models.CharField(max_length=50, verbose_name=('Nazwisko'))
    email = models.CharField(max_length=50, verbose_name=('Adres email'))
    phoneNumber = models.CharField(max_length=50, verbose_name=('Numer telefonu'))
    answer = models.TextField(verbose_name=('Odpowiedź'));

    file = models.FileField(upload_to='documents/')
    def __str__(self):
        return "%s %s" %(self.forename, self.surname)
