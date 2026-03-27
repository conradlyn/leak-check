import os
import csv
import re

# 输入文件（你自己改路径）
src_file = 'src_files/qq.txt'

# 输出目录
dst_dir = 'csv_files'
os.makedirs(dst_dir, exist_ok=True)

# 常量
CHUNK_SIZE = 10_000_000
SOURCE_ID = '8'

# 正则
qq_pattern = re.compile(r'^\d{5,11}$')
phone_pattern = re.compile(r'^1\d{10}$')

# ========================
# 基础清洗
# ========================
def clean_base(val):
    if not val:
        return ''
    return str(val).replace('\t', '').replace('\n', '').replace('\r', '').strip()

# ========================
# 校验
# ========================
def is_valid_qq(qq):
    return bool(qq_pattern.match(qq))

def is_valid_phone(phone):
    return bool(phone_pattern.match(phone))

# ========================
# 初始化
# ========================
file_index = 1
valid_count = 0
skipped_count = 0

current_chunk_count = 0

def open_new_file(idx):
    path = os.path.join(dst_dir, f'output_{idx}.csv')
    f = open(path, 'w', newline='', encoding='utf-8')
    writer = csv.writer(f)
    return f, writer, path

f_out, writer, current_path = open_new_file(file_index)

print(f"[INFO] 开始处理文件: {src_file}")

# ========================
# 主处理逻辑（流式）
# ========================
with open(src_file, 'r', encoding='utf-8', errors='ignore') as f_in:
    for line in f_in:
        line = clean_base(line)
        if not line:
            skipped_count += 1
            continue

        parts = line.split('----')

        # ========================
        # 情况1：一个分隔符
        # ========================
        if len(parts) == 2:
            qq = clean_base(parts[0])
            phone = clean_base(parts[1])

            if not (is_valid_qq(qq) and is_valid_phone(phone)):
                skipped_count += 1
                continue

            dst_row = [
                None, None, None, None,
                phone,
                None, None, None,
                qq,
                None, None, None,
                SOURCE_ID
            ]

            writer.writerow(dst_row)
            valid_count += 1
            current_chunk_count += 1

        # ========================
        # 情况2：两个分隔符
        # ========================
        elif len(parts) == 3:
            qq1 = clean_base(parts[0])
            qq2 = clean_base(parts[1])
            phone = clean_base(parts[2])

            # 必须全部合法，否则整行丢弃
            if not (is_valid_phone(phone) and is_valid_qq(qq1) and is_valid_qq(qq2)):
                skipped_count += 1
                continue

            for qq in (qq1, qq2):
                dst_row = [
                    None, None, None, None,
                    phone,
                    None, None, None,
                    qq,
                    None, None, None,
                    SOURCE_ID
                ]

                writer.writerow(dst_row)
                valid_count += 1
                current_chunk_count += 1

        # ========================
        # 其他情况
        # ========================
        else:
            skipped_count += 1
            continue

        # ========================
        # 分块输出（1000万）
        # ========================
        if current_chunk_count >= CHUNK_SIZE:
            f_out.close()

            print(f"[INFO] 输出文件: {current_path}")
            print(f"[INFO] 本批有效数据: {current_chunk_count}")
            print(f"[INFO] 累计跳过数据: {skipped_count}")
            print("-" * 50)

            file_index += 1
            current_chunk_count = 0

            f_out, writer, current_path = open_new_file(file_index)

# ========================
# 收尾
# ========================
f_out.close()

print(f"[INFO] 最终输出文件: {current_path}")
print(f"[INFO] 最后一批有效数据: {current_chunk_count}")
print(f"[INFO] 总有效数据: {valid_count}")
print(f"[INFO] 总跳过数据: {skipped_count}")
print("处理完成")