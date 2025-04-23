# Copyright 2021 ForgeFlow S.L.  <https://www.forgeflow.com>
# Copyright 2021 Tecnativa - Pedro M. Baeza
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


def add_crm_lead_fields(env):
    # Add numeric fields manually
    if not openupgrade.column_exists(env.cr, "crm_lead", "recurring_revenue_monthly"):
        openupgrade.logged_query(
            env.cr,
            """
            ALTER TABLE crm_lead
            ADD COLUMN recurring_revenue_monthly numeric
            """,
        )
    if not openupgrade.column_exists(
        env.cr, "crm_lead", "recurring_revenue_monthly_prorated"
    ):
        openupgrade.logged_query(
            env.cr,
            """
            ALTER TABLE crm_lead
            ADD COLUMN recurring_revenue_monthly_prorated numeric
            """,
        )


def rename_crm_tables(env):
    # Check if old table exists before renaming
    env.cr.execute(
        """
        SELECT EXISTS (
            SELECT FROM information_schema.tables
            WHERE table_name = 'crm_lead_tag_rel'
        )
        """
    )
    if env.cr.fetchone()[0]:
        openupgrade.rename_tables(env.cr, [("crm_lead_tag_rel", "crm_tag_rel")])


@openupgrade.migrate()
def migrate(env, version):
    add_crm_lead_fields(env)

    # Only rename fields if target column doesn't exist
    if not openupgrade.column_exists(env.cr, "crm_lead", "prorated_revenue"):
        openupgrade.rename_fields(
            env,
            [
                ("crm.lead", "crm_lead", "expected_revenue", "prorated_revenue"),
            ],
        )
    if not openupgrade.column_exists(env.cr, "crm_lead", "expected_revenue"):
        openupgrade.rename_fields(
            env,
            [
                ("crm.lead", "crm_lead", "planned_revenue", "expected_revenue"),
            ],
        )

    rename_crm_tables(env)
    openupgrade.remove_tables_fks(env.cr, ["crm_partner_binding"])
    # Disappeared constraint
    openupgrade.logged_query(
        env.cr,
        """ALTER TABLE crm_lead
           DROP CONSTRAINT IF EXISTS crm_lead_tag_name_uniq""",
    )
    openupgrade.delete_records_safely_by_xml_id(
        env, ["crm.constraint_crm_lead_tag_name_uniq"]
    )
