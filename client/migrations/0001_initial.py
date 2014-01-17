# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Client'
        db.create_table(u'client_client', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('on_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('client_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=3)),
            ('client_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('client_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('awb_assigned_from', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('awb_assigned_to', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('awb_left', self.gf('django.db.models.fields.IntegerField')(max_length=10)),
        ))
        db.send_create_signal(u'client', ['Client'])

        # Adding model 'Client_Additional'
        db.create_table(u'client_client_additional', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('on_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('client', self.gf('django.db.models.fields.related.OneToOneField')(related_name='additional', unique=True, to=orm['client.Client'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=50, null=True, blank=True)),
            ('scheduling_time', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('pan_no', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('tan_no', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('bank_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('account_no', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('city', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zoning.City'], null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=13)),
        ))
        db.send_create_signal(u'client', ['Client_Additional'])

        # Adding model 'Client_Warehouse'
        db.create_table(u'client_client_warehouse', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('on_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('warehouse_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(related_name='warehouse', to=orm['client.Client'])),
            ('pincode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zoning.Pincode'])),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=13)),
        ))
        db.send_create_signal(u'client', ['Client_Warehouse'])

        # Adding model 'Services'
        db.create_table(u'client_services', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('on_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('service', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'client', ['Services'])

        # Adding model 'Client_Services'
        db.create_table(u'client_client_services', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('on_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['client.Client'])),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['client.Services'])),
        ))
        db.send_create_signal(u'client', ['Client_Services'])


    def backwards(self, orm):
        # Deleting model 'Client'
        db.delete_table(u'client_client')

        # Deleting model 'Client_Additional'
        db.delete_table(u'client_client_additional')

        # Deleting model 'Client_Warehouse'
        db.delete_table(u'client_client_warehouse')

        # Deleting model 'Services'
        db.delete_table(u'client_services')

        # Deleting model 'Client_Services'
        db.delete_table(u'client_client_services')


    models = {
        u'client.client': {
            'Meta': {'object_name': 'Client'},
            'awb_assigned_from': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'awb_assigned_to': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'awb_left': ('django.db.models.fields.IntegerField', [], {'max_length': '10'}),
            'client_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'client_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'client_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'client.client_additional': {
            'Meta': {'object_name': 'Client_Additional'},
            'account_no': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['zoning.City']", 'null': 'True', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'additional'", 'unique': 'True', 'to': u"orm['client.Client']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pan_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'scheduling_time': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'tan_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'client.client_services': {
            'Meta': {'object_name': 'Client_Services'},
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['client.Client']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['client.Services']"})
        },
        u'client.client_warehouse': {
            'Meta': {'object_name': 'Client_Warehouse'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'warehouse'", 'to': u"orm['client.Client']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '13'}),
            'pincode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['zoning.Pincode']"}),
            'warehouse_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'client.services': {
            'Meta': {'object_name': 'Services'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'service': ('django.db.models.fields.CharField', [], {'max_length': '3'})
        },
        u'zoning.city': {
            'Meta': {'object_name': 'City'},
            'city': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'zoning.pincode': {
            'Meta': {'object_name': 'Pincode'},
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['zoning.City']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pincode': ('django.db.models.fields.IntegerField', [], {'unique': 'True', 'max_length': '6'})
        }
    }

    complete_apps = ['client']