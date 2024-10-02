from pymupdf import *

def analyze_font_sizes(pdf_path):
    size_s = list()          #Множество кеглей
    doc = open("test.pdf")
    counter = 1
    result = dict()

    for page in doc:
        text = page.get_text("dict")
        blocks = text["blocks"]
        page_lines = dict() 
        for blocks_index in range(0, len(blocks)):
            #print(blocks[blocks_index])
            if(blocks[blocks_index]["type"] == 0):
                for line in blocks[blocks_index]["lines"]:
                    spans = line["spans"][0]
                    line_text = spans["text"]
                    line_text_len = len(line_text)
                    if(line_text_len < 60 and line_text_len > 3):
                        page_lines[int(round(spans['size']))] = line_text
        if (page_lines):
            sort_fonts = sorted(page_lines.items(), key = lambda item: item[0], reverse = True)
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