import json
import os

path = os.path.dirname(__file__)

def load_schema(version, name='isp'):
    """
    Load a schema from ./``version``/``name``.json and return it.

    """
    schemapath = os.path.join(path, str(version), '%s.json'%(name,))
    with open(schemapath) as f:
        return json.load(f)


versions = {
    0.1: load_schema('0.1')
}

latest = versions[0.1]

def deps_for_version(version):
    return {
        'http://json-schema.org/geo': load_schema(version, 'geo'),
        'http://json-schema.org/address': load_schema(version, 'address'),
        'http://json-schema.org/geojson/geojson.json#': load_schema(version, 'geojson/geojson'),
        'http://json-schema.org/geojson/geometry.json#': load_schema(version, 'geojson/geometry'),
        'http://json-schema.org/geojson/bbox.json#': load_schema(version, 'geojson/bbox'),
        'http://json-schema.org/geojson/crs.json#': load_schema(version, 'geojson/crs'),
    }



__all__ = ['path', 'versions', 'latest']
