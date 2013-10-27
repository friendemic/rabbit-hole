facebook = {
    'access_token': '',

    'account_number': '',

    'feed_fields': {
        'id': None,
        'fb_account': {
            'descent': ['from', 'id']
        },
        'message': None,
        'is_self': {
            'action': 'is_self',
        },
        'link': None,
        'picture': None,
        'icon': None,
        'likes': {
            'action': 'len'
        },
        'comments': {
            'action': 'len'
        },
        'data': {
            'action': 'full_item_text'
        },
        'created_date': {
            'field_name': 'created_time',
            'type': 'datetime'
        },
        'updated_date': {
            'field_name': 'updated_time',
            'type': 'datetime'
        },
    }
}

db = {
    'type': 'mysql',
    'mysql': {
        'host': 'localhost',
        'user': 'root',
        'pass': '',
        'db_name': 'rabbithole_backend',
    },
    'echo': False
}
