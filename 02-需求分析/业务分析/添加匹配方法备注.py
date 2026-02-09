#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为小企业会计准则默认科目添加匹配方法备注
根据科目分类结果，标注每个科目适用的匹配方法
"""

import pandas as pd
import json
import os

# 读取科目分类结果
classification_file = "02-需求分析/功能分析/科目分类结果.json"
with open(classification_file, 'r', encoding='utf-8') as f:
    classifications = json.load(f)

# 读取原始科目数据
excel_file = "小企业会计准则 (1).xlsx"
df = pd.read_excel(excel_file, sheet_name=0, header=0)

# 清理数据：去除表头行
df = df[df['当前版本SAAS的默认科目'] != '编码'].copy()

# 创建匹配方法列
df['匹配方法'] = ''
df['匹配方法说明'] = ''

# 建立科目到分类的映射
subject_to_category = {}
for category, subjects in classifications.items():
    for subj in subjects:
        old_code = subj.get('old_code', '')
        old_name = subj.get('old_name', '')
        key = f"{old_code}_{old_name}"
        subject_to_category[key] = category

# 为每个科目添加匹配方法备注
for idx, row in df.iterrows():
    old_code = row['当前版本SAAS的默认科目']
    old_name = row['Unnamed: 1'] if pd.notna(row['Unnamed: 1']) else ''
    operation = row['操作'] if pd.notna(row['操作']) else ''
    auxiliary = row['辅助'] if pd.notna(row['辅助']) else ''
    has_issue = row['是否有问题'] if pd.notna(row['是否有问题']) else ''
    
    key = f"{old_code}_{old_name}"
    category = subject_to_category.get(key, '')
    
    # 根据分类和属性确定匹配方法
    if category == '传统方法-完全匹配':
        df.at[idx, '匹配方法'] = '传统精确匹配'
        df.at[idx, '匹配方法说明'] = '建议使用完全匹配（编码+名称）或编码匹配'
    elif category == '传统方法-层级匹配':
        df.at[idx, '匹配方法'] = '传统精确匹配'
        df.at[idx, '匹配方法说明'] = '建议使用层级匹配，处理多级科目结构'
    elif category == '其他处理-删除科目':
        df.at[idx, '匹配方法'] = '智能语义匹配'
        df.at[idx, '匹配方法说明'] = '本系统已删除，对方系统可能有此科目，需要智能匹配并建议替代方案'
    elif category == '其他处理-新增科目':
        df.at[idx, '匹配方法'] = '智能语义匹配'
        df.at[idx, '匹配方法说明'] = '本系统新增科目，对方系统可能无此科目，需要智能匹配或创建新科目'
    elif category == '其他处理-辅助核算':
        df.at[idx, '匹配方法'] = '智能语义匹配'
        df.at[idx, '匹配方法说明'] = '有辅助核算，需要额外处理辅助核算映射，建议使用智能匹配'
    elif category == '其他处理-待讨论':
        df.at[idx, '匹配方法'] = '智能语义匹配'
        df.at[idx, '匹配方法说明'] = '待讨论科目，需要人工确认，建议使用智能匹配提供候选'
    else:
        # 默认情况：根据操作类型判断
        if operation == '保持不变':
            df.at[idx, '匹配方法'] = '传统精确匹配'
            df.at[idx, '匹配方法说明'] = '标准科目，建议使用完全匹配或编码匹配'
        elif operation == '删除':
            df.at[idx, '匹配方法'] = '智能语义匹配'
            df.at[idx, '匹配方法说明'] = '已删除科目，需要智能匹配'
        else:
            df.at[idx, '匹配方法'] = '智能语义匹配'
            df.at[idx, '匹配方法说明'] = '需要智能匹配处理'

# 保存更新后的CSV文件
output_dir = "04-参考资料/业务文档"
os.makedirs(output_dir, exist_ok=True)

csv_file = os.path.join(output_dir, "小企业会计准则-默认科目.csv")
df.to_csv(csv_file, index=False, encoding='utf-8-sig')
print(f"✅ CSV文件已更新: {csv_file}")

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
    f.write(f"数据来源: {excel_file} 第一个sheet页\n\n")
    f.write(f"数据行数: {len(df)}\n\n")
    f.write("## 匹配方法说明\n\n")
    f.write("- **传统精确匹配**：适用于标准科目，使用完全匹配、编码匹配或层级匹配\n")
    f.write("- **智能语义匹配**：适用于删除科目、新增科目、有辅助核算的科目等，需要语义理解或特殊处理\n\n")
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
