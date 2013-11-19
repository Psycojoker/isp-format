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
    October 2013


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

3.1 coveredArea.area
=====================
The "area" key of a coveredArea object, is meant to represent a geographic area covered by the ISP. When present, it must contain a valid GeoJSON object, as defined in [geojson-spec]_.

As an additional restriction, it MUST only contain GeoJSON geometries of type Polygon or MultiPolygon.


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
TODO
