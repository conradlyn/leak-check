#!/bin/bash

# 定义总库和子库路径
TOTAL_DB="leak-check.db"
SUB_DB="macOS.db"

sqlite3 "$TOTAL_DB" <<SQL
-- 开启事务，提高大数据量插入性能
BEGIN TRANSACTION;

-- 附加子库
ATTACH '$SUB_DB' AS mac;

-- 插入子库的所有数据到总库
INSERT INTO person
SELECT * FROM mac.person;

-- 提交事务
COMMIT;

-- 分离子库
DETACH mac;
SQL

echo "导入完成: 子库 $SUB_DB 的 person 表已合并到总库 $TOTAL_DB"