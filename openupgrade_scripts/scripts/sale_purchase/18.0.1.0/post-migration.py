from openupgradelib import openupgrade, openupgrade_180


def convert_company_dependent(env):
    openupgrade_180.convert_company_dependent(
        env, "product.template", "service_to_purchase"
    )


@openupgrade.migrate()
def migrate(env, version):
    convert_company_dependent(env)
