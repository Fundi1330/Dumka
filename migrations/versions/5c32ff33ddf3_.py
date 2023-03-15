"""empty message

Revision ID: 5c32ff33ddf3
Revises: 
Create Date: 2023-03-15 13:23:49.559541

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5c32ff33ddf3'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Community',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('Community', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_Community_name'), ['name'], unique=False)

    op.create_table('Post',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('theme', sa.String(), nullable=True),
    sa.Column('tag', sa.String(), nullable=True),
    sa.Column('author', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('Post', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_Post_author'), ['author'], unique=False)
        batch_op.create_index(batch_op.f('ix_Post_tag'), ['tag'], unique=False)

    op.create_table('User',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('username', sa.String(length=120), nullable=True),
    sa.Column('email', sa.String(length=60), nullable=True),
    sa.Column('password_hash', sa.String(length=120), nullable=True),
    sa.Column('about_me', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_User_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_User_name'), ['name'], unique=False)
        batch_op.create_index(batch_op.f('ix_User_username'), ['username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('User', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_User_username'))
        batch_op.drop_index(batch_op.f('ix_User_name'))
        batch_op.drop_index(batch_op.f('ix_User_email'))

    op.drop_table('User')
    with op.batch_alter_table('Post', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Post_tag'))
        batch_op.drop_index(batch_op.f('ix_Post_author'))

    op.drop_table('Post')
    with op.batch_alter_table('Community', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_Community_name'))

    op.drop_table('Community')
    # ### end Alembic commands ###
