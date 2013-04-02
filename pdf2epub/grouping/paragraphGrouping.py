from lxml import etree
import pdf2epub.common as common

# lineHeightgrouping groups lines into paragraphs based on the
# height of the line. Lines with the same height are determined
# to be part of the same paragraph
class _lineHeightGrouping():
    def __init__(self):
        pass
    def apply(self, page, c):
        output = common.copyElementAttributes(page)
        paragraph = etree.Element('PARAGRAPH')
        lines  = page.getchildren() 

        if (len(lines) > 1):
            paragraph.append(lines[0])

        for i in xrange(0, len(lines) - 1):
            current = lines[i]
            nxt     = lines[i + 1]
            c_info  = common.lineExtract(current)
            n_info  = common.lineExtract(nxt)
            if (common.looseCompare(c_info['height'],n_info['height'],c['line_height_diff'])):
                # same para
                paragraph.append(nxt)
            else:
                # new para
                output.append(paragraph)
                paragraph = etree.Element('PARAGRAPH')
                paragraph.append(nxt)

        # add final paragraph
        output.append(paragraph)
        
        return output
    
    def requirements(self):
        return { 'line_height_diff' : 'allowed size difference between line heights' }

# some books have chapters where the first character (or perhaps more) of the
# first sentence of the first paragraph have a large letter.
# this class merges them into one 
class _chapterStartLetter():
    def __init__(self):
        pass
    def apply(self, page, c):
        for paragraph in page.iter('PARAGRAPH'):
            start = self.numberOfStartChars(paragraph)
            if (start > 0):
                if (self.fixStartChars(paragraph, start)):
                    self.mergeStartChars(paragraph, start)

        return page
             
    def numberOfStartChars(self, paragraph):
        lines = paragraph.getchildren()
        count = 0
        if (len(lines) > 1):
            for token in lines[0].iter('TOKEN'):
                info = common.tokenExtract(token)
                if (info['chars'] == 1):
                    # single character
                    count = count + 1
                else:
                    break
        return count

    def fixStartChars(self, paragraph, num):
        lines  = paragraph.getchildren()

        # the first 'non large' word on the page
        # has the x value which is the same start
        # value as the lines affected by the large start letter
        first  = lines[0]
        tokens = first.getchildren()
        first_normal = tokens[num]        
        first_info   = common.tokenExtract(first_normal)
        first_x      = first_info['x']

        # figure out indent by looking for the first line
        # with a different indent
        indent = None
        for i in xrange(1, len(lines)):
            line_info = common.lineExtract(lines[i])
            if (line_info['left'] != first_x):
                indent = line_info['left']
                break

        # if we found an indent fix line indents
        if (indent != None):
            lines[0].set('left', unicode(indent))
            for i in xrange(1, len(lines)):
                line_info = common.lineExtract(lines[i])
                if (line_info['left'] == first_x):
                    lines[i].set('left', unicode(indent))
            return True
        else:
            return False
        

    def mergeStartChars(self, paragraph, num):
        lines = paragraph.getchildren()
        tokens = lines[0].getchildren()
        merge = ""
   
        for i in xrange(0, num):
            merge = merge + tokens[i].text 
            lines[0].remove(tokens[i])

        merge = merge + tokens[num].text
        tokens[num].text = merge

    def requirements(self):
        return {}

