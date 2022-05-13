import csv

from os import path
from PyPDF2 import PdfFileReader, PdfFileWriter

root_dir = r'C:\Users\Andrew\Dropbox\OLS\Products\_JET Product Rollups\20220513'
product_name = 'JET Product Roll Up 13 May 2022'

writer = PdfFileWriter()
writer.addMetadata({u'/Title': product_name})

products = []
bookmarks = []
page_index = 0

with open(path.join(root_dir, 'publishing.csv'), encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    product = None
    for row in reader:
        # If the product title is not in product keys, add a new entry for the product
        if product is not None and row['title'] != product['title']:
            products.append(product)
            product = None

        if product is None:
            product = {'title': row['title'],
                       'file': path.join(root_dir, row['file']),
                       'page': row['page'],
                       'subtitles': []}
        else:
            if row['subtitle'] is not None:
                product['subtitles'].append((row['subtitle'], row['sub_page'], row['page']))

    # Catch dangling products if they haven't been added
    if product is not None:
        products.append(product)

for product in products:
    _pdf = PdfFileReader(product['file'])
    writer.appendPagesFromReader(_pdf)

    bookmarks.append({'title': product.get('title'),
                      'page': product.get('page'),
                      'children': []})

    subtitles = product.get('subtitles')
    for subtitle in subtitles:
        bookmarks[-1].get('children').append({'title': subtitle[0],
                                              'page': int(subtitle[1]) + page_index})

    page_index = len(_pdf.pages) + page_index

# Add bookmarks to writer
for bookmark in bookmarks:
    parent = writer.addBookmark(bookmark.get('title'), int(bookmark.get('page')))
    for child in bookmark.get('children'):
        writer.addBookmark(child.get('title'), child.get('page'), parent)

writer.setPageLayout('/SinglePage')

with open(path.join(root_dir, f"{product_name}.pdf"), 'wb') as out:
    writer.write(out)
