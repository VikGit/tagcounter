#!/bin/env python3

import unittest
from tagcounter.tagcounter import *

class Test(unittest.TestCase):
    """
    Here are placed all unittests for tagcounter app.
    """
    def test_GetResponse(self):
        """
        Ensure that GetResponse is able to download web page
        """
        resp = GetResponse('google.com')
        resp.get()
        self.assertIn(b'html', resp.body)

    def test_DB(self):
        """
        Check if is possible to insert and select data from DB
        """
        dbname = 'test_db'
        db = DB(dbname)
        db.insert('ggl', 'google.com', {'body': 1})
        res = db.select('ggl')
        db.close()
        self.assertEqual(res[0], 'ggl')
        if os.path.exists(dbname):
            os.remove(dbname)

    def test_counter(self):
        """
        Try to count HTML tags on the page
        """
        html = "<h1> My HTML </h1>"
        res, _useless = counter(html)
        self.assertEqual(res['h1'], 1)


if __name__ == '__main__':
    unittest.main()
