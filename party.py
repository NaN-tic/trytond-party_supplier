# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import If, Eval
from trytond.modules.party.party import STATES, DEPENDS

__all__ = ['Party', 'Invoice', 'Purchase']
__metaclass__ = PoolMeta


class Party:
    __name__ = 'party.party'

    supplier = fields.Boolean('Supplier', states=STATES, depends=DEPENDS)


class Invoice:
    __name__ = 'account.invoice'

    @classmethod
    def __setup__(cls):
        super(Invoice, cls).__setup__()
        supplier_domain = [If(Eval('type').in_(['in_invoice',
                        'in_credit_note']),
                ('supplier', '=', True),
                (),
                )]
        cls.party.domain.append(supplier_domain)
        cls.party.depends.append('type')


class Purchase:
    __name__ = 'purchase.purchase'

    @classmethod
    def __setup__(cls):
        super(Purchase, cls).__setup__()
        supplier_domain = [('supplier', '=', True)]
        if supplier_domain not in cls.party.domain:
            cls.party.domain.append(supplier_domain)
