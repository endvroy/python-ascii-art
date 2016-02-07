from PIL import Image
import numpy as np
import math, os

scale = 0.43


def translate_block(img):
    a = np.array(img)
    gray_scale = a.mean()
    char_table = " .'`^\",:;Il!i><~+_-?][}{1)(|\\/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    return char_table[int(gray_scale / 255 * (len(char_table) - 1))]


# def get_block_size(image, columns=80, scale=1):
#     width, height = image.size
#     block_width = width / columns
#     block_height = block_width / scale
#     rows = height / block_height
#     return math.ceil(rows)


def main():
    file_path = input('input full file path: ')
    base_name, *_ = os.path.splitext(file_path)
    output_file_path = base_name + '.txt'
    columns = int(input('input number of columns: '))

    with Image.open(file_path).convert('L') as image: # image = image.convert(mode='L')
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

    with open(output_file_path, 'w') as output_file:
        output_file.write('\n'.join(art))
        print('output written to {}'.format(output_file_path))


if __name__ == '__main__':
    main()
