# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Credential'
        db.create_table(u'credentials_credential', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='GENERIC', max_length=50)),
            ('destination_url', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('destination_ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39)),
            ('destination_port', self.gf('django.db.models.fields.IntegerField')()),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('username_field', self.gf('django.db.models.fields.CharField')(max_length=60, null=True, blank=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('password_field', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('OTP', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('payload', self.gf('django.db.models.fields.TextField')(max_length=4096, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'credentials', ['Credential'])


    def backwards(self, orm):
        # Deleting model 'Credential'
        db.delete_table(u'credentials_credential')


    models = {
        u'credentials.credential': {
            'Meta': {'object_name': 'Credential'},
            'OTP': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'destination_ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39'}),
            'destination_port': ('django.db.models.fields.IntegerField', [], {}),
            'destination_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'password_field': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'payload': ('django.db.models.fields.TextField', [], {'max_length': '4096', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'GENERIC'", 'max_length': '50'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'username_field': ('django.db.models.fields.CharField', [], {'max_length': '60', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['credentials']