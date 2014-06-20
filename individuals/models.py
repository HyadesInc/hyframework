from django.db import models
from django.contrib import admin

# Create your models here.

class Individual(models.Model):
    class Meta:
        verbose_name = "Individual"
        verbose_name_plural = "Individuals"
        
    
    receita_name = models.CharField(max_length=255, verbose_name="Name as in Receita Federal")
    
    cpf = models.CharField(max_length=11, verbose_name="CPF", unique=True)    

    
    def __unicode__(self):
        return unicode(self.type + ' ' + self.destination_url + ' ' + self.username)

class IndividualAdmin(admin.ModelAdmin):
    list_display = ['receita_name','cpf']
    list_filter = ['receita_name','cpf']
    search_fields = ['receita_name','cpf']

try: 
    admin.site.register(Individual, IndividualAdmin)
except:
    pass