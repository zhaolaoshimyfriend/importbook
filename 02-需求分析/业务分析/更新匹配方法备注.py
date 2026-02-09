#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据重新分类的结果，更新科目数据文件中的匹配方法备注
"""

import pandas as pd
import json
import os

# 读取科目分类结果
classification_file = "02-需求分析/功能分析/科目分类结果.json"
with open(classification_file, 'r', encoding='utf-8') as f:
    classifications = json.load(f)

# 读取科目数据
csv_file = "04-参考资料/业务文档/小企业会计准则-默认科目.csv"
df = pd.read_csv(csv_file, encoding='utf-8-sig')

# 确保有匹配方法列
if '匹配方法' not in df.columns:
    df['匹配方法'] = ''
else:
    df['匹配方法'] = df['匹配方法'].astype(str)
if '匹配方法说明' not in df.columns:
    df['匹配方法说明'] = ''
else:
    df['匹配方法说明'] = df['匹配方法说明'].astype(str)

# 建立科目到分类的映射
subject_to_category = {}
for category, subjects in classifications.items():
    for subj in subjects:
        code = subj.get('code', '')
        name = subj.get('name', '')
        key = f"{code}_{name}"
        subject_to_category[key] = category

# 为每个科目添加匹配方法备注
for idx, row in df.iterrows():
    code = row['科目代码']
    name = row['科目名称'] if pd.notna(row['科目名称']) else ''
    auxiliary = row['辅助核算'] if pd.notna(row['辅助核算']) else ''
    
    key = f"{code}_{name}"
    category = subject_to_category.get(key, '')
    
    # 根据分类确定匹配方法
    if category == '传统方法-完全匹配':
        df.at[idx, '匹配方法'] = '传统精确匹配'
        df.at[idx, '匹配方法说明'] = '建议使用完全匹配（编码+名称）或编码匹配'
    elif category == '传统方法-层级匹配':
        df.at[idx, '匹配方法'] = '传统精确匹配'
        df.at[idx, '匹配方法说明'] = '建议使用层级匹配，处理多级科目结构'
    elif category == '其他处理-辅助核算':
        df.at[idx, '匹配方法'] = '智能语义匹配'
        df.at[idx, '匹配方法说明'] = '有辅助核算，需要额外处理辅助核算映射，建议使用智能匹配'
    else:
        # 默认情况
        if pd.notna(auxiliary) and str(auxiliary).strip() != '':
            df.at[idx, '匹配方法'] = '智能语义匹配'
            df.at[idx, '匹配方法说明'] = '有辅助核算，需要额外处理辅助核算映射，建议使用智能匹配'
        else:
            code_str = str(code) if pd.notna(code) else ''
            if '.' in code_str or len(code_str) > 4:
                df.at[idx, '匹配方法'] = '传统精确匹配'
                df.at[idx, '匹配方法说明'] = '建议使用层级匹配，处理多级科目结构'
            else:
                df.at[idx, '匹配方法'] = '传统精确匹配'
                df.at[idx, '匹配方法说明'] = '建议使用完全匹配（编码+名称）或编码匹配'

# 保存更新后的CSV文件
output_dir = "04-参考资料/业务文档"
os.makedirs(output_dir, exist_ok=True)

csv_output = os.path.join(output_dir, "小企业会计准则-默认科目.csv")
df.to_csv(csv_output, index=False, encoding='utf-8-sig')
print(f"✅ CSV文件已更新: {csv_output}")

# 保存更新后的JSON文件
json_file = os.path.join(output_dir, "小企业会计准则-默认科目.json")
data_dict = df.to_dict('records')
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(data_dict, f, ensure_ascii=False, indent=2)
print(f"✅ JSON文件已更新: {json_file}")

# 保存更新后的Markdown文件
md_file = os.path.join(output_dir, "小企业会计准则-默认科目.md")
with open(md_file, 'w', encoding='utf-8') as f:
    f.write("# 小企业会计准则 - 默认科目数据（含匹配方法备注）\n\n")
    f.write(f"数据来源: {csv_file}\n\n")
    f.write(f"数据行数: {len(df)}\n\n")
    f.write("## 匹配方法说明\n\n")
    f.write("- **传统精确匹配**：适用于标准科目，使用完全匹配、编码匹配或层级匹配\n")
    f.write("- **智能语义匹配**：适用于有辅助核算的科目等，需要语义理解或特殊处理\n\n")
    f.write("## 数据表\n\n")
    # 表头
    headers = df.columns.tolist()
    f.write("| " + " | ".join(str(h) for h in headers) + " |\n")
    f.write("| " + " | ".join(["---"] * len(headers)) + " |\n")
    # 数据行
    for _, row in df.iterrows():
        f.write("| " + " | ".join(str(val) if pd.notna(val) else "" for val in row) + " |\n")
print(f"✅ Markdown文件已更新: {md_file}")

# 统计匹配方法分布
print("\n📊 匹配方法统计:")
match_method_stats = df['匹配方法'].value_counts()
for method, count in match_method_stats.items():
    percentage = (count / len(df) * 100) if len(df) > 0 else 0
    print(f"   {method}: {count} 个科目 ({percentage:.1f}%)")

print(f"\n总计: {len(df)} 个科目")
