import argparse
import csv
import logging

from os import path
from PyPDF2 import PdfFileWriter, PdfFileMerger

# Define Argparse
parser = argparse.ArgumentParser(description='Merge PDF files and customize results.')
parser.add_argument('infiles', nargs='*', type=argparse.FileType('r'), action='append')
parser.add_argument('--csv', type=argparse.FileType('r'),
                    help='CSV file with PDF documents, titles, and page numbers for bookmarks.')
parser.add_argument('--yaml', type=argparse.FileType('r'),
                    help='YAML file with PDF documents, titles, and page numbers for bookmarks.')
parser.add_argument('-f', '--filedir', type=str, help='Directory containing all PDFs and CSV to include.')
parser.add_argument('-o', '--outfile', type=argparse.FileType('w'), help='The output file name.')


def merge_docs():
    pass


if __name__ == '__main__':
    merge_docs()

# root_dir = r'C:\Users\Andrew\Dropbox\OLS\Products\_JET Product Rollups\20220422'
# product_name = 'JET Product Roll Up 22 April 2022'
#
# merger = PdfFileMerger()
# merger.addMetadata({u'/Title': product_name})
#
# products = []
#
# with open(path.join(root_dir, 'publishing.csv'), encoding='utf-8-sig') as csvfile:
#     reader = csv.DictReader(csvfile)
#     product = None
#     for row in reader:
#         # If the product title is not in product keys, add a new entry for the product
#         if product is not None and row['title'] != product['title']:
#             products.append(product)
#             product = None
#
#         if product is None:
#             product = {'title': row['title'],
#                        'file': path.join(root_dir, row['file']),
#                        'page': row['page'],
#                        'subtitles': []}
#         else:
#             if row['subtitle'] is not None:
#                 product['subtitles'].append((row['subtitle'], row['sub_page'], row['page']))
#
#     # Catch dangling products if they haven't been added
#     if product is not None:
#         products.append(product)
#
# for product in products:
#     merger.append(product['file'], import_bookmarks=False)
#     bookmark = merger.addBookmark(product['title'], product['page'])
#     for subtitle in product['subtitles']:
#         merger.addBookmark(subtitle[0], subtitle[2], bookmark)
#
# merger.write(path.join(root_dir, f'{product_name}.pdf'))
# merger.close()