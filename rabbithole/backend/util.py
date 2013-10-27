import json


def dthandler(obj):
    return obj.isoformat() if 'isoformat' in dir(obj) else None


def dump_json(obj):
    return json.dumps(obj, indent=4, default=dthandler)
