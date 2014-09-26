# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VisitedLink'
        db.create_table(u'unisender_visitedlink', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('campaign', self.gf('django.db.models.fields.related.ForeignKey')(related_name='visited_links', to=orm['unisender.Campaign'])),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('request_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('count', self.gf('django.db.models.fields.SmallIntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'unisender', ['VisitedLink'])


    def backwards(self, orm):
        # Deleting model 'VisitedLink'
        db.delete_table(u'unisender_visitedlink')


    models = {
        u'unisender.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'email_message': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'attachments'", 'to': u"orm['unisender.EmailMessage']"}),
            'filename': ('filebrowser.fields.FileBrowseField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'unisender.campaign': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Campaign'},
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'campaign'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['unisender.Subscriber']"}),
            'email_message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['unisender.EmailMessage']", 'null': 'True'}),
            'err_delivery_failed': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'err_dest_invalid': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'err_domain_inactive': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'err_internal': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'err_lost': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'err_mailbox_full': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'err_not_allowed': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'err_not_available': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'err_resend': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'err_skip_letter': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'err_spam_folder': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'err_spam_rejected': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'err_spam_retry': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'err_spam_skipped': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'err_src_invalid': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'err_unsubscribed': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'err_user_inactive': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'err_user_unknown': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'err_will_retry': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_check': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'last_error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'not_sent': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'ok_delivered': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'ok_link_visited': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'ok_read': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'ok_spam_folder': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'ok_unsubscribed': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'payment_limit': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sync': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'total': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'track_ga': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '50'}),
            'track_links': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '50'}),
            'track_read': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '50'}),
            'unisender_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'unisender.emailmessage': {
            'Meta': {'ordering': "('subject',)", 'object_name': 'EmailMessage'},
            'body': ('tinymce_4.fields.TinyMCEModelField', [], {}),
            'categories': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'generate_text': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'default': "'ru'", 'max_length': '50'}),
            'last_error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'list_id': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emails'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['unisender.SubscribeList']"}),
            'sender_email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sender_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'series_day': ('django.db.models.fields.PositiveSmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'series_time': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2014, 7, 23, 0, 0)'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sync': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'emails'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['unisender.Tag']"}),
            'text_body': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'unisender_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'wrap_type': ('django.db.models.fields.CharField', [], {'default': "'skip'", 'max_length': '50'})
        },
        u'unisender.field': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Field'},
            'field_type': ('django.db.models.fields.CharField', [], {'default': "'string'", 'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sort': ('django.db.models.fields.SmallIntegerField', [], {'default': '1'}),
            'sync': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unisender_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'unisender.smsmessage': {
            'Meta': {'object_name': 'SmsMessage'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sync': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unisender_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'unisender.subscribelist': {
            'Meta': {'ordering': "('title',)", 'object_name': 'SubscribeList'},
            'after_subscribe_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'before_subscribe_url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sync': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'unisender_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'unisender.subscriber': {
            'Meta': {'ordering': "('contact',)", 'object_name': 'Subscriber'},
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'contact_type': ('django.db.models.fields.CharField', [], {'default': "'email'", 'max_length': '50'}),
            'double_optin': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'list_ids': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'subscribers'", 'symmetrical': 'False', 'to': u"orm['unisender.SubscribeList']"}),
            'sync': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'subscribers'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['unisender.Tag']"}),
            'unisender_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'unisender.subscriberfields': {
            'Meta': {'object_name': 'SubscriberFields'},
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['unisender.Field']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subscriber': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fields'", 'to': u"orm['unisender.Subscriber']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'unisender.tag': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_error': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sync': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'unisender_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'unisender.visitedlink': {
            'Meta': {'object_name': 'VisitedLink'},
            'campaign': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'visited_links'", 'to': u"orm['unisender.Campaign']"}),
            'count': ('django.db.models.fields.SmallIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'request_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        }
    }

    complete_apps = ['unisender']