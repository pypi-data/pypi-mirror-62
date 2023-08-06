# -*- coding: utf-8 -*-
"""Flask Taxonomies Marshmallow schemas."""
from invenio_records_rest.schemas import StrictKeysMixin
from invenio_records_rest.schemas.fields import SanitizedUnicode
from marshmallow import Schema, ValidationError, post_dump, pre_load
from marshmallow.fields import Integer, Nested
from sqlalchemy.orm.exc import NoResultFound

from flask_taxonomies.models import (
    Taxonomy,
    after_taxonomy_marshmallow,
    before_taxonomy_marshmallow,
)
from flask_taxonomies.utils import load_dump
from flask_taxonomies.views import url_to_path


class TaxonomyLinksSchemaV1(StrictKeysMixin):
    self = SanitizedUnicode(required=False)
    tree = SanitizedUnicode(required=False)
    parent = SanitizedUnicode(required=False)
    parent_tree = SanitizedUnicode(required=False)


class TaxonomyTitleSchemaV1(StrictKeysMixin):
    lang = SanitizedUnicode(required=False)
    value = SanitizedUnicode(required=False)


class TaxonomyAncestorSchemaV1(Schema):
    # strict keys not present as the ancestor has many other application-dependent props
    # do your own post-validation if required
    slug = SanitizedUnicode(required=False)
    level = Integer(required=False)


class TaxonomySchemaV1(StrictKeysMixin):
    """Taxonomy schema."""
    id = Integer(required=False)
    slug = SanitizedUnicode(required=False)
    path = SanitizedUnicode(required=False)
    title = Nested(TaxonomyTitleSchemaV1, many=True, required=False)
    tooltip = SanitizedUnicode(required=False)
    level = Integer(required=False)
    links = Nested(TaxonomyLinksSchemaV1, required=False)
    ref = SanitizedUnicode(required=False, attribute='$ref', **load_dump('$ref'))
    descendants_count = Integer(required=False, dump_only=True)
    ancestors = Nested(TaxonomyAncestorSchemaV1, many=True, required=False)

    @pre_load
    def convert_ref(self, in_data, **kwargs):
        ref = None
        if '$ref' in in_data:
            ref = in_data['$ref']
        elif 'links' in in_data:
            ref = (in_data['links'] or {}).get('self', None)
        if not ref:
            # No reference found - don't convert anything
            return in_data

        resp = before_taxonomy_marshmallow.send(self, ref=ref)
        for r in resp:
            if r[1]:
                if r[1] is True:
                    return {'$ref': ref}
                return r[1]

        path = url_to_path(ref)
        term = Taxonomy.get_taxonomy_term(path)
        if not term:
            raise ValidationError('Taxonomy $ref link is invalid: {}'.format(ref))  # noqa

        after_taxonomy_marshmallow.send(self, ref=ref, taxonomy_term=term)

        return {'$ref': ref}


__all__ = ('TaxonomySchemaV1',)
