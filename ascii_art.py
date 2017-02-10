from PIL import Image
import numpy as np
import math, os
from concurrent import futures


def translate_block(img):
    a = np.array(img)
    gray_scale = a.mean()
    char_table = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    return char_table[int(gray_scale / 255 * (len(char_table) - 1))]


def convert_block(image, start_x, start_y, end_x, end_y):
    block = image.crop((start_x, start_y, end_x, end_y))
    return translate_block(block)


# def convert_row(image, row, columns, block_width, block_height):
#     width, height = image.size
#     for column in range(columns):
#         start_x, start_y = column * block_width, row * block_height
#         end_x = int(start_x + block_width if start_x + block_width < width else width)
#         end_y = int(start_y + block_height if start_y + block_height < height else height)
#         start_x, start_y = int(start_x), int(start_y)

def parallel_convert(image, columns, scale):
    width, height = image.size
    block_width = width / columns
    block_height = block_width / scale
    rows = math.ceil(height / block_height)
    art = [[None for i in range(columns)] for i in range(rows)]
    fd = {}
    with futures.ProcessPoolExecutor(max_workers=4) as executor:
        for row in range(rows):
            for column in range(columns):
                start_x, start_y = column * block_width, row * block_height
                end_x = int(start_x + block_width if start_x + block_width < width else width)
                end_y = int(start_y + block_height if start_y + block_height < height else height)
                start_x, start_y = int(start_x), int(start_y)
                future = executor.submit(convert_block, image, start_x, start_y, end_x, end_y)
                fd[row, column] = future
                results = futures.as_completed(fd.values())
                for k, v in fd.items():
                    art[k[0]][k[1]] = v.result()

    for row in range(rows):
        art[row] = ''.join(art[row])

    return '\n'.join(art)


def sequential_convert(image, columns, scale):
    width, height = image.size
    block_width = width / columns
    block_height = block_width / scale
    rows = math.ceil(height / block_height)
    art = []
    for row in range(rows):
        art.append('')
        for column in range(columns):
            start_x, start_y = column * block_width, row * block_height
            end_x = int(start_x + block_width if start_x + block_width < width else width)
            end_y = int(start_y + block_height if start_y + block_height < height else height)
            start_x, start_y = int(start_x), int(start_y)
            block = image.crop((start_x, start_y, end_x, end_y))
            art[row] += translate_block(block)

    return '\n'.join(art)


def main():
    scale = 0.43
    file_path = input('input full file path: ')
    base_name, *_ = os.path.splitext(file_path)
    output_file_path = base_name + '.txt'
    columns = int(input('input number of columns: '))

    with Image.open(file_path).convert('L') as image:  # image = image.convert(mode='L')
        art = sequential_convert(image, columns, scale)

    with open(output_file_path, 'w') as output_file:
        output_file.write(art)
        print('output written to {}'.format(output_file_path))


if __name__ == '__main__':
    main()
