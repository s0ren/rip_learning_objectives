﻿import tabula
import sys
import pandas as pd

def parse(file_name):
        # Read pdf into a list of DataFrame
    # dfs = tabula.read_pdf("test.pdf", pages=[19, 20, 21], pandas_options={'header': None})
    dfs = tabula.read_pdf(file_name, 
                        pages='all',
                        #   pages=[19, 20, 21],
                        guess=False,
                        pandas_options={'header': None})

    # print("n df's:", len(dfs))

    # print(len(dfs[0].columns))

    dfs = [df.iloc[:, 0] for df in dfs]

    lines = []
    for df in dfs:
        # print(len(df))
        lines.extend(df.values)

    # kun de linjer der er str
    lines = [l for l in lines if type(l) is str]

    # kun linjer der ikke indeholder 'Tilknytningsperiode'
    lines = [l for l in lines if 'Tilknytningsperiode' not in l]

    # kun linjer der ikke indeholder 'Nr. Målpind'
    lines = [l for l in lines if 'Nr. Målpind' not in l]

    md_top = f'# {lines[2]}' + '\n\n'
    md_top += f'{lines[3]}' + '  \n'
    md_top += f'_{lines[4]}_' + '\n\n'

    # fjern headere
    '''
    Metalindustriens Uddannelsesudvalg
    Uddannelsesordning for data- og kommunikationsuddannelsen
    Uddannelsesordning for 1205 Data- og kommunikationsuddannelsen (version 10)
    Bekendtgørelse om data- og kommunikationsuddannelsen (01-08-2023)
    Elevtypesamling: Ungdom og EUV3
    Fag fælles for hovedforløb
    Øvrige
    '''
    # lines = lines[7:] 

    # på hver side
    bad_h = '''
    Metalindustriens Uddannelsesudvalg
    Uddannelsesordning for data- og kommunikationsuddannelsen
    Uddannelsesordning for 1205 Data- og kommunikationsuddannelsen (version 10)
    Bekendtgørelse om data- og kommunikationsuddannelsen (01-08-2023)
    '''
    lines = [l for l in lines if l not in bad_h]

    # print all lines
    # print(*lines, sep='\n')

    subjects = [l for l in lines if l[:5] == 'Fag: ']
    print('Antal rå fag fundet', len(subjects), file=sys.stderr)
    print( *subjects, sep='\n', file=sys.stderr)
    print(file=sys.stderr)

    fag = []
    i = 0
    while i < len(lines): 
        l = lines[i]
        # hvis der står 'Fag: ' starter et fag med 8 linjers top
        if l[:5] == 'Fag: ':
            print(l, file=sys.stderr)
            f_head = lines[i:i+7]
            # spring frem til læringsmål
            i += 7

            # print(f_head)

            # herefter kommer læringsmålene
            f_learn_objectives = []
            if i >= len(lines):
                break
            l = lines[i] 
            while l[:5] != 'Fag: ' and i < len(lines):
                

                # print(l)

                # hvis linies´n starter på et tal
                if l.split()[0].isnumeric():
                    f_learn_objectives.append(l)
                else:
                    # til føj til seneste læringsmål
                    f_learn_objectives[-1] += ' ' + l
                i += 1
                if i >= len(lines):
                    break
                l = lines[i]
            fag.append({'head': f_head, 'learn objectives': f_learn_objectives})
            # lidt wierd, men vi har inkremteret i for meget, så vil ruller tilbage
            i -= 2

        i += 1
    # print(fag)
    return fag, md_top

def build_md(fag, md):
#    if hasattr(args, 'toc') and args.toc:
    if args.toc:
        md += ('<div style="page-break-after: always; visibility: hidden"> \n'
                # + ' \pagebreak \n'
                + ' \\tableofcontents \n'
                # + r' \pagebreak \n'
                + '</div>\n')
    for f in fag:
        if args.pagebreaks:
            md += ('<div style="page-break-after: always; visibility: hidden">\n'
                    + ' \\pagebreak\n'
                    + '</div>\n\n')
            # alternativ kunne det vist også være <div style="page-break-before:always"></div>

        # for at lave en titel overskrift for hvert fag
        # tag første linje i head og split ord
        t = f['head'][0].split()
        # ord 1 er nummeret
        n = t[1]
        # resten er faget titel
        name = ' '.join(t[2:])
        md += f"## `{n}` {name}" + '\n\n'
        
        # head
        md += '|||' + '\n'
        md += '|:-|:-|' + '\n'
        for h in f['head']:
            # print(h)
            h_line = h.split(':')
            k = h_line[0]
            v = ':'.join(h_line[1:])
            md += f'|{k}|{v}|' + '\n'
        md += '\n'

        # objectives
        for o in f['learn objectives']:
            # md += o + '\n'
            w = o.split()
            md += f'{w[0]}. {" ".join(w[1:])}' + '\n'
        md += '\n'
    return md

def main(input_file_name):

    fag, md = parse(input_file_name)

    # markdown

    print('Antal hele fag:', len(fag), file=sys.stderr)

#
    md = build_md(fag, md)

    print(md, file=sys.stdout)

def get_filename():
    if len(sys.argv) > 1:
        return sys.argv[1]
    else:
        return 'test/data/test1.pdf'
    
def get_params():
    import argparse
    parser = argparse.ArgumentParser(
        prog='dump_tabula',
        description="Dumper fag og læringsmål fra pdf'fil fra uddannelsesadministration.dk, til markdown som kan redigeres eller konverteres videre (med f.eks. pandoc)",
        # usage=''
        # epilog=''
        )
    parser.add_argument('-i', 
                        action='store',
                        dest='input_filename',
                        # default=sys.stdin,
                        default='test/data/test1.pdf',
                        # type=argparse.FileType('r'),
                        help='the input file (a pdf) to dump. Default is "test/data/test1.pdf"',
    )
    parser.add_argument('-p', '--pagebreaks',
                        action='store_true',
                        default=False,
                        dest='pagebreaks',
                        help='Sideskift før hvert fag',
    )
    parser.add_argument('--toc',
                        action='store_true',
                        default=False,
                        dest='toc',
                        help='Indholdsfortegenlse',
    )
    # print('sys.argv:', sys.argv)
    args = parser.parse_args()
    # print(args.input_filename, args.count, args.verbose)
    return args
    

args = get_params()
if __name__ == '__main__':
    main(args.input_filename)