from PIL import Image


def split_image_custom(image_path, rows=12, cols=6):
    # 打开图片
    with Image.open(image_path) as img:
        width, height = img.size

        # 四舍五入宽度到最近的整数
        width = round(width)

        # 计算每个子图的宽度和高度
        cell_width = width // cols
        cell_height = height // rows

        # 创建保存子图的列表
        images = []

        # 循环分割图片
        for row in range(rows):
            for col in range(cols):
                # 定义每个子图的左上角和右下角坐标
                left = col * cell_width
                top = row * cell_height
                right = min((col + 1) * cell_width, width)  # 防止超出边界
                bottom = min((row + 1) * cell_height, height)  # 防止超出边界

                # 使用crop函数切割出子图
                cropped_img = img.crop((left, top, right, bottom))

                # 添加切割后的子图到列表中
                images.append(cropped_img)

                # 如果需要保存每个子图，可以这样做:
                # cropped_img.save(f'sub_{row}_{col}.png')

    return images


# 使用函数
image_path = r'C:\Users\JA085914\Desktop\爬塔\11\Picsew_20241024152018.jpg'  # 替换成你的图片路径
sub_images = split_image_custom(image_path)

# 可以保存所有子图到文件
for i, sub_img in enumerate(sub_images):
    sub_img.save(f'sub_{i}.png')