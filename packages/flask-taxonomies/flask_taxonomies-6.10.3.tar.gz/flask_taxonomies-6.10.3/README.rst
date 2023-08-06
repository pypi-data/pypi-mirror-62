===============================
Flask Taxonomies
===============================

.. image:: https://img.shields.io/github/license/oarepo/flask-taxonomies.svg
        :target: https://github.com/oarepo/flask-taxonomies/blob/master/LICENSE

.. image:: https://img.shields.io/travis/oarepo/flask-taxonomies.svg
        :target: https://travis-ci.org/oarepo/flask-taxonomies

.. image:: https://img.shields.io/coveralls/oarepo/flask-taxonomies.svg
        :target: https://coveralls.io/r/oarepo/flask-taxonomies

.. image:: https://img.shields.io/pypi/v/flask-taxonomies.svg
        :target: https://pypi.org/pypi/flask-taxonomies


TaxonomyTerm trees REST API for Invenio Applications


Quickstart
----------

Run the following commands to bootstrap your environment ::

    git clone https://github.com/oarepo/flask_taxonomies
    cd flask_taxonomies
    pip install -e .

Once you have installed your DBMS, run the following to create your app's
database tables and perform the initial migration ::

    invenio db init create
    invenio alembic upgrade heads
    invenio run

Python Usage
------------

    >>> from flask_taxonomies.models import Taxonomy, TaxonomyTerm
    >>> # To create Taxonomy:
    >>> t = Taxonomy.create_taxonomy(code='taxcode')
    >>> # To create TaxonomyTerm
    >>> term = t.create_term(slug='slug', extra_data={})
    >>> another = t.create_term(slug='another', extra_data={})
    >>> # To create TaxonomyTerm within another
    >>> term2 = term.create_term(slug='slug1', extra_data={})
    >>> # To get taxonomy by code
    >>> t = Taxonomy.get('taxcode')
    >>> # To list taxonomy top-level terms
    >>> terms = list(t.roots)
    >>> # To get term from taxonomy
    >>> term = t.get_term('slug')
    >>> # To get term and taxonomy from path
    >>> t, term = Taxonomy.find_taxonomy_and_term('/taxcode/taxterm')
    >>> # To move term to a different place
    >>> term.move(another, MovePosition.INSIDE) # moves term to '/taxcode/another/slug/'
    >>> # To delete term and its descendants
    >>> term.delete()
    >>> # To update Taxonomy/TaxonomyTerm
    >>> t.update(extra_data={'updated': true})
    >>> # To delete Taxonomy
    >>> db.session.delete(t)

REST API Usage
-----

To list available taxonomies ::

    curl -X GET http://localhost:5000/taxonomies/
    > [{'code': ..., 'extra_data': ...}, ...]

To create taxonomy ::

    curl -X POST \
      http://localhost:5000/taxonomies/ \
      -d '{"code": "...", "extra_data": "{...}"}'

To create a term in taxonomy ::

    curl -X POST \
      http://localhost:5000/taxonomies/<taxonomy-code>/<taxonomy-parent-term-path>/ \
      -d '{"title": {"en": ..., ...}, "slug": "..."}

To list top-level terms in a taxonomy ::

    curl -X GET http://localhost:5000/taxonomies/<taxonomy-code>/
    > [{'slug': ..., ...}, {'slug': ..., ...}, ...]

To get Taxonomy Term details ::

    curl -X GET http://localhost:5000/taxonomies/<taxonomy-code>/<taxonomy-term-path>/
    > {'slug': ..., 'title': ..., 'extra_data', ..., 'children': [...], ...}

Delete taxonomy (including all its terms) ::

    curl -X DELETE \
      http://localhost:5000/taxonomies/<taxonomy-code>

Delete taxonomy term (including all its childrens) ::

    curl -X DELETE \
      http://localhost:5000/taxonomies/<taxonomy-code>/<taxonomy-term-path>/

Update taxonomy extra data ::

    curl -X PATCH \
        http://localhost:5000/taxonomies/<taxonomy-code>/ \
        -d '{"extra_data":"{...}"}'

Update taxonomy term data ::

    curl -X PATCH \
        http://localhost:5000/taxonomies/<taxonomy-code>/<taxonomy-term-path>/ \
        -d '{"title":"{...}", "extra_data":"{...}"}'

Move taxonomy term (or whole term subtree) inside, before or after another term ::

    curl -X POST \
        http://localhost:5000/taxonomies/<taxonomy-code>/<taxonomy-term-path>/ \
        -H 'Destination: http://localhost:5000/taxonomies/<taxonomy-or-term-path>' \
        -H 'Destination-Order: inside|before|after' \
        -H 'Content-Type: application/vnd.move'

Note: in case of taxonomy path, only "inside" is allowed.