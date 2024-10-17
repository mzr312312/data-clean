import camelot

tables = camelot.read_pdf(r"C:\Users\JA085914\Desktop\IoT数据统计点位收集(新增英文名称).pdf")
print(tables)
tables.export(r"C:\Users\JA085914\Desktop\extracted.csv", f="csv", compress=True)
