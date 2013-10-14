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


def validate_isp(jdict):
    """
    Validate a json-object against the isp json-schema
    """
    if not 'version' in jdict:
        raise ValidationError(u'version is a required property')
    try:
        schema=_schema.versions.get(jdict['version'])
    except (AttributeError, TypeError):
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


