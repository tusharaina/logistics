# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DRS.opening_km'
        db.add_column(u'transit_drs', 'opening_km',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)

        # Adding field 'DRS.closing_km'
        db.add_column(u'transit_drs', 'closing_km',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'DRS.opening_km'
        db.delete_column(u'transit_drs', 'opening_km')

        # Deleting field 'DRS.closing_km'
        db.delete_column(u'transit_drs', 'closing_km')


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
        u'transit.tb_history': {
            'Meta': {'object_name': 'TB_History'},
            'branch': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['internal.Branch']", 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mts': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['transit.MTS']", 'null': 'True', 'blank': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'tb': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tb_history'", 'to': u"orm['transit.TB']"})
        },
        u'zoning.city': {
            'Meta': {'object_name': 'City'},
            'city': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['transit']