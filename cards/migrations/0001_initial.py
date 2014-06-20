# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CreditCard'
        db.create_table(u'cards_creditcard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('card_type', self.gf('django.db.models.fields.CharField')(default='unknown', max_length=50)),
            ('card_holder', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('card_number', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('expiry_date_month', self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True)),
            ('expiry_date_year', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('card_code', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
        ))
        db.create_unique('cards_creditcard', ['card_type','card_number'])
        db.send_create_signal(u'cards', ['CreditCard'])


    def backwards(self, orm):
        # Deleting model 'CreditCard'
        db.delete_table(u'cards_creditcard')


    models = {
        u'cards.creditcard': {
            'Meta': {'object_name': 'CreditCard'},
            'card_code': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'card_holder': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'card_number': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'card_type': ('django.db.models.fields.CharField', [], {'default': "'unknown'", 'max_length': '50'}),
            'expiry_date_month': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'expiry_date_year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['cards']
