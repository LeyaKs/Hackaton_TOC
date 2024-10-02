import pymupdf



FILE_NAME = "Отчет эмитента 6 месяцев 2023.pdf"
SPECIAL_SYMBOL = "\\\\\\"
CONTENT_NAME = ["оглавление", "Оглавление", "ОГЛАВЛЕНИЕ", \
                "содержание", "Содержание", "СОДЕРЖАНИЕ", \
                "content", "Content", "CONTENT"]
content_page = -1
count_page = -1
g_string = SPECIAL_SYMBOL


def content_name_check(text):
    for i in range(len(CONTENT_NAME)):
            if CONTENT_NAME[i] in text:
                return True
    return False

def content_check(doc):
    global content_page
    global count_page
    for i in range(count_page):
        page = doc.load_page(i)
        text = page.get_text("text")
        print(text)
        if content_name_check(text):
            content_page = i + 1
            return text
    return None


def text_process(text):
    text = text.replace('\n', ' ')
    for i in range(10):
        for j in range(10):
            text = text.replace(str(j) + '.' + str(i), str(j) + SPECIAL_SYMBOL + str(i))
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
        if content_name_check(text):
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
    global g_string
    string = ""
    level = 1
    content = {}
    for i in range(len(text)):
        if string == "" and not word_check(text[i]):
            if SPECIAL_SYMBOL in text[i]:
                level = 2
            else:
                level = 1
            continue
        if word_check(text[i]):
            if string != '':
                string += ' '
            string += text[i]
        else:
            if SPECIAL_SYMBOL in string:
                string = string.replace(SPECIAL_SYMBOL, '.')
            if g_string == SPECIAL_SYMBOL:
                g_string = string
            content[string] = (level, text[i])
            string = ""
            level = 1
    return content



def content_take(doc):
    global content_page
    global count_page
    count_page = doc.page_count
    print("!!!!!!!!!" + str(count_page))
    FIRST_CHAPTER = SPECIAL_SYMBOL
    content = {}
    text = content_check(doc)
    if text == None:
        return content
    for i in range(content_page, count_page):
        print(text)
        if g_string in text:
            break
        text = text_process(text)
        content = {**content, **content_make(text)}
        page = doc.load_page(i)
        text = page.get_text("text")
    print(text)
    print(content)
    
    return content
