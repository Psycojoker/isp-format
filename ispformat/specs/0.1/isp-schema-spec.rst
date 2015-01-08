==========
ISP format
==========
------------------------------------------------
Schema specification & implementation guidelines
------------------------------------------------

:Editor:
    Gu1 <gu1@cafai.fr>
:Authors:
    FFDN diyisp schema working group
:Revision:
    draft-1 (0.1)
:Date:
    December 2013


**Abstract:**
 The ISP format is a file format created and supported by the FDN Federation (FFDN) in order to help ISPs sharing its value to document and publish relevent informations regarding their status and progress in a common format.


.. contents:: **Table of Contents**



1. Introduction
===============

The ISP format is meant to allow an ISP to share relevant data and informations, such as its number of subscribers, the URL of its websites, chatrooms, etc... It was mostly created with small/diy/non-profit ISPs in mind, such as those in the FFDN.

1.1. Definitions
----------------
* The ISP format itself is based on the JSON data format. The JavaScript Object Notation (JSON) format and its basic types are defined in [RFC4627]_.
* The ISP format is mostly specified as a JSON Schema file, a JSON-based format for defining the structure of JSON data. JSON Schema is defined in the following IETF draft [json-schema-04]_.
* The ISP format relies on HTTP/1.1 for data transfer [RFC2616]_.
* The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC2119]_.


2. JSON Schema definition of the format
=======================================
.. include:: ../schema/0.1/isp.json
    :literal:


3. Properties and objects definition
====================================

3.1 progressStatus
==================
This field is an enum specifiying the progress status of the ISP.

Here is the definition of the values::

  1. Project considered
  2. Primary members found
  3. Legal structure being created
  4. Legal structure created
  5. Base tools created (bank account, first members)
  6. ISP partially functional (first subscribers, maybe in degraded mode)
  7. ISP fully working

3.2 coveredArea.area
====================
The "area" key of a coveredArea object is meant to represent a geographic area covered by the ISP. When present, it must contain a valid GeoJSON object, as defined in [geojson-spec]_.

As an additional restriction, it MUST only contain GeoJSON geometries of type Polygon or MultiPolygon.

3.3 coveredArea.technologies
============================
The "technologies" key of a coveredArea object MUST contain a list of technologies provided in that area.
Here is a more complete definition of the allowed values for this field:

ftth
  Fiber to the home.
fttb
  Fiber to the building. Fiber reaches the boundary of the building with the final connection to the individual living space being made via alternative means.
dsl
  Internet access provided over a phone line. This encompass ADSL, VDSL, SDSL and all the other xDSL technologies.
wifi
  Internet access provided over Wi-Fi.

This list is not exhaustive. Please contact us to add more.

4. Implementing the format
==========================

An ISP implementing the ISP format MUST serve the file as a valid HTTP ressource named isp.json placed at the root (/) of its HTTP server.

The ressource SHOULD be served on the ISP's main website (e.g. http://www.isp.org/isp.json). If that is not possible for some reason, the ISP MUST serve it on a subdomain (e.g. http://api.isp.org/isp.json).

The ressource SHOULD be served with a MIME type of "application/json".

The ressource SHOULD be reachable over HTTPS ([RFC2818]_).

The ressource MUST be served over HTTP version 1.1.


4.1 Caching considerations
--------------------------

The HTTP ressource SHOULD provide an expiration time, either through the Cache-Control header's max-age directive or the Expires header.

Please note that clients may choose to ignore the provided expiration time in cases where the value is deemed to low (e.g. a few seconds) or too high (e.g. a month).

Moreover, not all Cache-Control directives are guaranteed to be respected by clients, such as private, must-revalidate, no-cache, no-store.

A client may choose to cache the response for a low amount of time even in cases where a ressource explicitely disabled caching by providing a max-age of 0 or an Expires date set in the past.

Additionally, a ressource SHOULD implement conditional requests by providing an ETag or Last-Modified header and responding to the If-Modified-Since or If-None-Match request headers properly.


5. References
=============

.. [RFC4627] Crockford, D., "The application/json Media Type for JavaScript Object Notation (JSON)",
             `RFC 4627 <http://tools.ietf.org/html/rfc4627>`_, July 2006.
.. [json-schema-04] "JSON Schema: core definitions and terminology",
                    `draft-zyp-json-schema-04 <http://tools.ietf.org/html/draft-zyp-json-schema-04>`_, January 31, 2013.
