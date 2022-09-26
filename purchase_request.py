# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.pool import PoolMeta


class CreatePurchaseAskParty(metaclass=PoolMeta):
    __name__ = 'purchase.request.create_purchase.ask_party'

    @classmethod
    def __setup__(cls):
        super(CreatePurchaseAskParty, cls).__setup__()

        supplier_domain = ('supplier', '=', True)
        if cls.party.domain:
            cls.party.domain += [supplier_domain]
        else:
            cls.party.domain = [supplier_domain]
