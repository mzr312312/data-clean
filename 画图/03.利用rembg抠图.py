from rembg import remove
from PIL import Image
import io

#可以从文件夹中的所有图像中删除背景：
#rembg p path/to/folder path/to/output
#也可以从单个图像中删除背景：
#rembg p path/to/input.png path/to/output.png
#其中，path/to/folder是图像文件夹的路径，path/to/input.png是输入图像的路径，path/to/output.png是输出图像的路径。
#如果输出图像的格式是jpg，则会自动压缩。
#如果需要调整抠图的效果，可以调整参数，具体请参考rembg的文档。
#如果需要批量处理图像，可以用批处理命令行工具，如Windows的cmd或Linux的bash。

# 读取输入图像
input_path = 'input_image.png'  # 输入图像文件路径
output_path = 'output_image.png'  # 输出图像文件路径

with open(input_path, 'rb') as input_file:
    input_image = input_file.read()

# 进行抠图
output_image = remove(input_image)

# 保存输出图像
with open(output_path, 'wb') as output_file:
    output_file.write(output_image)

# 显示输出结果
output_img = Image.open(io.BytesIO(output_image))
output_img.show()