.. [RFC2616] Fielding, R., Gettys, J. Mogul, J., Frystyk, H., Masinter, L., Leach P., and T. Berners-Lee,
             "Hypertext Transfer Protocol -- HTTP/1.1", `RFC 2616 <http://tools.ietf.org/html/rfc2616>`_, June 1999.
.. [RFC2119] Bradner, S., "Key words for use in RFCs to Indicate Requirement Levels", `RFC 2119 <http://tools.ietf.org/html/rfc2119>`_, March 1997.
.. [RFC2818] Rescorla, E., "HTTP Over TLS", `RFC 2818 <https://tools.ietf.org/html/rfc2818>`_, May 2000.
.. [geojson-spec] The `GeoJSON Format Specification 1.0 <http://geojson.org/geojson-spec.html>`_, 16 June 2008.


Appendix A. ISPs Examples
=========================
This is a minimal implementation example::

    {
        "name": "Oz Rural Fiber",
        "email": "dorothy@ozfiber.net",
        "memberCount": 8,
        "subscriberCount": 3,
        "coveredAreas": [
            {
                "name": "Munchkin Country",
                "technologies": ["ftth"],
            },
            {
                "name": "Yellow brick road",
                "technologies": ["wifi"],
            }
        ],
        "version": 0.1
    }

Here is another, more complete example::

    {
        "shortname": "MDN",
        "name": "Middle-earth Data Network",
        "description": "Non-profit ISP located in the Middle-earth",
        "logoURL": "https://www.mdn.net/logo.png",
        "website": "https://www.mdn.net/",
        "otherWebsites": {
            "wiki": "http://wiki.mdn.net"
        },
        "email": "contact@mdn.net",
        "mainMailingList": "public@lists.mdn.net",
        "creationDate": "1892-01-03",
        "progressStatus": 7,
        "memberCount": 600,
        "subscriberCount": 86,
        "chatrooms": [
            "irc://irc.freenode.net/#mdn",
            "xmpp:members@chat.mdn.net?join"
        ],
        "registeredOffice": {
            "extended-addess": "third hobbit-hole on the left",
            "street-address": "1 Main Street",
            "locality": "Hobbiton",
            "region": "Westfarthing",
            "postal-code": "??",
            "country-name": "The Shire"
        },
        "coordinates": {
            "latitude": 3.14159265,
            "longitude": 1.57079632
        },
        "coveredAreas": [
            {
                "name": "Mordor",
                "technologies": ["wifi"],
                "area": {
                    "type": "Polygon",
                    "coordinates": [[
                        [ -35.5078125, 18.646245142670608 ],
                        [ -35.5078125, 56.559482483762245 ],
                        [ 63.984375, 56.559482483762245 ],
                        [ 63.984375, 18.646245142670608 ],
                        [ -35.5078125, 18.646245142670608 ]
                    ]]
                }
            },
            {
                "name": "The Shire",
                "technologies": ["dsl"]
            }
        ],
        "version": 0.1
    }


Appendix B. Where to find GeoJSON for covered areas
====================================================

For France, you can use the GeoJSON files at https://github.com/ymarcon/gadm/tree/master/FR_adm/ (where adm1 is for region ; 2 for départment ; 4 for city). Find the JSON block corresponding to your ISP's covered area and then, copy and paste only the :code:`{ "type": "Polygon", [ ... ] }` block. Beware: only one :code:`}` at the end !

For the rest of the world, you can try to use nominatim: http://nominatim.openstreetmap.org/search.php?q=QUERY&polygon_geojson=1&format=json (where QUERY is state/city name) using the same method (only copy/paste the "MultiPolygon" block).

Please note that the GeoJSON produced by nominatim might not be completely supported by some GIS like Spatialite which is used by the reference implementation. This could cause errors like "Unable to store GeoJSON in database".


Revision History
============================

Version 0.1.2 (2014-07-24)
    Added "fttb" as a possible technology (AG DSN).
    Added section 3.3 with complete definitions for each allowed value for the ``coveredArea.technologies`` field.

Version 0.1.1 (2014-07-24)
    Added Appendix B. which contain some pointers on where to find GeoJSON for covered areas (lg).

Version 0.1 (2013-12-23)
    Initial relase of this document.
