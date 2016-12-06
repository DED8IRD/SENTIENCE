# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime

db.define_table('shitpost',
                Field('text_post', 'text'),
                Field('image', 'text'),
                Field('upvotes', 'integer', default=0),
                Field('created_on', 'datetime', default=datetime.datetime.utcnow(), readable=False, writable=False)
                )

db.define_table('post_comment',
                Field('shitpost', 'reference shitpost', readable=False, writable=False),
                Field('user_email', default=auth.user.email if auth.user_id else None, readable=False, writable=False),
                Field('username', requires=IS_NOT_EMPTY()),
                Field('comment_content', 'text', requires=IS_NOT_EMPTY()),
                Field('created_on', 'datetime', default=datetime.datetime.utcnow(), readable=False, writable=False),
                Field('updated_on', 'datetime', update=datetime.datetime.utcnow(), readable=False, writable=False)
                )

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
