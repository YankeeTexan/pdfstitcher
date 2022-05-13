import argparse
import json
import logging

from os import path
from PyPDF2 import PdfFileMerger

# Define Argparse
parser = argparse.ArgumentParser(description='Merge PDF files and customize results.')
parser.add_argument('infiles', nargs='*', type=argparse.FileType('r'), action='append')
parser.add_argument('--csv', type=argparse.FileType('r'),
                    help='CSV file with PDF documents, titles, and page numbers for bookmarks.')
parser.add_argument('--yaml', type=argparse.FileType('r'),
                    help='YAML file with PDF documents, titles, and page numbers for bookmarks.')
parser.add_argument('-f', '--filedir', type=str, help='Directory containing all PDFs and CSV to include.')
parser.add_argument('-o', '--outfile', type=argparse.FileType('w'), help='The output file name.')


class MergedDocument:
    def __init__(self, outfile, data: dict):
        self.file_dir = data['directory']
        self.outfile = outfile
        self.title = data['title']
        self.bookmarks = []
        self.merger = PdfFileMerger()
        self.page_index = 0
        for document in data['documents']:
            self.add_document(document)

    def add_document(self, document: dict):
        # pdf = PdfFileReader(path.join(self.file_dir, document['path']))
        pdf = path.join(self.file_dir, document['path'])
        self.merger.append(pdf, import_bookmarks=False)
        _start_page = self.page_index
        self.bookmarks.append({'title': document['title'],
                               'page': self.page_index,
                               'subtitles': []})
        if 'subtitles' in document.keys():
            for subtitle in document['subtitles']:
                sub_page = _start_page + subtitle['page'] - 1
                self.bookmarks[-1]['subtitles'].append({'subtitle': subtitle['subtitle'],
                                                        'page': sub_page})
        # Increment the page index
        self.page_index = len(self.merger.pages)

    def write_document(self):
        print(f"Adding bookmarks")
        for bookmark in self.bookmarks:
            print(f"Adding Bookmark {bookmark['title']} on page {bookmark['page']}.")
            _bm = self.merger.addBookmark(bookmark['title'], bookmark['page'])
            for subtitle in bookmark['subtitles']:
                print(f"Adding subtitle {subtitle['subtitle']} on page {subtitle['page']}.")
                self.merger.addBookmark(subtitle['subtitle'], subtitle['page'], parent=_bm)

        print(f"Writing {self.title} to output file {self.outfile}")
        self.merger.write(self.outfile)
        self.merger.close()


def merge_docs(outfile, json_file_path):
    with open(json_file_path, 'rb') as _json:
        data = json.load(_json)
    merged = MergedDocument(outfile, data)
    merged.write_document()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    merge_docs('test_output.pdf', './data/test.json')
