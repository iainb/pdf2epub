from lxml import etree
import pdf2epub.common as common

# lineExtractors take a page which contains 'text' elements, which in turn contains
# 'token' elements and converts them into 'line' elements which contain 'token' elements

# simpleLineExtractor extracts all the lines from a page
# placing all tokens inside what it considers to be
# lines based on the token's y coordinates
class _simpleLineExtractor():
    def __init__(self):
        pass

    def apply(self,page,c):
        output = common.copyElementAttributes(page) 
        line_info = None
        for text in page.iter('TEXT'):
            for token in text.iter('TOKEN'):
                token_info = common.tokenExtract(token)

                if (line_info == None):
                    line_info = token_info
                    line = etree.Element('LINE')
                
                if (common.looseCompare(token_info['y'],line_info['y'],c['y_height_diff'])):
                    # same line
                    line.append(token)
                else:
                    # new line
                    output.append(line)

                    # reset
                    line = etree.Element('LINE')
                    line.append(token)
                    line_info = token_info

        # handle last line
        if (line_info != None):
            output.append(line)

        for line in output.iter('LINE'):
            self.lineSummary(line)

        return output

    def lineSummary(self, line):
        base   = []
        top    = []
        height = []
        left  = None
        right = None 
        chars = 0

        for token in line.iter('TOKEN'):
            info = common.tokenExtract(token)
            base.append(info['base'])
            top.append(info['top'])
            height.append(info['height'])
            
            if (left == None):
                left = info['left']
            else:
                if (info['left'] < left):
                    left = info['left']

            if (right == None):
                right = info['right']
            else:
                if (info['right'] > right):
                    right = info['right']

            chars = chars + info['chars']

        # apply summary
        if (len(base) <= 2):
            line.set('base', unicode(common.largest(base)))
        else:
            line.set('base', unicode(common.mostCommon(base)))

        if (len(top) <= 2):
            line.set('top', unicode(common.smallest(top)))
        else:
            line.set('top',    unicode(common.mostCommon(top)))

        line.set('left',   unicode(left))
        line.set('right',  unicode(right))
        
        if (len(height) <= 2):
            line.set('height', unicode(common.largest(height)))
        else:
            line.set('height', unicode(common.mostCommon(height)))
        line.set('chars',  unicode(chars))
        
    def requirements(self):
        return {'y_height_diff': 'pixel difference between two line "y" values to consider them the same'}

simpleLineExtractor = _simpleLineExtractor()
