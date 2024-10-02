import pymupdf
import math

g_font : str = "tiro"
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
    toc_page_number : int = 1
    toc_page : pymupdf.Page = doc.new_page(toc_page_number, width = g_page_width, height = g_page_height)
    font=pymupdf.Font(g_font)
    toc_page.insert_font(fontname="page_font", fontbuffer=font.buffer)
    toc_header = "Оглавление"
    text_len = pymupdf.get_text_length(toc_header, g_font, g_fontsize * 2)
    textbox = pymupdf.Rect(g_page_width / 2 - text_len * 2, g_drawer_y, g_page_width, g_drawer_y + g_fontsize * 8)
    g_drawer_y += g_fontsize * 4
    toc_page.insert_textbox(textbox, toc_header, fontsize=g_fontsize * 2, fontname="page_font")
    for header in dictionary:
        if(g_drawer_y >= g_page_height):
            toc_page_number += 1
            toc_page : pymupdf.Page = doc.new_page(toc_page_number, width = g_page_width, height = g_page_height)
            g_drawer_y = 30
        textbox = __gen_rect(dictionary[header][0], header)
        toc_page.insert_textbox(textbox, header, fontsize=g_fontsize, fontname="page_font", encoding=pymupdf.TEXT_ENCODING_CYRILLIC)
        link = toc_page.insert_link({"kind": pymupdf.LINK_GOTO, "page": dictionary[header][1] + toc_page_number - 1, "from": textbox, "to": pymupdf.Point(1, 1)})
    doc.save(output_filename)

def find_and_generate(dictionary: dict, input_filename: str, output_filename: str = "res.pdf", toc_starting_page : int = 0) -> None:
    doc = pymupdf.open(input_filename)
    for i in range(toc_starting_page, len(doc)):
        page = doc[i]
        blocks = page.get_text("blocks")
        for block in blocks:
            for key in dictionary:
                if key in block[4]:
                    rect = pymupdf.Rect(block[0], block[1], block[2], block[3])
                    link_info : dict = {"kind": pymupdf.LINK_GOTO, "page": int(dictionary[key][1]), "from": rect, "to": pymupdf.Point(1, 1)}
                    page.insert_link(link_info)
    doc.save(output_filename)