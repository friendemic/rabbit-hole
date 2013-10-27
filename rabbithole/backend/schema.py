from sqlalchemy import Table, Column, String, MetaData, Integer, DateTime
from sqlalchemy import Boolean, Text

metadata = MetaData()
content_facebook = Table('content_facebook', metadata,
                         Column('id', String(100), primary_key=True),
                         Column('fb_account', String(100)),
                         Column('message', String(5000)),
                         Column('is_self', Boolean),
                         Column('link', String(1000)),
                         Column('picture', String(1000)),
                         Column('icon', String(1000)),
                         Column('likes', Integer),
                         Column('comments', Integer),
                         Column('created_date', DateTime),
                         Column('updated_date', DateTime),
                         Column('data', Text),
                         mysql_engine='InnoDB',
                         mysql_charset='utf8'
                         )


def update_schema(engine):
    metadata.create_all(engine)
