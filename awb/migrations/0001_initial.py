# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Manifest'
        db.create_table(u'awb_manifest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('on_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('client', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['client.Client'])),
            ('uploaded_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('warehouse', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['client.Client_Warehouse'])),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['internal.Branch'])),
            ('status', self.gf('django.db.models.fields.CharField')(default=u'O', max_length=1)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'awb', ['Manifest'])

        # Adding model 'AWB'
        db.create_table(u'awb_awb', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('on_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('awb', self.gf('django.db.models.fields.CharField')(unique=True, max_length=15)),
            ('order_id', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('invoice_no', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('customer_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('address_1', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('address_2', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('area', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('pincode', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zoning.Pincode'])),
            ('phone_1', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('phone_2', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('package_value', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('package_price', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('expected_amount', self.gf('django.db.models.fields.FloatField')(max_length=12, null=True, blank=True)),
            ('weight', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('length', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('breadth', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('height', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('package_sku', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('priority', self.gf('django.db.models.fields.CharField')(default=u'N', max_length=1)),
            ('barcode', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'awb', ['AWB'])

        # Adding model 'AWB_Status'
        db.create_table(u'awb_awb_status', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('on_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('awb', self.gf('django.db.models.fields.related.OneToOneField')(related_name=u'awb_status', unique=True, to=orm['awb.AWB'])),
            ('manifest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['awb.Manifest'], null=True, blank=True)),
            ('current_branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['internal.Branch'], null=True, blank=True)),
            ('current_tb', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transit.TB'], null=True, blank=True)),
            ('current_mts', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transit.MTS'], null=True, blank=True)),
            ('current_drs', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transit.DRS'], null=True, blank=True)),
            ('current_dto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transit.DTO'], null=True, blank=True)),
            ('current_fe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['internal.Employee'], null=True, blank=True)),
            ('collected_amt', self.gf('django.db.models.fields.FloatField')(max_length=12, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default=u'DR', max_length=3)),
            ('zone', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['zoning.Zone'], null=True, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(default=u'', max_length=200, blank=True)),
            ('reason', self.gf('django.db.models.fields.CharField')(default=u'', max_length=200, blank=True)),
            ('updated_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
        ))
        db.send_create_signal(u'awb', ['AWB_Status'])

        # Adding model 'AWB_History'
        db.create_table(u'awb_awb_history', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('on_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('awb', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['awb.AWB'])),
            ('tb', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transit.TB'], null=True, blank=True)),
            ('mts', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transit.MTS'], null=True, blank=True)),
            ('drs', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transit.DRS'], null=True, blank=True)),
            ('dto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transit.DTO'], null=True, blank=True)),
            ('rto', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['transit.RTO'], null=True, blank=True)),
            ('fe', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['internal.Employee'], null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('branch', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['internal.Branch'], null=True, blank=True)),
        ))
        db.send_create_signal(u'awb', ['AWB_History'])


    def backwards(self, orm):
        # Deleting model 'Manifest'
        db.delete_table(u'awb_manifest')

        # Deleting model 'AWB'
        db.delete_table(u'awb_awb')

        # Deleting model 'AWB_Status'
        db.delete_table(u'awb_awb_status')

        # Deleting model 'AWB_History'
        db.delete_table(u'awb_awb_history')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'awb.awb': {
            'Meta': {'object_name': 'AWB'},
            'address_1': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'address_2': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'awb': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'barcode': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'breadth': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'customer_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'expected_amount': ('django.db.models.fields.FloatField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_no': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'length': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'order_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'package_price': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'package_sku': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'package_value': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'phone_1': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'phone_2': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'pincode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['zoning.Pincode']"}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "u'N'", 'max_length': '1'}),
            'weight': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        u'awb.awb_history': {
            'Meta': {'object_name': 'AWB_History'},
            'awb': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['awb.AWB']"}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internal.Branch']", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'drs': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transit.DRS']", 'null': 'True', 'blank': 'True'}),
            'dto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transit.DTO']", 'null': 'True', 'blank': 'True'}),
            'fe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internal.Employee']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mts': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transit.MTS']", 'null': 'True', 'blank': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'rto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transit.RTO']", 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'tb': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transit.TB']", 'null': 'True', 'blank': 'True'})
        },
        u'awb.awb_status': {
            'Meta': {'object_name': 'AWB_Status'},
            'awb': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "u'awb_status'", 'unique': 'True', 'to': u"orm['awb.AWB']"}),
            'collected_amt': ('django.db.models.fields.FloatField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'current_branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internal.Branch']", 'null': 'True', 'blank': 'True'}),
            'current_drs': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transit.DRS']", 'null': 'True', 'blank': 'True'}),
            'current_dto': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transit.DTO']", 'null': 'True', 'blank': 'True'}),
            'current_fe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internal.Employee']", 'null': 'True', 'blank': 'True'}),
            'current_mts': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transit.MTS']", 'null': 'True', 'blank': 'True'}),
            'current_tb': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transit.TB']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'manifest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['awb.Manifest']", 'null': 'True', 'blank': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '200', 'blank': 'True'}),
            'remark': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '200', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'DR'", 'max_length': '3'}),
            'updated_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'zone': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['zoning.Zone']", 'null': 'True', 'blank': 'True'})
        },
        u'awb.manifest': {
            'Meta': {'object_name': 'Manifest'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internal.Branch']"}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['client.Client']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "u'O'", 'max_length': '1'}),
            'uploaded_by': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'warehouse': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['client.Client_Warehouse']"})
        },
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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'internal.branch': {
            'Meta': {'object_name': 'Branch'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'branch_manager': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'branch_employee'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.User']"}),
            'branch_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['zoning.City']", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '13', 'null': 'True', 'blank': 'True'})
        },
        u'internal.employee': {
            'Meta': {'object_name': 'Employee'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internal.Branch']", 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['zoning.City']", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'internal.vehicle': {
            'Meta': {'object_name': 'Vehicle'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internal.Branch']", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'driver_name': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'vehicle_no': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'vehicle_type': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        u'transit.drs': {
            'Meta': {'object_name': 'DRS'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internal.Branch']"}),
            'closing_km': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'drs_id': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'fe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'opening_km': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'O'", 'max_length': '1'}),
            'vehicle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internal.Vehicle']"})
        },
        u'transit.dto': {
            'Meta': {'object_name': 'DTO'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internal.Branch']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'dto_id': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'fe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'O'", 'max_length': '1'}),
            'vehicle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internal.Vehicle']"})
        },
        u'transit.mts': {
            'Meta': {'object_name': 'MTS'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_branch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'from'", 'to': u"orm['internal.Branch']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mts_id': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'}),
            'to_branch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'to'", 'to': u"orm['internal.Branch']"}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'})
        },
        u'transit.rto': {
            'Meta': {'object_name': 'RTO'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internal.Branch']"}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fe': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'rto_id': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'O'", 'max_length': '1'}),
            'vehicle': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internal.Vehicle']"})
        },
        u'transit.tb': {
            'Meta': {'object_name': 'TB'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'delivery_branch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'delivery'", 'to': u"orm['internal.Branch']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'origin_branch': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'origin'", 'to': u"orm['internal.Branch']"}),
            'tb_id': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'})
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
        },
        u'zoning.zone': {
            'Meta': {'object_name': 'Zone'},
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'zone': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1'})
        }
    }

    complete_apps = ['awb']