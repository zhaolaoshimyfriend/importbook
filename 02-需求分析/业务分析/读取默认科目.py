#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
读取默认会计科目Excel文件，持久化为结构化数据
"""

import pandas as pd
import json
import os

# 文件路径
excel_file = "小企业会计准则 (1).xlsx"
output_dir = "04-参考资料/业务文档"

# 读取Excel文件的第一个sheet页
print(f"正在读取文件: {excel_file}")
df = pd.read_excel(excel_file, sheet_name=0, header=0)

print(f"数据形状: {df.shape}")
print(f"列名: {list(df.columns)}")
print(f"\n前5行数据预览:")
print(df.head())

# 确保输出目录存在
os.makedirs(output_dir, exist_ok=True)

# 保存为CSV格式（便于查看和编辑）
csv_file = os.path.join(output_dir, "小企业会计准则-默认科目.csv")
df.to_csv(csv_file, index=False, encoding='utf-8-sig')
print(f"\n✅ CSV文件已保存: {csv_file}")

# 保存为JSON格式（便于程序读取）
json_file = os.path.join(output_dir, "小企业会计准则-默认科目.json")
# 将DataFrame转换为字典列表
data_dict = df.to_dict('records')
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(data_dict, f, ensure_ascii=False, indent=2)
print(f"✅ JSON文件已保存: {json_file}")

# 保存为Markdown表格格式（便于文档查看）
md_file = os.path.join(output_dir, "小企业会计准则-默认科目.md")
with open(md_file, 'w', encoding='utf-8') as f:
    f.write("# 小企业会计准则 - 默认科目数据\n\n")
    f.write(f"数据来源: {excel_file} 第一个sheet页\n\n")
    f.write(f"数据行数: {len(df)}\n\n")
    f.write("## 数据表\n\n")
    # 手动生成Markdown表格
    # 表头
    headers = df.columns.tolist()
    f.write("| " + " | ".join(str(h) for h in headers) + " |\n")
    f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
    # 数据行
    for _, row in df.iterrows():
        f.write("| " + " | ".join(str(val) if pd.notna(val) else "" for val in row) + " |\n")
print(f"✅ Markdown文件已保存: {md_file}")

# 输出数据统计信息
print(f"\n📊 数据统计:")
print(f"   - 总行数: {len(df)}")
print(f"   - 总列数: {len(df.columns)}")
print(f"   - 列名: {', '.join(df.columns)}")
