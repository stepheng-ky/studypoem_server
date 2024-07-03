# 将文件格式化

# 定义需要换行的标点符号集合
PUNCTUATION = set("，。！？；：「」『』（）【】《》〕")


def split_by_punctuation(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile, \
            open(output_file, 'w', encoding='utf-8') as outfile:

        line = infile.readline()
        while line:
            for char in line:
                if char in PUNCTUATION:
                    outfile.write(char + '\n')  # 写入标点并换行
                elif char != '\\' and char != 'n':
                    outfile.write(char)
            # 写入原始行的换行符（如果有）
            # outfile.write(line.rstrip('\n') + '\n')
            line = infile.readline()



#
for i in range(1,9035):
    # 使用示例
    input_filename = f'./poems_file/{i}.txt'  # 原始文件名
    output_filename = f'./poems_file_fmt/{i}.txt'  # 新文件名
    split_by_punctuation(input_filename, output_filename)