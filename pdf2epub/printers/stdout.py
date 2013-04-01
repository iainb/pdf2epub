

def printBook(book):
    for page in book.iter('PAGE'):
        printPage(page)

def printPage(page):
    print "Page: " + page.get('number')

    for line in page.iterchildren('LINE'):
        printLine(line)

    for text in page.iterchildren('TEXT'):
        printText(text)

    for para in page.iterchildren('PARAGRAPH'):
        printPara(para)

def printPara(para):
    print "<p " + para.get('complete', 'unknown')  + ">"
    for line in para.iter('LINE'):
        printLine(line)
    print "</p>"

def printLine(line):
    verbose = True
    verbose = False
    verbose_token = True
    verbose_token = False

    out = []
    for token in line.iter('TOKEN'):
        if (token.text != None):
            if (verbose_token == True):
                print token.items()
                print token.text
            out.append(token.text)
    if (verbose):
        print "<LINE>"
        print line.items()
        print " ".join(out)
        print "</LINE>"
    else:
        print " ".join(out)

def printText(text):
    out = []
    for token in text.iter('TOKEN'):
        if (token.text != None):
            out.append(token.text)
    print " ".join(out)
