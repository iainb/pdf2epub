# tokenFilters are filters that operate on token elements

# trimHeaderAndFooter removes token elements from the page
# which have fall inside the header_size or footer_size
class _trimHeaderAndFooter():
    def __init__(self):
        pass
    
    def apply(self, page, c):
        page_number = float(page.get('number'))
        page_height = float(page.get('height'))
        upper_cutoff = c['header_size']
        lower_cutoff = page_height - c['footer_size']

        removed_text = []
        l = []
        for text in page.iter('TEXT'):
            for token in text.iter('TOKEN'):
                y = float(token.get('y'))
                if (y < upper_cutoff or y > lower_cutoff):
                    removed_text.append(token.text)
                    text.remove(token)
                else:
                    if (token.text != None):
                        l.append(token.text)
        return page

    def requirements(self):
        return { 'header_size': 'header size in pixels',
                 'footer_size': 'footer size in pixels' }

trimHeaderAndFooter = _trimHeaderAndFooter()
