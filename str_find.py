from pymupdf import *

def analyze_font_sizes(pdf_path):
    size_s = list()          #Множество кеглей
    doc = open("test.pdf")
    counter = 1             #Счетчик страниц
    result = dict()         #Итоговый словарь

    for page in doc:
        text = page.get_text("dict")        #Получение текста в виде словарей
        blocks = text["blocks"]             #Разбиение его на блоки
        page_lines = dict()                 #Словарь для каждой страницы с типом строка, размер шрифта
        for blocks_index in range(0, len(blocks)):
            if(blocks[blocks_index]["type"] == 0):          #Проверка, что нужный тип страницы
                for line in blocks[blocks_index]["lines"]:
                    spans = line["spans"][0]                #Получение нужного значения из line
                    line_text = spans["text"]
                    line_text_len = len(line_text)          #Проверка длины (не добавлять слишком длинные и короткие)
                    if(line_text_len < 60 and line_text_len > 3):
                        page_lines[int(round(spans['size']))] = line_text
        if (page_lines):
            sort_fonts = sorted(page_lines.items(), key = lambda item: item[0], reverse = True)     #Сортировка по размерам шрифта
            size_s.append(sort_fonts)
            cnt_size_s = len(size_s[counter-1])
            if cnt_size_s == 1:
                continue
            if cnt_size_s == 2:
                max_size = sort_fonts[0][0]
                for i in range(0, len(size_s[counter-1])):
                    if (size_s[counter-1][i][0] == max_size):
                        result[size_s[counter-1][i][1]] = (1,counter)
            if cnt_size_s == 3:
                max_size_1 = sort_fonts[0][0]
                max_size_2 = sort_fonts[1][0]
                for i in range(0, len(size_s[counter-1])):
                    if (size_s[counter-1][i][0] == max_size_1):
                        result[size_s[counter-1][i][1]] = (1,counter)
                    if (size_s[counter-1][i][0] == max_size_2):
                        result[size_s[counter-1][i][1]] = (2,counter)
        counter += 1
    return result