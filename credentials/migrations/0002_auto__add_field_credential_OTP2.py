# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Credential.OTP2'
        db.add_column(u'credentials_credential', 'OTP2',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)
        db.create_unique('credentials_credential', ['type', 'destination_url', 'destination_port', 'username', 'password'])
        db.create_unique('credentials_credential', ['type', 'destination_ip', 'destination_port', 'username', 'password'])


    def backwards(self, orm):
        # Deleting field 'Credential.OTP2'
        db.delete_column(u'credentials_credential', 'OTP2')
        db.delete_unique('credentials_credential', ['type', 'destination_url', 'destination_port', 'username', 'password'])
        db.delete_unique('credentials_credential', ['type', 'destination_ip', 'destination_port', 'username', 'password'])


    models = {
        u'credentials.credential': {
            'Meta': {'object_name': 'Credential'},
            'OTP': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'OTP2': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
