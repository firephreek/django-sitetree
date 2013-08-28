# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ValidationMethod'
        db.create_table(u'sitetree_validationmethod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('method_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('parameters', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('keyword_args', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'sitetree', ['ValidationMethod'])

        # Adding model 'TreeItemValidationMethod'
        db.create_table(u'sitetree_treeitemvalidationmethod', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('validation_method_instance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sitetree.ValidationMethod'])),
            ('tree_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sitetree.TreeItem'])),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'sitetree', ['TreeItemValidationMethod'])

        # Adding field 'TreeItem.rule_order'
        db.add_column(u'sitetree_treeitem', 'rule_order',
                      self.gf('django.db.models.fields.CharField')(default='PO', max_length=3),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'ValidationMethod'
        db.delete_table(u'sitetree_validationmethod')

        # Deleting model 'TreeItemValidationMethod'
        db.delete_table(u'sitetree_treeitemvalidationmethod')

        # Deleting field 'TreeItem.rule_order'
        db.delete_column(u'sitetree_treeitem', 'rule_order')


    models = {
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sitetree.tree': {
            'Meta': {'object_name': 'Tree'},
            'alias': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        u'sitetree.treeitem': {
            'Meta': {'unique_together': "(('tree', 'alias'),)", 'object_name': 'TreeItem'},
            'access_loggedin': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'access_perm_type': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'access_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'access_restricted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'alias': ('sitetree.models.CharFieldNullable', [], {'db_index': 'True', 'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'hint': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inbreadcrumbs': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'inmenu': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'insitetree': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sitetree.TreeItem']", 'null': 'True', 'blank': 'True'}),
            'rule_order': ('django.db.models.fields.CharField', [], {'default': "'PO'", 'max_length': '3'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'tree': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sitetree.Tree']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'urlaspattern': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'validation_methods': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['sitetree.ValidationMethod']", 'through': u"orm['sitetree.TreeItemValidationMethod']", 'symmetrical': 'False'})
        },
        u'sitetree.treeitemvalidationmethod': {
            'Meta': {'object_name': 'TreeItemValidationMethod'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {}),
            'tree_item': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sitetree.TreeItem']"}),
            'validation_method_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sitetree.ValidationMethod']"})
        },
        u'sitetree.validationmethod': {
            'Meta': {'object_name': 'ValidationMethod'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keyword_args': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'method_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parameters': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['sitetree']