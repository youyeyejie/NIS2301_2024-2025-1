import os
import re

# 获取当前目录
root_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ppt_directory = os.path.join(root_directory, 'Zhang\'s ppt')
current_directories = [ppt_directory]

def convert_chinese_to_arabic(chinese_number):
    chinese_to_arabic_map = {
        '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
        '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
        '百': 100
    }
    result = 0
    temp = 0
    for char in chinese_number:
        if char in chinese_to_arabic_map:
            num = chinese_to_arabic_map[char]
            if num == 10 or num == 100:  # 处理“十”或“百”
                if temp == 0:
                    temp = 1
                result += temp * num
                temp = 0
            else:
                temp = num
    result += temp
    return result

# 遍历当前目录下的文件
for current_directory in current_directories:
    for filename in os.listdir(current_directory):
        old_path = os.path.join(current_directory, filename)
        if os.path.isfile(old_path):
            # 使用正则表达式提取并修改文件名
            match = re.search(r'第([一二三四五六七八九十百]+)章(?:第([一二三四五六七八九十百]+)节)?', filename)
            if match:
                chapter = convert_chinese_to_arabic(match.group(1))
                section = match.group(2)
                if section:
                    section = convert_chinese_to_arabic(section)
                    new_filename = re.sub(r".*第[一二三四五六七八九十百]+章(?:第[一二三四五六七八九十百]+节)\-?", f"Ch{chapter}.{section}_", filename)
                else:
                    new_filename = f"Ch{chapter}_" + re.sub(r'.*第[一二三四五六七八九十百]+章\-', '', filename)

                new_path = os.path.join(current_directory, new_filename)
                os.rename(old_path, new_path)
                print(f"重命名: {filename} -> {new_filename}")