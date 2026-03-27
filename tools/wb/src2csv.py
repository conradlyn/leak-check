import os
import csv
import re

src_dir = 'src_files'
dst_dir = 'csv_files'
os.makedirs(dst_dir, exist_ok=True)

# 校验规则
phone_pattern = re.compile(r'^1\d{10}$')  # 国内手机号 11 位
uid_pattern = re.compile(r'^\d+$')        # UID 全数字

chunk_size = 10_000_000  # 每个输出文件 1000 万行

for filename in os.listdir(src_dir):
    src_path = os.path.join(src_dir, filename)
    if not os.path.isfile(src_path):
        continue

    output_rows = []
    file_index = 1
    total_valid = 0
    phone_errors = 0
    uid_errors = 0

    def write_chunk(rows, idx):
        if not rows:
            return
        out_path = os.path.join(dst_dir, f"{filename.rsplit('.',1)[0]}_{idx}.csv")
        with open(out_path, 'w', newline='', encoding='utf-8') as f_out:
            writer = csv.writer(f_out)
            writer.writerows(rows)
        print(f"[INFO] 已输出文件: {out_path}, 行数: {len(rows)}")

    with open(src_path, 'r', encoding='utf-8', errors='ignore') as f_in:
        for line_number, line in enumerate(f_in, start=1):
            line = line.strip()
            if not line:
                continue

            # 支持制表符、逗号或空格分隔
            parts = re.split(r'\t|,|\s+', line)
            if len(parts) < 2:
                continue

            phone, uid = parts[0].strip(), parts[1].strip()

            # 校验
            if not phone_pattern.match(phone):
                phone_errors += 1
                if phone_errors % 10000 == 0:  # 每 10000 个报错输出一次
                    print(f"[WARN] 手机号校验失败累计: {phone_errors}")
                continue

            if not uid_pattern.match(uid):
                uid_errors += 1
                if uid_errors % 10000 == 0:
                    print(f"[WARN] UID校验失败累计: {uid_errors}")
                continue

            # 构建目标行
            dst_row = [
                '',       # 身份证号
                '',       # 姓名
                '',       # 收件人
                '',       # 昵称
                phone,    # 手机号
                '',       # 地址
                '',       # 车辆
                '',       # 邮箱
                '',       # QQ
                uid,      # weibo
                '3'       # 来源ID
            ]

            output_rows.append(dst_row)
            total_valid += 1

            # 达到 chunk_size 写文件
            if len(output_rows) >= chunk_size:
                write_chunk(output_rows, file_index)
                output_rows = []
                file_index += 1

    # 写剩余行
    if output_rows:
        write_chunk(output_rows, file_index)

    print(f"[INFO] 文件 {filename} 处理完成")
    print(f"[INFO] 合法行总数: {total_valid}, 手机号错误: {phone_errors}, UID错误: {uid_errors}")

print("所有文件处理完成。")