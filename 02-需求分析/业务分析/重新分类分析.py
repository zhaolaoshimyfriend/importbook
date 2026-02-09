#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据修改后的科目数据重新进行分类分析
"""

import pandas as pd
import json
import os

# 读取科目数据
csv_file = "04-参考资料/业务文档/小企业会计准则-默认科目.csv"
df = pd.read_csv(csv_file, encoding='utf-8-sig')

# 初始化分类结果
categories = {
    '传统方法-完全匹配': [],
    '传统方法-编码匹配': [],
    '传统方法-层级匹配': [],
    '模型分析-语义匹配': [],
    '模型分析-同义词匹配': [],
    '其他处理-删除科目': [],
    '其他处理-新增科目': [],
    '其他处理-待讨论': [],
    '其他处理-辅助核算': []
}

# 分析每个科目
for idx, row in df.iterrows():
    code = row['科目代码'] if pd.notna(row['科目代码']) else ''
    name = row['科目名称'] if pd.notna(row['科目名称']) else ''
    category_type = row['类别'] if pd.notna(row['类别']) else ''
    auxiliary = row['辅助核算'] if pd.notna(row['辅助核算']) else ''
    
    # 构建科目信息
    subject_info = {
        'code': code,
        'name': name,
        'category': category_type,
        'auxiliary': auxiliary,
        'debit_credit': row.get('借贷', ''),
    }
    
    # 分类逻辑
    if pd.notna(auxiliary) and str(auxiliary).strip() != '':
        categories['其他处理-辅助核算'].append(subject_info)
    else:
        # 检查是否有层级关系（编码包含小数点或层级结构）
        code_str = str(code) if pd.notna(code) else ''
        if '.' in code_str or len(code_str) > 4:
            categories['传统方法-层级匹配'].append(subject_info)
        else:
            # 标准科目，使用传统精确匹配
            categories['传统方法-完全匹配'].append(subject_info)

# 统计结果
print("=" * 60)
print("科目分类统计")
print("=" * 60)
for category, subjects in categories.items():
    print(f"{category}: {len(subjects)} 个科目")

# 保存分类结果
output_dir = "02-需求分析/功能分析"
os.makedirs(output_dir, exist_ok=True)

# 保存为JSON
json_file = os.path.join(output_dir, "科目分类结果.json")
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(categories, f, ensure_ascii=False, indent=2)
print(f"\n✅ JSON文件已保存: {json_file}")

# 保存为Markdown文档
md_file = os.path.join(output_dir, "科目分类分析报告.md")
with open(md_file, 'w', encoding='utf-8') as f:
    f.write("# 科目分类分析报告（更新版）\n\n")
    f.write("## 分类依据\n\n")
    f.write("根据科目特征进行分类：\n\n")
    f.write("1. **传统方法-完全匹配**：标准科目，编码和名称都完全一致\n")
    f.write("2. **传统方法-编码匹配**：编码相同但名称可能不同\n")
    f.write("3. **传统方法-层级匹配**：有明确层级关系的科目\n")
    f.write("4. **模型分析-语义匹配**：名称相似但编码不同，需要语义理解\n")
    f.write("5. **模型分析-同义词匹配**：可能存在同义词的科目\n")
    f.write("6. **其他处理-删除科目**：已删除的科目，需要特殊处理\n")
    f.write("7. **其他处理-新增科目**：新增的科目，需要确认\n")
    f.write("8. **其他处理-待讨论**：需要讨论的科目\n")
    f.write("9. **其他处理-辅助核算**：有辅助核算的科目，需要特殊处理\n\n")
    
    f.write("## 分类统计\n\n")
    f.write("| 分类 | 数量 | 占比 |\n")
    f.write("|------|------|------|\n")
    total = sum(len(subjects) for subjects in categories.values())
    for category, subjects in categories.items():
        count = len(subjects)
        percentage = (count / total * 100) if total > 0 else 0
        f.write(f"| {category} | {count} | {percentage:.1f}% |\n")
    
    f.write(f"\n**总计**: {total} 个科目\n\n")
    
    # 详细列表
    for category, subjects in categories.items():
        if len(subjects) > 0:
            f.write(f"## {category}\n\n")
            f.write(f"共 {len(subjects)} 个科目\n\n")
            f.write("| 科目代码 | 科目名称 | 类别 | 辅助核算 |\n")
            f.write("|----------|----------|------|----------|\n")
            for subj in subjects[:50]:  # 只显示前50个
                f.write(f"| {subj['code']} | {subj['name']} | {subj['category']} | {subj['auxiliary']} |\n")
            if len(subjects) > 50:
                f.write(f"\n*（仅显示前50个，共{len(subjects)}个）*\n")
            f.write("\n")

print(f"✅ Markdown报告已保存: {md_file}")
