# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Individual.cpf'
        db.alter_column(u'individuals_individual', 'cpf', self.gf('django.db.models.fields.CharField')(unique=True, max_length=11))

    def backwards(self, orm):

        # Changing field 'Individual.cpf'
        db.alter_column(u'individuals_individual', 'cpf', self.gf('django.db.models.fields.IntegerField')(max_length=11, unique=True))

    models = {
        u'individuals.individual': {
            'Meta': {'object_name': 'Individual'},
            'cpf': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '11'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'receita_name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['individuals']