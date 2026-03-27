#!/bin/bash

DB_FILE="../../db/macOS.db"
CSV_DIR="csv_files"

# 打印开始
echo "Starting batch import into $DB_FILE ..."

# 创建临时 SQL 文件用于性能优化
TMP_SQL=$(mktemp)

cat <<EOF > $TMP_SQL
PRAGMA foreign_keys = OFF;
PRAGMA synchronous = OFF;
PRAGMA journal_mode = MEMORY;
BEGIN TRANSACTION;
EOF

# 批量导入 CSV 文件
for csv_file in "$CSV_DIR"/*.csv; do
    if [[ -f "$csv_file" ]]; then
        echo "Importing $csv_file ..."
        echo ".mode csv" >> $TMP_SQL
        echo ".import $csv_file person" >> $TMP_SQL
    fi
done

# 提交事务并恢复设置
cat <<EOF >> $TMP_SQL
COMMIT;
PRAGMA journal_mode = DELETE;
PRAGMA synchronous = FULL;
EOF

# 执行 SQL
sqlite3 "$DB_FILE" < $TMP_SQL

# 删除临时文件
rm $TMP_SQL

echo "All CSV files imported successfully."