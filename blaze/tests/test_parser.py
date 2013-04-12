import unittest

from blaze.datashape import *
from blaze.datashape.parser import parse
from blaze.datashape.record import RecordDecl, derived
from blaze.datashape.coretypes import _reduce

tests = []

#------------------------------------------------------------------------

class TestDatashapeParser(unittest.TestCase):

    def test_simple_parse(self):
        x = parse('2, 3, int32')
        y = parse('300 , 400, {x: int64; y: int32}')

        self.assertEqual(type(x) , DataShape)
        self.assertEqual(type(y) , DataShape)

        self.assertEqual(type(y[0]) , Fixed)
        self.assertEqual(type(y[1]) , Fixed)
        self.assertEqual(type(y[2]) , Record)

        rec = y[2]

        self.assertEqual(rec['x'] , int64)
        self.assertEqual(rec['y'] , int32)

    def test_compound_record1(self):
        p = parse('6, {x:int32; y:float64; z:string}')

        self.assertEqual(type(p[0]) , Fixed)
        self.assertEqual(type(p[1]) , Record)

    def test_compound_record2(self):
        p = parse('{ a: { x: int; y: int }; b: {w: int; u: int } }')

        self.assertEqual(type(p) , Record)

    def test_free_variables(self):
        p = parse('N, M, 800, 600, int32')

        self.assertEqual(type(p[0]) , TypeVar)
        self.assertEqual(type(p[1]) , TypeVar)
        self.assertEqual(type(p[2]) , Fixed)
        self.assertEqual(type(p[3]) , Fixed)
        self.assertEqual(type(p[4]) , CType)

    def test_parse_equality(self):
        x = parse('800, 600, int64')
        y = parse('800, 600, int64')

        self.assertTrue(x._equal(y) )

    def test_parse_vars(self):
        x = parse('Range(1,2), int32')

        self.assertEqual(x[0].lower , 1)
        self.assertEqual(x[0].upper , 2)

    def test_parse_either(self):
        x = parse('Either(int64, float64)')

        self.assertEqual(type(x) , Either)
        self.assertEqual(x.a , int64)
        self.assertEqual(x.b , float64)

    def test_custom_record(self):

        class Stock1(RecordDecl):
            name   = string
            open   = float_
            close  = float_
            max    = int64
            min    = int64
            volume = float_

            @derived('int64')
            def mid(self):
                return (self.min + self.max)/2

    def test_fields_with_reserved_names(self):
        # Should be able to name a field 'type', 'int64'
        # or any other word otherwise reserved in the
        # datashape language
        x = parse("""{
                type: bool;
                blob: bool;
                bool: bool;
                int: int32;
                float: float32;
                double: float64;
                int8: int8;
                int16: int16;
                int32: int32;
                int64: int64;
                uint8: uint8;
                uint16: uint16;
                uint32: uint32;
                uint64: uint64;
                float16: float32;
                float32: float32;
                float64: float64;
                float128: float64;
                complex64: float32;
                cfloat32: float32;
                complex128: float64;
                cfloat64: float64;
                string: string;
                object: string;
                datetime: string;
                datetime64: string;
                timedelta: string;
                timedelta64: string;
                json: string;
            }""")

    def test_kiva_datashape(self):
        # A slightly more complicated datashape which should parse
        x = parse("""5, VarDim, {
              id: int64;
              name: string;
              description: {
                languages: VarDim, string(2);
                texts: json;
              };
              status: string;
              funded_amount: float64;
              basket_amount: json;
              paid_amount: json;
              image: {
                id: int64;
                template_id: int64;
              };
              video: json;
              activity: string;
              sector: string;
              use: string;
              delinquent: bool;
              location: {
                country_code: string(2);
                country: string;
                town: json;
                geo: {
                  level: string;
                  pairs: string;
                  type: string;
                };
              };
              partner_id: int64;
              posted_date: json;
              planned_expiration_date: json;
              loan_amount: float64;
              currency_exchange_loss_amount: json;
              borrowers: VarDim, {
                first_name: string;
                last_name: string;
                gender: string(1);
                pictured: bool;
              };
              terms: {
                disbursal_date: json;
                disbursal_currency: string(3,'A');
                disbursal_amount: float64;
                loan_amount: float64;
                local_payments: VarDim, {
                  due_date: json;
                  amount: float64;
                };
                scheduled_payments: VarDim, {
                  due_date: json;
                  amount: float64;
                };
                loss_liability: {
                  nonpayment: string;
                  currency_exchange: string;
                  currency_exchange_coverage_rate: json;
                };
              };
              payments: VarDim, {
                amount: float64;
                local_amount: float64;
                processed_date: json;
                settlement_date: json;
                rounded_local_amount: float64;
                currency_exchange_loss_amount: float64;
                payment_id: int64;
                comment: json;
              };
              funded_date: json;
              paid_date: json;
              journal_totals: {
                entries: int64;
                bulkEntries: int64;
              };
            }
        """)


tests.append(TestDatashapeParser)

#------------------------------------------------------------------------

def run(verbosity=1, repeat=1):
    suite = unittest.TestSuite()
    for cls in tests:
        for _ in range(repeat):
            suite.addTest(unittest.makeSuite(cls))

    runner = unittest.TextTestRunner(verbosity=verbosity)
    return runner.run(suite)

if __name__ == '__main__':
    run()
