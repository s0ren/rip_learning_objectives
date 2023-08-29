import unittest

import dump_tabula as dt

class TestEkstern(unittest.TestCase):

    # def test_parse_args():
    #     testargs = ["prog", "-f", "/home/fenton/project/setup.py"]
    #     with patch.object(sys, 'argv', testargs):
    #         setup = get_setup_file()
    #         assert setup == "/home/fenton/project/setup.py"

    def test_get_fielname(self):
        from unittest.mock import patch
        import sys
        testargs = ['dump_tabula.py', 'testfile.pdf', 'hest']

        expected_filename = testargs[1]

        with patch.object(sys, 'argv', testargs):
            actual_filename = dt.get_filename()
            self.assertEqual(expected_filename, actual_filename, 'filnavn overført til sys.argv[1]')

    def test_get_fielname_default(self):
        from unittest.mock import patch
        import sys
        testargs = ['dump_tabula.py',]

        expected_filename = 'test1.pdf'

        with patch.object(sys, 'argv', testargs):
            actual_filename = dt.get_filename()
            self.assertEqual(expected_filename, actual_filename, 'filnavn overført til sys.argv[1]')

    def test_main(self):
        """
        tester main med filen test1.pdf der kun indeholder 1 side- med 3 fag
        """
        from io import StringIO
        from unittest.mock import patch

        test_file_name = 'test/data/test1.pdf'

        expected_markdown = """# Uddannelsesordning for 1205 Data- og kommunikationsuddannelsen (version 10)

Bekendtgørelse om data- og kommunikationsuddannelsen (01-08-2023)  
_Fag: 1590 Fiberinstallation_

## `1590` Fiberinstallation

|||
|:-|:-|
|Fag| 1590 Fiberinstallation|
|Niveau| Avanceret|
|Opr. varighed| 1,0 uger|
|Fagkategori| Uddannelsesspecifikke fag|
|Bundet/Valgfri| Valgfri|
|Afkortning| 0%|
|Varighed| 1,0 uger|

1. Lærlingen kan udføre og implementere fiberinstallationer.
2. Lærlingen kan montere de korrekte fibertyper til givne installationer
3. Lærlingen kan kan fejlfinde og udføre reparation af fiberinstallationerne
4. Lærlingen kan foretage splidsning og konnektering af fiberkabler
5. Lærlingen kan foretage fejlfinding og reparation på fiberinstallationer
6. Lærlingen kan i forbindelse med fiberarbejde anvende og tilrette tilhørende dokumentation

## `1598` Mailserver i Windows organisationen

|||
|:-|:-|
|Fag| 1598 Mailserver i Windows organisationen|
|Niveau| Rutineret|
|Opr. varighed| 1,0 uger|
|Fagkategori| Uddannelsesspecifikke fag|
|Bundet/Valgfri| Valgfri|
|Afkortning| 0%|
|Varighed| 1,0 uger|

1. Lærlingen opnår et fagligt niveau minimum svarende til MCP Implementing and Managing Exchange Server 2003 eller nyere
2. Lærlingen kan installere en eller flere mailservere i et Windows Domæne
3. Lærlingen kan installere en mailserver i et cluster
4. Lærlingen kan installere en mailserver i et front-end/back-end system
5. Lærlingen kan administrere brugerkonti for mailserveren
6. Lærlingen kan konfigurere sikkerhed for mailserveren
7. Lærlingen kan lave backup og restore af dele af mailserveren
8. Lærlingen kan lave en disaster recovery af hele mailserveren
9. Lærlingen kan oprette delte mapper på mailserveren

## `6245` Gateway sikkerhed

|||
|:-|:-|
|Fag| 6245 Gateway sikkerhed|
|Niveau| Rutineret|
|Opr. varighed| 1,0 uger|
|Fagkategori| Uddannelsesspecifikke fag|
|Bundet/Valgfri| Valgfri|
|Afkortning| 0%|
|Varighed| 1,0 uger|

1. Lærlingen opnår et fagligt niveau minimum svarende til MCP "Implementing Internet Security and Acceleration Server".
2. Lærlingen kan udføre netdesign, placering af firewall i forhold til netværk.
3. Lærlingen kan installere og konfigurere en ISA Server.
4. Lærlingen kan konfigurere NAT (network address Tranlation) på ISA Server.
5. Lærlingen kan konfigurere klient computere (ISA client).
6. Lærlingen kan konfigurere og vedligeholde ISA Server vha. Management Console.


"""

        expected_status_message = """Antal rå fag fundet 3
Fag: 1590 Fiberinstallation
Fag: 1598 Mailserver i Windows organisationen
Fag: 6245 Gateway sikkerhed

Fag: 1590 Fiberinstallation
Fag: 1598 Mailserver i Windows organisationen
Fag: 6245 Gateway sikkerhed
Antal hele fag: 3
"""

        with patch('sys.stdout', new = StringIO()) as fake_out:
            with patch('sys.stderr', new = StringIO()) as fake_err:
                dt.main(test_file_name)
                self.assertEqual(fake_out.getvalue(), expected_markdown)
                self.assertEqual(fake_err.getvalue(), expected_status_message)


if __name__ == '__main__':
    unittest.main()