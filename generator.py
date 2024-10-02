import pymupdf
import math

g_font : str = "times-roman"
g_fontsize : int = 11

g_line_spacing : float = 10
g_indent : float = 30

g_page_width : float = 595
g_page_height : float = 842

g_drawer_y : float = 30

def __gen_rect(rank: int, header: str) -> pymupdf.Rect:
    global g_drawer_y
    drawer_x = __indent(rank)
    textbox_width = g_page_width - drawer_x - g_indent
    text_len = pymupdf.get_text_length(header, g_font, g_fontsize)
    rows_number = math.ceil(text_len / textbox_width)
    textbox = pymupdf.Rect(drawer_x, g_drawer_y, g_page_width, g_drawer_y + g_fontsize * rows_number * 2)
    g_drawer_y += g_fontsize * rows_number * 2
    return textbox

def __indent(rank: int) -> float:
    atan_res = math.atan((rank - 1) / 5) / math.pi
    return g_indent + atan_res * g_page_width

def generate(dictionary: dict, input_filename: str, output_filename: str) -> None:
    global g_drawer_y
    doc = pymupdf.open(input_filename)
    toc_page_number : int = 0
    toc_page : pymupdf.Page = doc.new_page(toc_page_number, width = g_page_width, height = g_page_height)
    toc_page.insert_font(g_font)
    for header in dictionary:
        if(g_drawer_y >= g_page_height):
            toc_page_number += 1
            toc_page : pymupdf.Page = doc.new_page(toc_page_number, width = g_page_width, height = g_page_height)
            g_drawer_y = 30
        textbox = __gen_rect(dictionary[header][0], header)
        toc_page.insert_textbox(textbox, header, fontsize=g_fontsize, fontname=g_font)
        link = toc_page.insert_link({"kind": pymupdf.LINK_GOTO, "page": dictionary[header][1] + toc_page_number, "from": textbox, "to": pymupdf.Point(1, 1)})
    doc.save(output_filename)

def find_and_generate(dictionary: dict, input_filename: str, output_filename: str = "res.pdf", toc_starting_page : int = 0) -> None:
    doc = pymupdf.open(input_filename)
    for i in range(toc_starting_page, len(doc)):
        page = doc[i]
        blocks = page.get_text("blocks")
        print(blocks)
        for block in blocks:
            for key in dictionary:
                if key in block[4]:
                    rect = pymupdf.Rect(block[0], block[1], block[2], block[3])
                    page.insert_link({"kind": pymupdf.LINK_GOTO, "page": dictionary[key][1], "from": rect, "to": pymupdf.Point(1, 1)})
    doc.save(output_filename)

def main():
    find_and_generate({}, "Отчет эмитента 6 месяцев 2023.pdf", "res.pdf", 0)

if __name__ == "__main__":
    main()