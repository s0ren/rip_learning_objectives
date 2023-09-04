import unittest

import dump_tabula as dt

class TestMarkDown(unittest.TestCase):

    def test_markdown_kun_titel(self):
        '''
        Bygger en meget simpel parse model med kun titel i head og ingen mål, som vi tester om den giver den rigtige md
        '''
        # Arange
        fag = [ 
            {
                'head' : [
                    'Fag: 000 Fagets titel',
                    # 'head1: tekst 1',
                    # 'head2: tekst 2',
                    ],
                'learn objectives': [
                    # '1 første mål',
                    # '2 andet mål',
                ]
            }
        ]

        md_top = ''

        exptected_md = '''## `000` Fagets titel

|||
|:-|:-|
|Fag| 000 Fagets titel|


'''
        # Act
        actual_md = dt.build_md(fag, md_top)

        # Assert
        self.assertEqual(actual_md, exptected_md, 'simpel md')

    def test_markdown_titel_1head(self):
        '''
        Bygger en meget simpel parse model med kun fag titel og et head mere. Ingen mål, som vi tester om den giver den rigtige md
        '''
        # Arange
        fag = [ 
            {
                'head' : [
                    'Fag: 000 Fagets titel',
                     'head1: tekst 1',
                    # 'head2: tekst 2',
                    ],
                'learn objectives': [
                    # '1 første mål',
                    # '2 andet mål',
                ]
            }
        ]

        md_top = ''
        exptected_md = '''## `000` Fagets titel

|||
|:-|:-|
|Fag| 000 Fagets titel|
|head1| tekst 1|


'''
        # Act
        actual_md = dt.build_md(fag, md_top)

        # Assert
        self.assertEqual(actual_md, exptected_md, 'simpel md')

    def test_markdown_kun_titel_1mål(self):
        '''
        Bygger en meget simpel parse model- med titel og 1 mål, som vi tester om den giver den rigtige md
        '''
        # Arange
        fag = [ 
            {
                'head' : [
                    'Fag: 000 Fagets titel',
                    # 'head1: tekst 1',
                    # 'head2: tekst 2',
                    ],
                'learn objectives': [
                    '1 første mål',
                    # '2 andet mål',
                ]
            }
        ]

        md_top = ''

        exptected_md = '''## `000` Fagets titel

|||
|:-|:-|
|Fag| 000 Fagets titel|

1. første mål

'''
        # Act
        actual_md = dt.build_md(fag, md_top)

        # Assert
        self.assertEqual(actual_md, exptected_md, 'simpel md')

    def test_markdown(self):
        '''
        Bygger en meget simpel parse model, som vi tester om den giver den rigtige md
        '''
        # Arange

        fag = [ 
            {
                'head' : [
                    'Fag: 000 Fagets titel',
                    'head1: tekst 1',
                    'head2: tekst 2',
                    ],
                'learn objectives': [
                    '1 første mål',
                    '2 andet mål',
                ]
            }
        ]

        md_top = '# Top overskrift\n\n'

        exptected_md = '''# Top overskrift

## `000` Fagets titel

|||
|:-|:-|
|Fag| 000 Fagets titel|
|head1| tekst 1|
|head2| tekst 2|

1. første mål
2. andet mål

'''

        # Act

        actual_md = dt.build_md(fag, md_top)

        # Assert

        self.assertEqual(actual_md, exptected_md, 'simpel md')

if __name__ == '__main__':
    unittest.main()