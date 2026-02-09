#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据修改后的CSV文件重新生成JSON和MD文件，并重新进行分类分析
"""

import pandas as pd
import json
import os

# 读取修改后的CSV文件
csv_file = "04-参考资料/业务文档/小企业会计准则-默认科目.csv"
df = pd.read_csv(csv_file, encoding='utf-8-sig')

print(f"读取CSV文件: {csv_file}")
print(f"数据形状: {df.shape}")
print(f"列名: {list(df.columns)}")
print(f"\n前5行数据:")
print(df.head())

# 确保输出目录存在
output_dir = "04-参考资料/业务文档"
os.makedirs(output_dir, exist_ok=True)

# 保存为JSON格式
json_file = os.path.join(output_dir, "小企业会计准则-默认科目.json")
data_dict = df.to_dict('records')
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(data_dict, f, ensure_ascii=False, indent=2)
print(f"\n✅ JSON文件已更新: {json_file}")

# 保存为Markdown格式
md_file = os.path.join(output_dir, "小企业会计准则-默认科目.md")
with open(md_file, 'w', encoding='utf-8') as f:
    f.write("# 小企业会计准则 - 默认科目数据\n\n")
    f.write(f"数据来源: {csv_file}\n\n")
    f.write(f"数据行数: {len(df)}\n\n")
    f.write("## 数据表\n\n")
    # 表头
    headers = df.columns.tolist()
    f.write("| " + " | ".join(str(h) for h in headers) + " |\n")
    f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
    # 数据行
    for _, row in df.iterrows():
        f.write("| " + " | ".join(str(val) if pd.notna(val) else "" for val in row) + " |\n")
print(f"✅ Markdown文件已更新: {md_file}")

# 输出数据统计信息
print(f"\n📊 数据统计:")
print(f"   - 总行数: {len(df)}")
print(f"   - 总列数: {len(df.columns)}")
print(f"   - 列名: {', '.join(df.columns)}")
