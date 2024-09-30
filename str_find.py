import os
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar

def analyze_font_sizes(pdf_path):
    size_s = set()                         # Множество размеров шрифтов
    for page in extract_pages(pdf_path):
        for element in page:
            for line in element:
                if isinstance(line, LTTextContainer):   #Проверка на строку
                    for char in line:
                        size_s.add(int(round(char.size)))    #Добавление шрифта в список
                        break
    size_sorted = sorted(size_s, reverse=True) 
    str_type = {}                       #Готовый словарь
    for page in extract_pages(pdf_path):
        for element in page:
            for line in element:
                if isinstance(line, LTTextContainer):   #Проверка на строку
                    for char in line:
                        if (int(round(char.size)) == size_sorted[0]):
                            str_type[line.get_text()] = (1, int(round(char.size)))
                        if (int(round(char.size)) == size_sorted[1]):
                            str_type[line.get_text()] = (2, int(round(char.size)))
                        break
    return str_type