# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'SalePosition.uuid'
        db.add_column('desk_saleposition', 'uuid',
                      self.gf('django.db.models.fields.CharField')(max_length=65, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'SalePosition.uuid'
        db.delete_column('desk_saleposition', 'uuid')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'backend.cashdesk': {
            'Meta': {'ordering': "['name']", 'object_name': 'Cashdesk'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'active_session': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'active_session_set'", 'unique': 'True', 'null': 'True', 'to': "orm['backend.CashdeskSession']"}),
            'allow_supervisor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'invoice_printer': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'invoice_printer_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'unique': 'True', 'max_length': '15'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'receipt_printer': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'backend.cashdesksession': {
            'Meta': {'ordering': "['valid_from', 'cashdesk']", 'object_name': 'CashdeskSession'},
            'cashdesk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Cashdesk']"}),
            'cashier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'change': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'drawer_sum': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'drawer_sum_ok': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_logged_in': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'supervisor_after': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'supervised_after_cashdisksession_set'", 'null': 'True', 'to': "orm['auth.User']"}),
            'supervisor_before': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'supervised_before_cashdisksession_set'", 'to': "orm['auth.User']"}),
            'total': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'valid_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'valid_until': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'was_logged_in': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'backend.ticket': {
            'Meta': {'ordering': "['active', 'name', '-sale_price']", 'object_name': 'Ticket'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'EUR'", 'max_length': '3'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_advice': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_autoprint': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'invoice_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'invoice_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'limit_supervisor': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'limit_timespan': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'preorder_sold': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rabate_rate': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'receipt_advice': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'receipt_autoprint': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'receipt_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sale_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tax_rate': ('django.db.models.fields.SmallIntegerField', [], {'default': '19'}),
            'valid_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'valid_until': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'desk.sale': {
            'Meta': {'object_name': 'Sale'},
            'cached_sum': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'cashdesk': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Cashdesk']"}),
            'cashier': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'fulfilled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reversed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.CashdeskSession']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'desk.saleposition': {
            'Meta': {'object_name': 'SalePosition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'rabate_rate': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sale': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['desk.Sale']"}),
            'sale_price': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '7', 'decimal_places': '2', 'blank': 'True'}),
            'supervisor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'authorized_positions'", 'null': 'True', 'to': "orm['auth.User']"}),
            'tax_rate': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ticket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['backend.Ticket']"}),
            'uuid': ('django.db.models.fields.CharField', [], {'max_length': '65', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['desk']