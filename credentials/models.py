from django.db import models
from django.contrib import admin

# Create your models here.

# Principal modelo de salas de aula
class Credential(models.Model):
    class Meta:
        verbose_name = "Credential"
        verbose_name_plural = "Credentials"
        
    CREDENTIAL_TYPES = (
             ('FACEBOOK', 'Facebook'),
             ('TWITTER', 'Twitter'),
             ('WORDPRESS', 'Wordpress'),
             ('GENERIC', 'Generic'),
             ('FTP', 'FTP'),
             ('FATECSPSAN', 'FatecSP SAN'),
             )
    # Status do agente
    type = models.CharField(max_length=50,
                                      choices=CREDENTIAL_TYPES,
                                      default='GENERIC')
    
    destination_url = models.CharField(max_length=255, verbose_name="Destination URL", null=True, blank=True)
    
    destination_ip = models.GenericIPAddressField(verbose_name="Destination IP")
    
    destination_port = models.IntegerField(verbose_name="Destination Port")
    
    username = models.CharField(max_length=60, verbose_name="Username")
    username_field = models.CharField(max_length=60, verbose_name="Username Field", null=True, blank=True)
    
    password = models.CharField(max_length=150, verbose_name="Password")
    password_field = models.CharField(max_length=150, verbose_name="Password Field", null=True, blank=True)

    OTP = models.BooleanField(default=False, verbose_name='OTP', help_text='If a OTP was detected during the authentication, it is possible that the username+password alone won\'t suffice, so try checking the payload for possible useful information')

    payload = models.TextField(max_length=4096, verbose_name="Payload", null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    
    unique_together = (("type", "destination_url", "destination_port", "username", "password"), ("type", "destination_ip", "destination_port", "username", "password"),)

    
    def __unicode__(self):
        return unicode(self.type + ' ' + self.destination_url + ' ' + self.username)

class CredentialAdmin(admin.ModelAdmin):
    list_display = ['type', 'destination_url', 'destination_ip', 'username', 'created']
    list_filter = ['type', 'destination_url', 'destination_ip', 'username', 'created']
    search_fields = ['type', 'destination_url', 'destination_ip', 'username', 'created']
    readonly_fields = ('created',)


try: 
    admin.site.register(Credential, CredentialAdmin)
except:
    pass