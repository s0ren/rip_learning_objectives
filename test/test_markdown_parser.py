import unittest

import dump_tabula as dt
import mistletoe
from mistletoe import Document
from mistletoe.ast_renderer import AstRenderer

import json

class TestMarkDown_w_parser(unittest.TestCase):

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
        actual_ast = Document(actual_md)
        # with AstRenderer() as astRenderer:
            # print(astRenderer.render(actual_ast))

        # Assert
        self.assertIsInstance(actual_ast, Document, 'AST er typen Dokument')
        self.assertIsInstance(actual_ast.children, list, 'children er typen list')
        self.assertIsInstance(actual_ast.children[0], mistletoe.block_token.Heading, 'children[0] er typen Heading')
        self.assertIsInstance(actual_ast.children[0].children[0], mistletoe.span_token.InlineCode, 'Headings første child er typen InlineCode')
        self.assertIsInstance(actual_ast.children[0].children[1], mistletoe.span_token.RawText, 'Headings første child er typen RawText')
        #### Det er da mega træls at skrive...

        # ACT / Assert igen
        with AstRenderer() as astRenderer:
            # print(astRenderer.render(actual_ast))
            ast_json = json.loads( astRenderer.render(actual_ast) )
        self.assertEqual(ast_json['type'], 'Document')
        self.assertEqual(ast_json['children'][0]['type'], 'Heading')
        self.assertEqual(ast_json['children'][0]['children'][0]['type'], 'InlineCode')
        self.assertEqual(ast_json['children'][0]['children'][0]['children'][0]['type'], 'RawText')
        self.assertEqual(ast_json['children'][0]['children'][0]['children'][0]['content'], '000')

        self.assertEqual(ast_json['children'][1]['type'], 'Paragraph')
        # Det er jo næsten det samme... :-(

        # Act - Assert igen

        actial_l = actual_md.split('\n')
        # print(actial_l)

        # fag header
        self.assertIn('## `000` Fagets titel', actial_l[0])
        # fag tabel
        self.assertIn('|||', actial_l[2])
        self.assertIn('|:-|:-|', actial_l[3])
        # fag tabel titel
        self.assertIn('|Fag| 000 Fagets titel|', actial_l[4])
        
    # @unittest.skip
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
        # Act
        actual_md = dt.build_md(fag, md_top)

        actual_md = dt.build_md(fag, md_top)
        actual_ast = Document(actual_md)
        with AstRenderer() as astRenderer:
            print(astRenderer.render(actual_ast))

        actual_l = actual_md.split('\n')
        # print(*[f"{i}: {l}" for i,l in enumerate(actual_l)], sep='\n')


        # Assert
        self.assertAlmostEquals(len(actual_md), 78)

        self.assertIsInstance(actual_ast, Document, 'AST er typen Dokument')
       
        # table
        self.assertIsInstance(actual_ast.children[1], mistletoe.block_token.Paragraph, 'children[1] er typen Paragraph')
        self.assertIsInstance(actual_ast.children[1].children[1], mistletoe.span_token.LineBreak, 'table p andet child er typen LineBreak')
        self.assertIsInstance(actual_ast.children[1].children[6], mistletoe.span_token.RawText, 'table p\'s næstsidste child er typen RawText')
        self.assertEquals(actual_ast.children[1].children[6].content, '|head1| tekst 1|', 'table p\'s næstsidste child er ')

        self.assertIn('|head1| tekst 1|', actual_l[5])
        self.assertEquals(len(actual_l), 9)

    @unittest.skip
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

    @unittest.skip
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