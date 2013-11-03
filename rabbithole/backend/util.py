import json
import dateutil.parser

def date_format(obj):
    if 'isoformat' in dir(obj):
        return obj.isoformat()

    try:
        return dateutil.parser.parse(obj).isoformat()
    except:
        return None


def dump_json(obj):
    return json.dumps(obj, indent=4, default=date_format)


def denull_dict(obj):
    return {k:obj[k] for k in obj.keys() if obj[k] is not None}

