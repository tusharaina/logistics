# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Services'
        db.delete_table(u'client_services')

        # Deleting model 'Client_Services'
        db.delete_table(u'client_client_services')


        # Changing field 'Client_Additional.bank_name'
        db.alter_column(u'client_client_additional', 'bank_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Client_Additional.phone'
        db.alter_column(u'client_client_additional', 'phone', self.gf('django.db.models.fields.CharField')(max_length=13, null=True))

        # Changing field 'Client_Additional.address'
        db.alter_column(u'client_client_additional', 'address', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Client_Additional.account_no'
        db.alter_column(u'client_client_additional', 'account_no', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

        # Changing field 'Client_Warehouse.phone'
        db.alter_column(u'client_client_warehouse', 'phone', self.gf('django.db.models.fields.CharField')(max_length=13, null=True))

        # Changing field 'Client_Warehouse.address'
        db.alter_column(u'client_client_warehouse', 'address', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

    def backwards(self, orm):
        # Adding model 'Services'
        db.create_table(u'client_services', (
            ('on_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('service', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'client', ['Services'])

        # Adding model 'Client_Services'
        db.create_table(u'client_client_services', (
            ('on_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('service', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['client.Services'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['client.Client'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'client', ['Client_Services'])


        # User chose to not deal with backwards NULL issues for 'Client_Additional.bank_name'
        raise RuntimeError("Cannot reverse this migration. 'Client_Additional.bank_name' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Client_Additional.bank_name'
        db.alter_column(u'client_client_additional', 'bank_name', self.gf('django.db.models.fields.CharField')(max_length=50))

        # User chose to not deal with backwards NULL issues for 'Client_Additional.phone'
        raise RuntimeError("Cannot reverse this migration. 'Client_Additional.phone' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Client_Additional.phone'
        db.alter_column(u'client_client_additional', 'phone', self.gf('django.db.models.fields.CharField')(max_length=13))

        # User chose to not deal with backwards NULL issues for 'Client_Additional.address'
        raise RuntimeError("Cannot reverse this migration. 'Client_Additional.address' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Client_Additional.address'
        db.alter_column(u'client_client_additional', 'address', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'Client_Additional.account_no'
        db.alter_column(u'client_client_additional', 'account_no', self.gf('django.db.models.fields.CharField')(default=None, max_length=50))

        # User chose to not deal with backwards NULL issues for 'Client_Warehouse.phone'
        raise RuntimeError("Cannot reverse this migration. 'Client_Warehouse.phone' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'Client_Warehouse.phone'
        db.alter_column(u'client_client_warehouse', 'phone', self.gf('django.db.models.fields.CharField')(max_length=13))

        # Changing field 'Client_Warehouse.address'
        db.alter_column(u'client_client_warehouse', 'address', self.gf('django.db.models.fields.CharField')(default='', max_length=50))

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
            'account_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'bank_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['zoning.City']", 'null': 'True', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'additional'", 'unique': 'True', 'to': u"orm['client.Client']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'pan_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'scheduling_time': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'tan_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'client.client_warehouse': {
            'Meta': {'object_name': 'Client_Warehouse'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'warehouse'", 'to': u"orm['client.Client']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'}),
            'pincode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['zoning.Pincode']"}),
            'warehouse_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
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