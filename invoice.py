# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.pyson import If, Eval

__all__ = ['Invoice']


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    @classmethod
    def __setup__(cls):
        super(Invoice, cls).__setup__()
        supplier_domain = [If(Eval('type') == 'in',
                ('supplier', '=', True),
                (),
                )]
        cls.party.domain.append(supplier_domain)
        cls.party.depends.append('type')
