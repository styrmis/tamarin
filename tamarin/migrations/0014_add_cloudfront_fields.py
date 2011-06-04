# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'CloudFrontLogRecord'
        db.create_table('tamarin_cloudfrontlogrecord', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('distribution', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['tamarin.CloudFrontLoggedDistribution'])),
            ('request_dtime', self.gf('django.db.models.fields.DateTimeField')()),
            ('edge_location', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('bytes_sent', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('remote_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('http_method', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('cs_host', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('cs_uri_stem', self.gf('django.db.models.fields.CharField')(max_length=2048)),
            ('http_status', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('referrer', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('user_agent', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('query_string', self.gf('django.db.models.fields.CharField')(max_length=2048, null=True, blank=True)),
        ))
        db.send_create_signal('tamarin', ['CloudFrontLogRecord'])

        # Adding model 'CloudFrontLoggedDistribution'
        db.create_table('tamarin_cloudfrontloggeddistribution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
            ('log_bucket_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('monitor_distribution', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('tamarin', ['CloudFrontLoggedDistribution'])


    def backwards(self, orm):
        
        # Deleting model 'CloudFrontLogRecord'
        db.delete_table('tamarin_cloudfrontlogrecord')

        # Deleting model 'CloudFrontLoggedDistribution'
        db.delete_table('tamarin_cloudfrontloggeddistribution')


    models = {
        'tamarin.cloudfrontloggeddistribution': {
            'Meta': {'object_name': 'CloudFrontLoggedDistribution'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_bucket_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'monitor_distribution': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'tamarin.cloudfrontlogrecord': {
            'Meta': {'object_name': 'CloudFrontLogRecord'},
            'bytes_sent': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cs_host': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'cs_uri_stem': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'distribution': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tamarin.CloudFrontLoggedDistribution']"}),
            'edge_location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'http_method': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'http_status': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'query_string': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'referrer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'remote_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'request_dtime': ('django.db.models.fields.DateTimeField', [], {}),
            'user_agent': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'tamarin.s3loggedbucket': {
            'Meta': {'object_name': 'S3LoggedBucket'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log_bucket_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'monitor_bucket': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'})
        },
        'tamarin.s3logrecord': {
            'Meta': {'object_name': 'S3LogRecord'},
            'bucket': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tamarin.S3LoggedBucket']"}),
            'bucket_owner': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'bytes_sent': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'error_code': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'http_status': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'http_version': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.TextField', [], {}),
            'object_size': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'operation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'referrer': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'remote_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'request_dtime': ('django.db.models.fields.DateTimeField', [], {}),
            'request_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'request_method': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'request_uri': ('django.db.models.fields.TextField', [], {}),
            'requester': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'total_time': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'turnaround_time': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user_agent': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'version_id': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['tamarin']
