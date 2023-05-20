# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
add organization application model

Revision ID: 6e669fe86792
Revises: c5f718cb98ac
Create Date: 2023-05-20 19:35:17.214081
"""

import sqlalchemy as sa
import sqlalchemy_utils.types.url

from alembic import op
from sqlalchemy.dialects import postgresql

revision = "6e669fe86792"
down_revision = "c5f718cb98ac"


def upgrade():
    op.create_table(
        "organization_applications",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            server_default=sa.text("gen_random_uuid()"),
            nullable=False,
        ),
        sa.Column("name", sa.Text(), nullable=False),
        sa.Column("display_name", sa.Text(), nullable=False),
        sa.Column(
            "orgtype",
            sa.Enum("Community", "Company", name="organizationtype"),
            nullable=False,
        ),
        sa.Column("link_url", sqlalchemy_utils.types.url.URLType(), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column(
            "submitted", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.CheckConstraint(
            "link_url ~* '^https?://.*'::text",
            name="organization_applications_valid_link_url",
        ),
        sa.CheckConstraint(
            "name ~* '^([A-Z0-9]|[A-Z0-9][A-Z0-9._-]*[A-Z0-9])$'::text",
            name="organization_applications_valid_name",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_organization_applications_submitted"),
        "organization_applications",
        ["submitted"],
        unique=False,
    )


def downgrade():
    op.drop_index(
        op.f("ix_organization_applications_submitted"),
        table_name="organization_applications",
    )
    op.drop_table("organization_applications")
