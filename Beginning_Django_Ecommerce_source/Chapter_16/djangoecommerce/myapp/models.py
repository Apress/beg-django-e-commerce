# -*- coding: utf-8 -*-
from django.db.models import permalink, signals
from google.appengine.ext import db
from ragendja.dbutils import cleanup_relations

class Person(db.Model):
    """Basic user profile with personal details."""
    first_name = db.StringProperty(required=True)
    last_name = db.StringProperty(required=True)

    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

    @permalink
    def get_absolute_url(self):
        return ('myapp.views.show_person', (), {'key': self.key()})

signals.pre_delete.connect(cleanup_relations, sender=Person)

class File(db.Model):
    owner = db.ReferenceProperty(Person, required=True, collection_name='file_set')
    name = db.StringProperty(required=True)
    file = db.BlobProperty(required=True)

    @permalink
    def get_absolute_url(self):
        return ('myapp.views.download_file', (), {'key': self.key(),
                                                  'name': self.name})

    def __unicode__(self):
        return u'File: %s' % self.name

class Contract(db.Model):
    employer = db.ReferenceProperty(Person, required=True, collection_name='employee_contract_set')
    employee = db.ReferenceProperty(Person, required=True, collection_name='employer_contract_set')
    start_date = db.DateTimeProperty()
    end_date = db.DateTimeProperty()
