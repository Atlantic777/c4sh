# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('backend_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('backend', ['UserProfile'])

        # Adding model 'Ticket'
        db.create_table('backend_ticket', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('receipt_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('invoice_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sale_price', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('invoice_price', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(default='EUR', max_length=3)),
            ('tax_rate', self.gf('django.db.models.fields.SmallIntegerField')(default=19)),
            ('rabate_rate', self.gf('django.db.models.fields.SmallIntegerField')(default=0)),
            ('limit_timespan', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('valid_from', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('valid_until', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('limit_supervisor', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('receipt_autoprint', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('receipt_advice', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('invoice_autoprint', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('invoice_advice', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('backend', ['Ticket'])

        # Adding model 'Cashdesk'
        db.create_table('backend_cashdesk', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('invoice_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(unique=True, max_length=15)),
            ('receipt_printer', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('invoice_printer', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('invoice_printer_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('allow_supervisor', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('active_session', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='active_session_set', unique=True, null=True, to=orm['backend.CashdeskSession'])),
        ))
        db.send_create_signal('backend', ['Cashdesk'])

        # Adding model 'CashdeskSession'
        db.create_table('backend_cashdesksession', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cashdesk', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Cashdesk'])),
            ('cashier', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('supervisor_before', self.gf('django.db.models.fields.related.ForeignKey')(related_name='supervised_before_cashdisksession_set', to=orm['auth.User'])),
            ('valid_from', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('valid_until', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('change', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('is_logged_in', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('was_logged_in', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('drawer_sum', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True)),
            ('drawer_sum_ok', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('supervisor_after', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='supervised_after_cashdisksession_set', null=True, to=orm['auth.User'])),
            ('total', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=7, decimal_places=2, blank=True)),
        ))
        db.send_create_signal('backend', ['CashdeskSession'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('backend_userprofile')

        # Deleting model 'Ticket'
        db.delete_table('backend_ticket')

        # Deleting model 'Cashdesk'
        db.delete_table('backend_cashdesk')

        # Deleting model 'CashdeskSession'
        db.delete_table('backend_cashdesksession')


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
            'rabate_rate': ('django.db.models.fields.SmallIntegerField', [], {'default': '0'}),
            'receipt_advice': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'receipt_autoprint': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'receipt_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sale_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tax_rate': ('django.db.models.fields.SmallIntegerField', [], {'default': '19'}),
            'valid_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'valid_until': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'backend.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['backend']