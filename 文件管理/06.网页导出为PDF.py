from weasyprint import HTML

url = 'https://fortelabs.com/blog/para/'
output_file = 'output.pdf'

# 从URL获取HTML
html = HTML(url)

# 将HTML转换为PDF
html.write_pdf(output_file)