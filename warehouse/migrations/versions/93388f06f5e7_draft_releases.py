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
Draft Releases

Revision ID: 93388f06f5e7
Revises: 80018e46c5a4
Create Date: 2020-09-29 18:23:35.798571
"""

import sqlalchemy as sa

from alembic import op

revision = "93388f06f5e7"
down_revision = "80018e46c5a4"

# Note: It is VERY important to ensure that a migration does not lock for a
#       long period of time and to ensure that each individual migration does
#       not break compatibility with the *previous* version of the code base.
#       This is because the migrations will be ran automatically as part of the
#       deployment process, but while the previous version of the code is still
#       up and running. Thus backwards incompatible changes must be broken up
#       over multiple migrations inside of multiple pull requests in order to
#       phase them in over multiple deploys.


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("releases", sa.Column("project_name", sa.Text(), nullable=True))
    op.add_column("releases", sa.Column("published", sa.DateTime(), nullable=True))
    # ### end Alembic commands ###
    # Fill the project_name and published columns
    op.execute(
        """
        UPDATE releases AS target SET published = (
        SELECT created
        FROM releases AS source WHERE source.id = target.id
        );
    """
    )
    op.execute(
        """
        UPDATE releases AS r SET project_name = (
            SELECT name
            FROM projects AS p WHERE p.id = r.project_id
        )
    """
    )
    # Create the hashing database function for our draft identifiers
    op.execute(
        """
        CREATE FUNCTION make_draft_hash(project_name text, version text)
        returns text as $$
                SELECT  md5(project_name || version)
            $$
            LANGUAGE SQL
            IMMUTABLE
            RETURNS NULL ON NULL INPUT;
    """
    )


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("releases", "published")
    op.drop_column("releases", "project_name")
    # ### end Alembic commands ###
    op.execute("DROP FUNCTION make_draft_hash")
