"""
This module is used to put all of the pieces together and provide a single
point of entry to get logs pulled, parsed, and stored. The only important
function in this module for users is :func:`pull_and_parse_logs`. This is what
the celery task and the Django management command (tamarin_pull_logs) call
to get things going.
"""
import logging
import gzip
import dateutil.parser
import tempfile
import boto
from boto.exception import S3ResponseError
from django.conf import settings
from tamarin.models import CloudFrontLoggedDistribution, CloudFrontLogRecord
from tamarin.parser import CloudFrontLogParser

# Logger for this module.
LOGGER = logging.getLogger(__name__)

def store_parsed_entry(parsed):
    """
    Given a parsed log entry, copy the values from the parser's output to
    a CloudFrontLogRecord object. If the log already exists, update the values.
    
    :param pyparsing.ParseResults parsed: The parsed results for a single
        log entry.
    :rtype: CloudFrontLogRecord
    :returns: The updated or newly created S3LogRecord object for the
        parsed log entry.
    """
    
    distribution, b_created = CloudFrontLoggedDistribution.objects.get_or_create(name=parsed['cs_host'])
    
    request_dtime = dateutil.parser.parse("%s %s" % (parsed['request_date_string'], parsed['request_time_string']))
    
    # The field will now be blank in the model if it was initially a hypen
    if parsed['query_string'] == '-':
        parsed['query_string'] = None
    
    records = CloudFrontLogRecord.objects.filter(distribution=distribution,
                                                 request_dtime=request_dtime,
                                                 edge_location=parsed['edge_location'],
                                                 bytes_sent=parsed['bytes_sent'],
                                                 remote_ip=parsed['remote_ip'],
                                                 cs_host=parsed['cs_host'],
                                                 http_method=parsed['http_method'],
                                                 cs_uri_stem=parsed['cs_uri_stem'],
                                                 http_status=parsed['http_status'],
                                                 referrer=parsed['referrer'],
                                                 user_agent=parsed['user_agent'],
                                                 query_string=parsed['query_string'])
    
    if len(records) > 0:
        assert len(records) == 1
        return records[0]
    else:
        record = CloudFrontLogRecord(distribution=distribution,
                                 request_dtime=request_dtime,
                                 edge_location=parsed['edge_location'],
                                 bytes_sent=parsed['bytes_sent'],
                                 remote_ip=parsed['remote_ip'],
                                 cs_host=parsed['cs_host'],
                                 http_method=parsed['http_method'],
                                 cs_uri_stem=parsed['cs_uri_stem'],
                                 http_status=parsed['http_status'],
                                 referrer=parsed['referrer'],
                                 user_agent=parsed['user_agent'],
                                 query_string=parsed['query_string'])
    
    record.save()
    
    return record

def pull_and_parse_logs():
    """
    Pulls all of the keys from the bucket's log bucket, hands them off to the
    parser, then stores the values in S3LogRecord objects.
    """
    # When True, delete S3 log keys after they have been parsed.
    purge_parsed_keys = getattr(settings, 'TAMARIN_PURGE_PARSED_KEYS', 
    (not settings.DEBUG))
    # All buckets with monitor_bucket == True (active).
    logged_buckets = CloudFrontLoggedDistribution.objects.get_log_buckets_to_monitor()
    conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID,
                           settings.AWS_SECRET_ACCESS_KEY)

    for logged_bucket in logged_buckets:
        bucket = conn.get_bucket(logged_bucket.log_bucket_name)
        for key in bucket.get_all_keys():
            LOGGER.debug(key)

            log_file = tempfile.NamedTemporaryFile()

            try:
                # Stuff the entire contents of the S3 key into string variable.

                key_contents = key.get_contents_to_file(log_file)
                log_file.flush()
                log_contents = gzip.open(log_file.name).read()
                
                # Skip version and field names lines
                log_contents = "\n".join(log_contents.split("\n")[2:])
            except S3ResponseError:
                # We're going to get a response error from time to time, S3
                # is not bullet proof. In this case, move on to the next
                # key and a later execution of the puller will grab this one.
                print "S3ResponseError encountered when retrieving: %s" % key
                continue

            parser = CloudFrontLogParser(log_contents)
            for log_entry in parser.parse_lines():
                store_parsed_entry(log_entry)

            if purge_parsed_keys:
                # Delete the key after parsing it if the
                # TAMARIN_PURGE_PARSED_KEYS setting is True. 
                key.delete()
