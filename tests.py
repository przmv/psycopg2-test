"""Test various PostgreSQL types handling with psycopg2"""

import collections
import psycopg2
import psycopg2.extras
import unittest

class TestReturnValues(unittest.TestCase):
    """Return values test case"""

    def setUp(self):
        self.conn = psycopg2.connect(
            database='postgres',
            user='postgres',
            host='db',
            port=5432)
        self.cur = self.conn.cursor()

    def tearDown(self):
        self.cur.close()
        self.conn.close()

    def test_composite(self):
        """Test composite types"""
        self.cur.execute(
            """
            CREATE TYPE grade_distrib AS (
                grade character,
                distrib double precision
            );
            """
        )
        psycopg2.extras.register_composite('grade_distrib', self.cur)
        self.cur.execute(
            """
            SELECT '("A", 0.25)'::grade_distrib;
            """
        )
        result = self.cur.fetchone()[0]
        grade_distrib = collections.namedtuple('grade_distrib',
                                               ['grade', 'distrib'])
        expect = grade_distrib(grade='A', distrib=0.25)
        self.assertEqual(result, expect)

    def test_array(self):
        """Test array"""
        self.cur.execute(
            """
            SELECT
                ARRAY['foo', 'bar', 'baz'],
                ARRAY[[1,2,3],[4,5,6],[7,8,9]],
                ARRAY[true,false,true];
            """
        )
        result = self.cur.fetchone()
        expect = (['foo', 'bar', 'baz'],
                  [[1, 2, 3],
                   [4, 5, 6],
                   [7, 8, 9]],
                  [True, False, True])
        self.assertEqual(result, expect)

    def test_composite_array(self):
        """Test array of composite"""
        self.cur.execute(
            """
            CREATE TYPE grade_distrib AS (
                grade character,
                distrib double precision
            );
            """
        )
        psycopg2.extras.register_composite('grade_distrib', self.cur)
        self.cur.execute(
            """
            SELECT ARRAY[
                '("A", 0.12)'::grade_distrib,
                '("B", 0.23)'::grade_distrib,
                '("C", 0.34)'::grade_distrib,
                '("D", 0.45)'::grade_distrib
            ];
            """
        )
        result = self.cur.fetchone()[0]
        grade_distrib = collections.namedtuple('grade_distrib',
                                               ['grade', 'distrib'])
        expect = [grade_distrib(grade='A', distrib=0.12),
                  grade_distrib(grade='B', distrib=0.23),
                  grade_distrib(grade='C', distrib=0.34),
                  grade_distrib(grade='D', distrib=0.45)]
        self.assertEqual(result, expect)

    def test_json(self):
        """Test JSON"""
        self.cur.execute(
            """
            SELECT '{
                "foo": "bar",
                "bar": 42,
                "baz": false,
                "quuix": null,
                "foo": 3.14,
                "fruit": "apple"
            }'::json;
            """
        )
        result = self.cur.fetchone()[0]
        expect = {'baz': False,
                  'foo': 3.14,
                  'bar': 42,
                  'fruit': 'apple',
                  'quuix': None}
        self.assertEqual(result, expect)

    def test_jsonb(self):
        """Test JSON (jsonb)"""
        self.cur.execute(
            """
            SELECT '{
                "foo": "bar",
                "bar": 42,
                "baz": false,
                "quuix": null,
                "foo": 3.14,
                "fruit": "apple"
            }'::jsonb;
            """
        )
        result = self.cur.fetchone()[0]
        expect = {'baz': False,
                  'foo': 3.14,
                  'bar': 42,
                  'fruit': 'apple',
                  'quuix': None}
        self.assertEqual(result, expect)

if __name__ == '__main__':
    unittest.main()
