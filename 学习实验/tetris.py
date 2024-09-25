import pygame
import sys
import random

# 初始化Pygame
pygame.init()

# 设置窗口大小
width, height = 300, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('俄罗斯方块')

# 定义方块的形状
shapes = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

# 定义游戏区域
grid_width, grid_height = 10, 20
grid = [[0 for _ in range(grid_width)] for _ in range(grid_height)]

# 处理方块的移动和旋转
current_shape = random.choice(shapes)
shape_x, shape_y = 4, 0  # 调整初始位置

# 设置下落速度和键盘快捷键
fall_speed = 10  # 方块自动下落速度，单位为毫秒
key_left = pygame.K_LEFT
key_right = pygame.K_RIGHT
key_down = pygame.K_DOWN
key_rotate = pygame.K_UP

def collides(grid, shape, x, y):
    for dy, row in enumerate(shape):
        for dx, val in enumerate(row):
            if val and (y + dy >= grid_height or x + dx < 0 or x + dx >= grid_width or grid[y + dy][x + dx]):
                return True
    return False

def merge_shape(grid, shape, x, y):
    for dy, row in enumerate(shape):
        for dx, val in enumerate(row):
            if val:
                grid[y + dy][x + dx] = 1

def clear_lines(grid):
    full_lines = []
    for y, row in enumerate(grid):
        if all(row):
            full_lines.append(y)
    for y in full_lines:
        del grid[y]
        grid.insert(0, [0 for _ in range(grid_width)])

# 绘制游戏区域
def draw_grid(screen, grid):
    block_size = 30
    for y, row in enumerate(grid):
        for x, val in enumerate(row):
            if val:
                pygame.draw.rect(screen, (255, 255, 255), (x * block_size, y * block_size, block_size, block_size), 0)

# 绘制当前方块
def draw_shape(screen, shape, x, y):
    block_size = 30
    for dy, row in enumerate(shape):
        for dx, val in enumerate(row):
            if val:
                pygame.draw.rect(screen, (255, 255, 255), ((x + dx) * block_size, (y + dy) * block_size, block_size, block_size), 0)

# 旋转方块
def rotate_shape(shape):
    return list(zip(*shape[::-1]))

# 游戏循环
running = True
clock = pygame.time.Clock()
fall_time = 0

while running:
    clock.tick(60)
    fall_time += clock.get_rawtime()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == key_left:
                if not collides(grid, current_shape, shape_x - 1, shape_y):
                    shape_x -= 1
            elif event.key == key_right:
                if not collides(grid, current_shape, shape_x + 1, shape_y):
                    shape_x += 1
            elif event.key == key_down:
                if not collides(grid, current_shape, shape_x, shape_y + 1):
                    shape_y += 1
            elif event.key == key_rotate:
                rotated_shape = rotate_shape(current_shape)
                if not collides(grid, rotated_shape, shape_x, shape_y):
                    current_shape = rotated_shape

    # 方块自动下落
    if fall_time >= fall_speed:
        fall_time = 0
        if not collides(grid, current_shape, shape_x, shape_y + 1):
            shape_y += 1
        else:
            merge_shape(grid, current_shape, shape_x, shape_y)
            clear_lines(grid)
            current_shape = random.choice(shapes)
            shape_x, shape_y = 4, 0  # 调整初始位置

    # 填充屏幕
    screen.fill((0, 0, 0))

    # 绘制游戏区域
    draw_grid(screen, grid)

    # 绘制当前方块
    draw_shape(screen, current_shape, shape_x, shape_y)

    # 更新屏幕
    pygame.display.flip()

# 退出Pygame
pygame.quit()
sys.exit()
