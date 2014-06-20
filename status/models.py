from django.db import models

class Status(models.Model):
    class Meta:
        verbose_name = "Status"
        verbose_name_plural = "Status"
        
    name = models.CharField(max_length=255, verbose_name='Name')
    pid = models.IntegerField(verbose_name='PID')
    status = models.BooleanField(default=False, verbose_name='Status')
    
    def __unicode__(self):
        return unicode(self.name)