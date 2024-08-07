import unittest
from decimal import Decimal

from proteus import Model
from trytond.modules.account.tests.tools import (create_chart,
                                                 create_fiscalyear, create_tax,
                                                 get_accounts)
from trytond.modules.account_invoice.tests.tools import (
    create_payment_term, set_fiscalyear_invoice_sequences)
from trytond.modules.company.tests.tools import create_company, get_company
from trytond.tests.test_tryton import drop_db
from trytond.tests.tools import activate_modules
from trytond.model.modelstorage import DomainValidationError

class Test(unittest.TestCase):

    def setUp(self):
        drop_db()
        super().setUp()

    def tearDown(self):
        drop_db()
        super().tearDown()

    def test(self):

        # Install party_supplier
        config = activate_modules(['purchase', 'party_supplier'])

        # Create company
        _ = create_company()
        company = get_company()

        # Reload the context
        User = Model.get('res.user')
        config._context = User.get_preferences(True, config.context)

        # Create fiscal year
        fiscalyear = set_fiscalyear_invoice_sequences(
            create_fiscalyear(company))
        fiscalyear.click('create_period')

        # Create chart of accounts
        _ = create_chart(company)
        accounts = get_accounts(company)
        revenue = accounts['revenue']
        expense = accounts['expense']

        # Create tax
        tax = create_tax(Decimal('.10'))
        tax.save()

        # Create parties
        Party = Model.get('party.party')
        supplier = Party(name='Supplier')
        supplier.supplier = True
        supplier.save()
        customer = Party(name='Customer')
        customer.save()

        # Create account category
        ProductCategory = Model.get('product.category')
        account_category = ProductCategory(name="Account Category")
        account_category.accounting = True
        account_category.account_expense = expense
        account_category.account_revenue = revenue
        account_category.supplier_taxes.append(tax)
        account_category.save()

        # Create product
        ProductUom = Model.get('product.uom')
        unit, = ProductUom.find([('name', '=', 'Unit')])
        ProductTemplate = Model.get('product.template')
        Product = Model.get('product.product')
        product = Product()
        template = ProductTemplate()
        template.name = 'product'
        template.default_uom = unit
        template.type = 'goods'
        template.purchasable = True
        template.list_price = Decimal('10')
        template.cost_price_method = 'fixed'
        template.account_category = account_category
        template.save()
        product.template = template
        product.cost_price = Decimal('5')
        product.save()

        # Create payment term
        payment_term = create_payment_term()
        payment_term.save()

        # Create Product Supplier
        ProductSupplier = Model.get('purchase.product_supplier')
        ProductSupplierPrice = Model.get('purchase.product_supplier.price')
        product_supplier = ProductSupplier()
        product_supplier.product = template
        product_supplier.party = supplier
        product_supplier_price = ProductSupplierPrice()
        product_supplier.prices.append(product_supplier_price)
        product_supplier_price.sequence = 1
        product_supplier_price.quantity = Decimal(1.0)
        product_supplier_price.unit_price = Decimal(12)
        product_supplier.save()
        product_supplier = ProductSupplier()
        product_supplier.product = template
        product_supplier.party = customer
        product_supplier_price = ProductSupplierPrice()
        product_supplier.prices.append(product_supplier_price)
        product_supplier_price.sequence = 1
        product_supplier_price.quantity = Decimal(1.0)
        product_supplier_price.unit_price = Decimal(12)
        with self.assertRaises(DomainValidationError):
            product_supplier.save()

        # Purchase to Supplier
        Purchase = Model.get('purchase.purchase')
        PurchaseLine = Model.get('purchase.line')
        purchase = Purchase()
        purchase.party = supplier
        purchase.payment_term = payment_term
        purchase.invoice_method = 'order'
        purchase_line = PurchaseLine()
        purchase.lines.append(purchase_line)
        purchase_line.product = product
        purchase_line.quantity = 1.0
        purchase_line.unit_price = product.cost_price
        purchase.save()

        # Purchase to Customer
        Purchase = Model.get('purchase.purchase')
        PurchaseLine = Model.get('purchase.line')
        purchase = Purchase()
        purchase.party = customer
        purchase.payment_term = payment_term
        purchase.invoice_method = 'order'
        purchase_line = PurchaseLine()
        purchase.lines.append(purchase_line)
        purchase_line.product = product
        purchase_line.quantity = 1.0
        purchase_line.unit_price = product.cost_price
        with self.assertRaises(DomainValidationError):
            purchase.save()
