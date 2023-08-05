# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

import trytond.tests.test_tryton
import unittest

from trytond.modules.purchase_line_twocolumn.tests.test_purchase import PurchaseLineTestCase
from trytond.modules.account_invoice_line_twocolumn.tests.test_invoice import InvoiceLineTestCase

__all__ = ['suite']


class PurchaseTestCase(\
            PurchaseLineTestCase,
    ):
    'Test two-columns module'
    module = 'purchase_line_twocolumn'

#end PurchaseTestCase


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(PurchaseTestCase))
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(InvoiceLineTestCase))
    return suite
