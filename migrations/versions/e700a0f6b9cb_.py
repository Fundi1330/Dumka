"""empty message

Revision ID: e700a0f6b9cb
Revises: 857d15eba364
Create Date: 2023-03-26 19:40:25.543663

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e700a0f6b9cb'
down_revision = '857d15eba364'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('Community', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.String(length=300), nullable=True))
        batch_op.add_column(sa.Column('themes', postgresql.ARRAY(sa.String()), nullable=True))
        batch_op.create_index(batch_op.f('ix_Community_description'), ['description'], unique=False)

    with op.batch_alter_table('Post', schema=None) as batch_op:
        batch_op.alter_column('author',
               existing_type=sa.VARCHAR(),
               nullable=False)
        batch_op.drop_index('ix_Post_author')
        batch_op.drop_index('ix_Post_text')
        batch_op.drop_index('ix_Post_theme')
        batch_op.create_foreign_key(None, 'User', ['author'], ['username'])

    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.add_column(sa.Column('avatar', sa.String(), nullable=True))
        batch_op.drop_index('ix_User_interests')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.create_index('ix_User_interests', ['interests'], unique=False)
        batch_op.drop_column('avatar')

    with op.batch_alter_table('Post', schema=None) as batch_op:
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_index('ix_Post_theme', ['theme'], unique=False)
        batch_op.create_index('ix_Post_text', ['text'], unique=False)
        batch_op.create_index('ix_Post_author', ['author'], unique=False)
        batch_op.alter_column('author',
               existing_type=sa.VARCHAR(),
               nullable=True)

    with op.batch_alter_table('Community', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Community_description'))
        batch_op.drop_column('themes')
        batch_op.drop_column('description')

    # ### end Alembic commands ###