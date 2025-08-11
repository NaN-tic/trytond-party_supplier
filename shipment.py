# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.pool import PoolMeta


class ShipmentIn(metaclass=PoolMeta):
    __name__ = 'stock.shipment.in'

    @classmethod
    def __setup__(cls):
        super().__setup__()

        supplier_domain = ('supplier', '=', True)
        if cls.supplier.domain:
            cls.supplier.domain += [supplier_domain]
        else:
            cls.supplier.domain = [supplier_domain]
