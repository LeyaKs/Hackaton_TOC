import pymupdf


FILE_NAME = "pril_V.pdf"


def content_check(doc):
    for i in range(2):
        page = doc.load_page(i)
        text = page.get_text("text")
        print(text)
        if ("Оглавление" in text) or ("Содержание" in text) \
                or ("ОГЛАВЛЕНИЕ" in text) or ("СОДЕРЖАНИЕ" in text):
            return text
    return None


def text_process(text):
    text = text.replace('\n', ' ')
    for i in range(10):
        text = text.replace('.' + str(i), '\\'+str(i))
    text = text.replace('.', ' ')
    text = text.replace('Глава', ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')
    if text[0] == ' ':
        text = text[1:]
    if text[-1] == ' ':
        text = text[:len(text) - 1]
    text = text.split(' ')
    for i in range(len(text)):
        if ("Оглавление" in text) or ("Содержание" in text) \
                or ("ОГЛАВЛЕНИЕ" in text) or ("СОДЕРЖАНИЕ" in text):
            text = text[1:]
        else:
            break
    return text


def word_check(word):
    alphabet_eng = 'AaBbСсDdEeFfGgHhIiJjKkLlMmNnОоРрQqRrSsTtUuVvWwXxYyZz'
    alphabet_eng_len = len(alphabet_eng)
    alphabet_rus = "аАеЕёЁиИоОуУыЫэЭюЮяЧбБвВгГдДжЖзЗйЙкКлЛмМнНпПрРсСтТфФхХцЦчЧшШщЩ"
    alphabet_rus_len = len(alphabet_rus)
    for i in range(alphabet_eng_len):
        if alphabet_eng[i] in word:
            return True
    for i in range(alphabet_rus_len):
        if alphabet_rus[i] in word:
            return True
    return False
    

def content_make(text):
    string = ""
    level = 1
    content = {}
    for i in range(len(text)):
        if string == "" and not word_check(text[i]):
            if '\\' in text[i]:
                level = 2
            else:
                level = 1
            continue
        if word_check(text[i]):
            if string != '':
                string += ' '
            string += text[i]
        else:
            content[string] = (level, text[i])
            string = ""
            level = 1
    return content
            


def content_take(doc):
    content = {}
    text = content_check(doc)
    if text == None:
        return content
    text = text_process(text)
    content = content_make(text)
    print(text)
    print(content)
    


content_take(pymupdf.open(FILE_NAME))
