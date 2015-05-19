# -*- coding: utf-8 -*-

import ispformat.schema as _schema
from jsonschema import Draft4Validator, RefResolver, draft4_format_checker
from jsonschema.exceptions import RefResolutionError, SchemaError, ValidationError
import json
import os.path
from urlparse import urlsplit


class MyRefResolver(RefResolver):
    def resolve_remote(self, uri):
        # Prevent remote resolving
        raise RefResolutionError("LOL NOPE")


geojson_allowed_types=('Polygon', 'MultiPolygon')
def validate_geojson_type(d):
    """
    Make sure a geojson dict only contains allowed geometry types
    """
    type_=d.get('type')
    if type_ not in geojson_allowed_types:
        return False
    return True


def validate_geojson(geodict):
    """
    Convenience function to validate a geojson dict
    """
    _version = 0.1
    schema = _schema.load_schema(_version, 'geojson/geojson')
    v = Draft4Validator(
        schema,
        resolver=MyRefResolver.from_schema(schema, store=_schema.deps_for_version(_version)),
        format_checker=draft4_format_checker,
    )

    for err in v.iter_errors(geodict):
        return False

    if not validate_geojson_type(geodict):
        return False

    return True


def validate_isp(jdict):
    """
    Validate a json-object against the isp json-schema
    """
    if not 'version' in jdict:
        raise ValidationError(u'version is a required property')
    try:
        schema=_schema.versions[jdict['version']]
    except (AttributeError, TypeError, KeyError):
        raise ValidationError(u'version %r unsupported'%jdict['version'])

    v=Draft4Validator(
        schema,
        resolver=MyRefResolver.from_schema(schema, store=_schema.deps_for_version(jdict['version'])),
        format_checker=draft4_format_checker,
    )

    for err in v.iter_errors(jdict):
        yield err

    def is_valid_url(u):
        try:
            pu=urlsplit(u)
        except:
            return False
        if pu.scheme not in ('', 'http', 'https'):
            return False
        if not pu.netloc:
            return False
        return True

    if 'website' in jdict and not is_valid_url(jdict['website']):
        yield ValidationError(u'%r must be an absolute HTTP URL'%u'website',
                              instance=jdict[u'website'], schema=schema[u'properties'][u'website'],
                              path=[u'website'], schema_path=[u'properties', u'website', u'description'],
                              validator=u'validate_url', validator_value=jdict['website'])

    if 'logoURL' in jdict and not is_valid_url(jdict['logoURL']):
        yield ValidationError(u'%r must be an absolute HTTP URL'%u'logoURL',
                              instance=jdict[u'logoURL'], schema=schema[u'properties'][u'logoURL'],
                              path=[u'logoURL'], schema_path=[u'properties', u'logoURL', u'description'],
                              validator=u'validate_url', validator_value=jdict['logoURL'])

    sch=schema[u'properties'][u'otherWebsites'][u'patternProperties'][u'^.+$']
    for name, url in jdict.get('otherWebsites', {}).iteritems():
        if is_valid_url(url):
            continue
        yield ValidationError(u'%r must be an absolute HTTP URL'%name,
                              instance=url, schema=sch, path=[u'otherWebsite', name],
                              schema_path=[u'properties', u'otherWebsites', u'patternProperties', u'^.+$', 'description'],
                              validator=u'validate_url', validator_value=url)

    for i, ca in enumerate(jdict.get('coveredAreas', [])):
        area=ca.get('area')
        if area and validate_geojson_type(area):
            continue
        elif not area:
            continue

        yield ValidationError(
            u'GeoJSON can only contain the following types: %s'%repr(geojson_allowed_types),
            instance=ca, schema=schema[u'definitions'][u'coveredArea'][u'properties'][u'area'],
            path=['coveredAreas', i, 'area'],
            schema_path=[u'properties', u'coveredAreas', u'items', u'properties', u'area'],
            validator=u'validate_geojson_type', validator_value=ca
        )
