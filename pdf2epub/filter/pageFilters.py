# pageFilters are filters that operate on page elements within a book

# removePages filters pages from the book based on page number
class _removePages():
    def __init__(self):
        pass
    def apply(self, book, c):
        for page in book.iter('PAGE'):
            page_number = float(page.get('number'))
            if (page_number < c['start_page'] or page_number > c['end_page']):
                book.remove(page)
        return book

    def requirements(self):
        return { 'start_page': 'pages before this number will be removed',
                 'end_page'  : 'pages after this number will be removed' }

# make classes available as part of module
removePages = _removePages()
