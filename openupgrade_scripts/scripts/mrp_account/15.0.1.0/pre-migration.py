# Copyright 2023 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from openupgradelib import openupgrade


def pre_create_mrp_production_analytic_account_id(env):
    """Pre-create the column for avoiding computation on module upgrade"""
    if openupgrade.column_exists(env.cr, "mrp_production", "analytic_account_id"):
        return
    # Add many2one field manually with SQL
    openupgrade.logged_query(
        env.cr,
        """
        ALTER TABLE mrp_production
        ADD COLUMN analytic_account_id integer
        """,
    )


@openupgrade.migrate()
def migrate(env, version):
    pre_create_mrp_production_analytic_account_id(env)
