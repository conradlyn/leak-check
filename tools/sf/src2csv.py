import os
import csv

# 源目录和目标目录
src_dir = 'src_files'
dst_dir = 'csv_files'

os.makedirs(dst_dir, exist_ok=True)

# 源字段顺序和目标字段顺序
src_fields = ['手机号', '收件人', '地址']
dst_fields = ['身份证号', '姓名', '收件人', '昵称', '手机号', '地址', '车辆', '邮箱', 'QQ', 'weibo', '来源ID']

for filename in os.listdir(src_dir):
    src_path = os.path.join(src_dir, filename)
    if not os.path.isfile(src_path):
        continue

    dst_path = os.path.join(dst_dir, filename.rsplit('.', 1)[0] + '.csv')

    line_count = 0
    with open(src_path, 'r', encoding='utf-8') as f_in, \
         open(dst_path, 'w', newline='', encoding='utf-8') as f_out:

        writer = csv.writer(f_out)

        for line in f_in:
            line = line.strip()
            if not line:
                continue

            parts = line.split(',')
            src_dict = {k: '' for k in src_fields}
            for i, val in enumerate(parts):
                if i < len(src_fields):
                    src_dict[src_fields[i]] = val.strip()

            dst_row = [
                '',                          # 身份证号
                '',                          # 姓名
                src_dict.get('收件人', ''),  # 收件人
                '',                          # 昵称
                src_dict.get('手机号', ''),   # 手机号
                src_dict.get('地址', ''),     # 地址
                '',                          # 车辆
                '',                          # 邮箱
                '',                          # QQ
                '',                          # weibo
                '2'                          # 来源ID
            ]

            writer.writerow(dst_row)
            line_count += 1

    print(f"已处理文件: {filename}, 行数: {line_count}")

print("所有文件转换完成，输出目录为 csv_files。")