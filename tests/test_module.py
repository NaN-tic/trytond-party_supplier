
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.modules.company.tests import CompanyTestMixin
from trytond.tests.test_tryton import ModuleTestCase


class PartySupplierTestCase(CompanyTestMixin, ModuleTestCase):
    'Test PartySupplier module'
    module = 'party_supplier'


del ModuleTestCase
