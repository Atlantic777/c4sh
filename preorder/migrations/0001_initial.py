# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PreorderTicket'
        db.create_table('preorder_preorderticket', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('backend_id', self.gf('django.db.models.fields.SmallIntegerField')()),
            ('price', self.gf('django.db.models.fields.DecimalField')(max_digits=7, decimal_places=2)),
            ('currency', self.gf('django.db.models.fields.CharField')(default='EUR', max_length=3)),
            ('tax_rate', self.gf('django.db.models.fields.SmallIntegerField')(default=19)),
            ('limit_timespan', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('valid_from', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('valid_until', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('limit_amount', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('limit_amount_user', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('is_ticket', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('deleted', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('preorder', ['PreorderTicket'])

        # Adding model 'PreorderPosition'
        db.create_table('preorder_preorderposition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('preorder', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['preorder.Preorder'])),
            ('ticket', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['preorder.PreorderTicket'])),
            ('uuid', self.gf('c4sh.preorder.models.UUIDField')(unique=True, max_length=64, blank=True)),
        ))
        db.send_create_signal('preorder', ['PreorderPosition'])

        # Adding model 'Preorder'
        db.create_table('preorder_preorder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('user_id', self.gf('django.db.models.fields.IntegerField')()),
            ('additional_info', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('unique_secret', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('cached_sum', self.gf('django.db.models.fields.TextField')()),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('paid_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('paid_via', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
        ))
        db.send_create_signal('preorder', ['Preorder'])


    def backwards(self, orm):
        # Deleting model 'PreorderTicket'
        db.delete_table('preorder_preorderticket')

        # Deleting model 'PreorderPosition'
        db.delete_table('preorder_preorderposition')

        # Deleting model 'Preorder'
        db.delete_table('preorder_preorder')


    models = {
        'preorder.preorder': {
            'Meta': {'object_name': 'Preorder'},
            'additional_info': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cached_sum': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'paid_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'paid_via': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'unique_secret': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'user_id': ('django.db.models.fields.IntegerField', [], {}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'preorder.preorderposition': {
            'Meta': {'object_name': 'PreorderPosition'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'preorder': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['preorder.Preorder']"}),
            'ticket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['preorder.PreorderTicket']"}),
            'uuid': ('c4sh.preorder.models.UUIDField', [], {'unique': 'True', 'max_length': '64', 'blank': 'True'})
        },
        'preorder.preorderticket': {
            'Meta': {'ordering': "['active', 'name', '-price']", 'object_name': 'PreorderTicket'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'backend_id': ('django.db.models.fields.SmallIntegerField', [], {}),
            'currency': ('django.db.models.fields.CharField', [], {'default': "'EUR'", 'max_length': '3'}),
            'deleted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ticket': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'limit_amount': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'limit_amount_user': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'limit_timespan': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'tax_rate': ('django.db.models.fields.SmallIntegerField', [], {'default': '19'}),
            'valid_from': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'valid_until': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['preorder']