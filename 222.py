import openpyxl
with open('new_file_20240605140841.txt', "r", encoding='utf-8') as file:
    content = file.readlines()


# content.
def write_to_excel(content):
    book = openpyxl.Workbook()
    sheet = book.active
    for ct in content:
        if ct == '\n':
            continue
        else:
            sheet.append([ct])
    book.save('家宽.xlsx')
write_to_excel(content)