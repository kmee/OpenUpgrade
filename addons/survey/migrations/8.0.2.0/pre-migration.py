# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright (C) 2014 Therp BV (<http://therp.nl>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.openupgrade import openupgrade


@openupgrade.migrate()
def migrate(cr, version):

    openupgrade.rename_tables(
        cr, [('survey', 'survey_survey'),
             ('survey_request', 'survey_user_input')])

    openupgrade.rename_columns(
        cr,
        {
            'survey_survey': [
                ('note', 'description'),
            ],
        })
    # we create and prefill this fields (with bogus data, they will be
    # recomputed during post-migrate in order to avoid errors when creating
    # not null constraints
    # cr.execute(
    #     '''alter table calendar_event
    #     add column start timestamp without time zone,
    #     add column stop timestamp without time zone''')
    # cr.execute(
    #     '''update calendar_event
    #     set start=start_datetime, stop=stop_datetime''')

    # cr.execute(
    #     '''insert into survey_user_input (id, create_uid, create_date, write_date, write_uid, survey_id, deadline, email) select id, create_uid, create_date, write_date, write_uid, survey_id, date_deadline, email from survey_request''' % (
    #         openupgrade.get_legacy_name('survey_id'),
    #     )
    # )
