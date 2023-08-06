#
# This file is part of Invenio.
# Copyright (C) 2016-2018 CERN.
#
# Invenio is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.

"""Create flask-taxonomies branch."""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'e5848504dc5f'
down_revision = None
branch_labels = ('flask_taxonomies',)
depends_on = None


def upgrade():
    """Upgrade database."""
    pass


def downgrade():
    """Downgrade database."""
    pass
