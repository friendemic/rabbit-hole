from sqlalchemy.sql.expression import select
from ..schema import content_facebook

columns = content_facebook.c
serialize_columns = [
    columns.id,
    columns.fb_account,
    columns.message,
    columns.is_self,
    columns.link,
    columns.picture,
    columns.icon,
    columns.comments,
    columns.created_date,
    columns.updated_date
]

def insert_update_items(conn, items):
    """Insert or update all the given items

    Args:
        items: array of dictionaries representing the items
    """
    insert_query = content_facebook.insert()
    update_query = content_facebook.update().where('id=:b_id')

    for item in items:
        if item_exists(conn, item):
            item['b_id'] = item.get('id')
            conn.execute(update_query, **item)
        else:
            conn.execute(insert_query, **item)


def item_exists(conn, item):
    """Determine whether the given feed item exists in the database, based
    on its 'id' element

    Args:
        conn: Open connection to the database
        item: dict-like representing the item
    """
    select_query = select(columns=[content_facebook.c.id]).where('id=:id')
    result = conn.execute(select_query, id=item.get('id'))
    return result.fetchone() is not None

def filter_items(conn, from_date=None, end_date=None, fb_accounts=None):
    """Query the DB for feed items.

    Args:
        conn: Open connection to the database
        from_date: Earliest created_date for returned feed items
        end_date: Latest created_date for returned feed items
        fb_accounts: array of facebook account IDs to filter query by
    Returns:
        Array of dictionaries representing rows returned
    """

    select_query = select(columns=serialize_columns)

    if(from_date is not None):
        print "adding from date query"
        select_query = select_query.where(content_facebook.c.created_date > from_date);

    if(end_date is not None):
        print "adding end_date date query"
        select_query = select_query.where(content_facebook.c.created_date < end_date);

    if(fb_accounts is not None):
        select_query = select_query.where(content_facebook.c.fb_account.in_(fb_accounts))

    print "running query %s" % str(select_query)

    return [dict(d.items()) for d in conn.execute(select_query).fetchall()]

def dump_table(conn):
    select_query = content_facebook.select()
    return [d.items() for d in conn.execute(select_query).fetchall()]