# splitOnIndent splits up paragraphs when an
# indented line is found
class _splitOnIndent():
    def __init__(self):
        pass
    def apply(self, page, c):
        output = common.copyElementAttributes(page)
        for paragraph in page.iter('PARAGRAPH'):
            paras = self.split(paragraph,c )    
            for para in paras:
                output.append(para)

        return output

    def split(self, paragraph, c):
        lines = paragraph.getchildren()
        indent  = self.estimateIndent(paragraph, c)
        justify = self.estimateJustify(paragraph, c)
        output = []
        tmp = etree.Element('PARAGRAPH')
        info = None
        for i in xrange(0,len(lines)):
            info = common.lineExtract(lines[i])
            if (common.looseCompare(info['left'],indent,c['para_indent_diff'])):
                # same para
                tmp.append(lines[i])
            elif (i == 0):
                # indented first line 
                tmp.append(lines[i])
            else:
                # new para
                tmp.set('complete', 'yes')
                output.append(tmp)
                tmp = etree.Element('PARAGRAPH')
                tmp.append(lines[i])

        if (info != None):
            if (common.looseCompare(info['right'],justify,c['para_indent_diff'])):
                if (len(tmp) == 1):
                    tmp.set('complete', 'yes')
                else:
                    tmp.set('complete', 'no')
            else:
                tmp.set('complete', 'yes')

            output.append(tmp)
        return output

    def estimateIndent(self, paragraph, c):
        lines = paragraph.getchildren()
        right = []
        for i in xrange(0,len(lines)):
            info = common.lineExtract(lines[i])
            right.append(info['left'])

        if (len(right) <= 2):
            indent = common.smallest(right)
        else:
            indent = common.mostCommon(right)
        return indent

    def estimateJustify(self, paragraph, c):
        lines = paragraph.getchildren()
        right = []
        for i in xrange(0,len(lines)):
            info = common.lineExtract(lines[i])
            right.append(info['right'])

        if (len(right) <= 2):
            indent = common.largest(right)
        else:
            indent = common.mostCommon(right)
        return indent
        
    def requirements(self):
        return { 'para_indent_diff' : 'allowed difference between line indents before a new paragraph is formed' }

# split up paragraphs if there is a space larger than the
# height of one line between two lines.
class _splitOnVerticalGap():
    def __init__(self):
        pass
    def apply(self, page, c):
        output = common.copyElementAttributes(page)
        for paragraph in page.iter('PARAGRAPH'):
            paras = self.split(paragraph,c )    
            for para in paras:
                output.append(para)
       
        return output

    def split(self, paragraph, c):
        output = []    
        lines = paragraph.getchildren()
        common_diff  = self.lineDiff(lines)


        tmp = etree.Element('PARAGRAPH')
        if (len(lines) > 0):
            tmp.append(lines[0])

        for i in xrange(0,len(lines) - 1):
            a = lines[i]
            b = lines[i + 1]
            
            a_values = common.lineExtract(a)
            b_values = common.lineExtract(b)

            diff = b_values['base'] - a_values['base']

            if (common.looseCompare(common_diff,diff,c['vertical_diff'])):
                # same
                tmp.append(b)
            else:
                # split
                output.append(tmp)
                tmp = etree.Element('PARAGRAPH')
                tmp.append(b)

        output.append(tmp)
        return output

    def lineDiff(self,lines):
        values = []
        for i in xrange(0, len(lines) - 1):
            a = lines[i]
            b = lines[i + 1]

            a_info = common.lineExtract(a)
            b_info = common.lineExtract(b)
            values.append(b_info['base'] - a_info['base'])

        return common.mostCommon(values)
            

        
    def requirements(self):
        return {'vertical_diff' : 'allowed space between lines before a new para is created'}


class _createSummary():
    def __init__(self):
        pass
    def apply(self, page, c):
        for para in page.iter('PARAGRAPH'):
            self.paragraphSummary(para)

        return page

    def paragraphSummary(self, para):
        base  = None
        top   = None
        left  = None
        right = None
        chars = 0
        lines = 0
        height = []
        for line in para.iter('LINE'):
            info = common.lineExtract(line)

            if (base == None):
                base = info['base']
            else:
                if (info['base'] > base):
                    base = info['base']
            
            if (top == None):
                top = info['top']
            else:
                if (info['top'] < top):
                    top = info['top']

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
            height.append(info['height'])
            lines += 1

        # apply summary        
        para.set('base',   unicode(base))
        para.set('top',    unicode(top))
        para.set('left',   unicode(left))
        para.set('right',  unicode(right))
        para.set('chars',  unicode(chars))
        para.set('height', unicode(common.mostCommon(height)))
        para.set('lines', unicode(lines))


    def requiremnets():
        return {}

# make class instances available
lineHeightGrouping = _lineHeightGrouping()
chapterStartLetter = _chapterStartLetter()
splitOnIndent      = _splitOnIndent()
splitOnVerticalGap = _splitOnVerticalGap()
createSummary      = _createSummary()
