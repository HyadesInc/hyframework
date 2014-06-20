# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Individual'
        db.create_table(u'individuals_individual', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('receita_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cpf', self.gf('django.db.models.fields.IntegerField')(unique=True, max_length=11)),
        ))
        db.send_create_signal(u'individuals', ['Individual'])


    def backwards(self, orm):
        # Deleting model 'Individual'
        db.delete_table(u'individuals_individual')


    models = {
        u'individuals.individual': {
            'Meta': {'object_name': 'Individual'},
            'cpf': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'max_length': '11'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receita_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['individuals']