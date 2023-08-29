import unittest

import dump_tabula as dt

class TestParse(unittest.TestCase):

    def test_parse(self):
        test_file_name = 'test/data/test1.pdf'
        actual_fag, actual_md_top = dt.parse(test_file_name)
        self.assertEqual(len(actual_fag), 3, 'der skal være 3 fag')
        self.assertEqual(actual_fag[0]['head'][0], 'Fag: 1590 Fiberinstallation', 'Første fag er "1590 Fiberinstallation"')
        self.assertEqual(len(actual_fag[1]['learn objectives']), 9, 'Antal målepinde')
        self.assertEqual(actual_fag[2]['learn objectives'][1], '2 Lærlingen kan udføre netdesign, placering af firewall i forhold til netværk.', '3. fags 2. målpind')

        self.assertEqual(actual_fag[1]['learn objectives'][0], '1 Lærlingen opnår et fagligt niveau minimum svarende til MCP Implementing and Managing Exchange Server 2003 eller nyere', '2. fags første målpind')
        self.assertEqual(actual_fag[1]['learn objectives'][-1], '9 Lærlingen kan oprette delte mapper på mailserveren', '2. fags sidste målpind')
 
        self.assertEqual(len(actual_md_top), 178, 'Længden af md_top')
        self.assertIn('Data- og kommunikationsuddannelsen', actual_md_top)
        self.assertIn('data- og kommunikationsuddannelsen', actual_md_top)
        self.assertIn('1205', actual_md_top)
        self.assertIn('version 10', actual_md_top)
        self.assertIn('01-08-2023', actual_md_top)

if __name__ == '__main__':
    unittest.main()