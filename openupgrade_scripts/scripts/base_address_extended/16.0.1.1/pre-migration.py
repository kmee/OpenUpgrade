# Copyright 2025 Dixmit
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

import re

from openupgradelib import openupgrade

_add_fields = [
    (
        "street_name",
        "res.partner",
        "res_partner",
        "char",
        None,
        "base_address_extended",
        None,
    ),
    (
        "street_number",
        "res.partner",
        "res_partner",
        "char",
        None,
        "base_address_extended",
        None,
    ),
    (
        "street_number2",
        "res.partner",
        "res_partner",
        "char",
        None,
        "base_address_extended",
        None,
    ),
]


def parse_street(street):
    """Parse street field into components."""
    if not street:
        return None, None, None

    # Regex para extrair nome da rua, número e complemento
    pattern = r"^(.*?)(?:\s([0-9][0-9\S]*))?(?: - (.+))?$"
    match = re.match(pattern, street)

    if not match:
        return street.strip(), None, None

    street_name = match.group(1)
    street_number = match.group(2)
    street_number2 = match.group(3)

    return (
        street_name.strip() if street_name else None,
        street_number.strip() if street_number else None,
        street_number2.strip() if street_number2 else None,
    )


@openupgrade.migrate()
def migrate(env, _version):
    # Primeiro adiciona os campos
    openupgrade.add_fields(env, _add_fields)

    # Busca todos os parceiros com endereço usando SQL
    env.cr.execute("SELECT id, street FROM res_partner WHERE street IS NOT NULL")
    partners = env.cr.fetchall()

    for partner_id, street in partners:
        street_name, street_number, street_number2 = parse_street(street)

        # Prepara os valores e parâmetros para o UPDATE
        update_fields = []
        params = []

        if street_name:
            update_fields.append("street_name = %s")
            params.append(street_name)
        if street_number:
            update_fields.append("street_number = %s")
            params.append(street_number)
        if street_number2:
            update_fields.append("street_number2 = %s")
            params.append(street_number2)

        if update_fields:
            params.append(partner_id)
            query = """
                UPDATE res_partner
                SET {}
                WHERE id = %s
            """.format(", ".join(update_fields))

            openupgrade.logged_query(env.cr, query, tuple(params))
