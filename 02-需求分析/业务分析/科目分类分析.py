#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
根据科目映射关系设计场景分析，对默认科目进行分类
确定哪些用传统方法、哪些用模型分析、哪些需要其他处理
"""

import pandas as pd
import json
import os

# 读取数据
csv_file = "04-参考资料/业务文档/小企业会计准则-默认科目.csv"
df = pd.read_excel("小企业会计准则 (1).xlsx", sheet_name=0, header=0)

# 清理数据：去除表头行
df = df[df['当前版本SAAS的默认科目'] != '编码'].copy()

# 初始化分类结果
categories = {
    '传统方法-完全匹配': [],  # 编码和名称都完全一致，标准科目
    '传统方法-编码匹配': [],  # 编码相同但名称可能不同，标准编码体系
    '传统方法-层级匹配': [],  # 有明确层级关系的科目
    '模型分析-语义匹配': [],  # 名称相似但编码不同，需要语义理解
    '模型分析-同义词匹配': [],  # 可能存在同义词的科目
    '其他处理-删除科目': [],  # 已删除的科目，需要特殊处理
    '其他处理-新增科目': [],  # 新增的科目，需要确认
    '其他处理-待讨论': [],  # 需要讨论的科目
    '其他处理-辅助核算': []  # 有辅助核算的科目，需要特殊处理
}

# 分析每个科目
for idx, row in df.iterrows():
    old_code = row['当前版本SAAS的默认科目']
    old_name = row['Unnamed: 1'] if pd.notna(row['Unnamed: 1']) else ''
    new_code = row['修改后SAAS的默认科目'] if pd.notna(row['修改后SAAS的默认科目']) else None
    new_name = row['Unnamed: 3'] if pd.notna(row['Unnamed: 3']) else ''
    operation = row['操作'] if pd.notna(row['操作']) else ''
    remark = row['备注'] if pd.notna(row['备注']) else ''
    has_issue = row['是否有问题'] if pd.notna(row['是否有问题']) else ''
    category = row['类别'] if pd.notna(row['类别']) else ''
    auxiliary = row['辅助'] if pd.notna(row['辅助']) else ''
    
    # 构建科目信息
    subject_info = {
        'old_code': old_code,
        'old_name': old_name,
        'new_code': new_code,
        'new_name': new_name,
        'operation': operation,
        'category': category,
        'auxiliary': auxiliary,
        'remark': remark
    }
    
    # 分类逻辑
    if operation == '删除':
        categories['其他处理-删除科目'].append(subject_info)
    elif operation == '新增' or (pd.isna(old_code) and pd.notna(new_code)):
        categories['其他处理-新增科目'].append(subject_info)
    elif has_issue == '需要讨论' or '待讨论' in str(remark):
        categories['其他处理-待讨论'].append(subject_info)
    elif pd.notna(auxiliary) and str(auxiliary).strip() != '':
        categories['其他处理-辅助核算'].append(subject_info)
    elif operation == '保持不变':
        # 保持不变且编码和名称都一致
        if pd.notna(old_code) and pd.notna(new_code) and old_code == new_code:
            if old_name == new_name:
                # 完全匹配：标准科目，使用传统方法
                categories['传统方法-完全匹配'].append(subject_info)
            else:
                # 编码相同但名称不同，使用传统方法但需要名称映射
                categories['传统方法-编码匹配'].append(subject_info)
        else:
            # 其他保持不变的情况
            categories['传统方法-完全匹配'].append(subject_info)
    else:
        # 检查是否有层级关系（编码包含小数点或层级结构）
        code_str = str(old_code) if pd.notna(old_code) else ''
        if '.' in code_str or len(code_str) > 4:
            categories['传统方法-层级匹配'].append(subject_info)
        else:
            # 默认使用语义匹配
            categories['模型分析-语义匹配'].append(subject_info)

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
    f.write("# 科目分类分析报告\n\n")
    f.write("## 分类依据\n\n")
    f.write("根据《科目映射关系设计场景分析》的结论，对默认科目进行分类：\n\n")
    f.write("1. **传统方法-完全匹配**：编码和名称都完全一致的标准科目\n")
    f.write("2. **传统方法-编码匹配**：编码相同但名称可能不同，使用标准编码体系\n")
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
            f.write("| 原编码 | 原名称 | 新编码 | 新名称 | 操作 | 类别 | 辅助核算 |\n")
            f.write("|--------|--------|--------|--------|------|------|----------|\n")
            for subj in subjects[:50]:  # 只显示前50个
                f.write(f"| {subj['old_code']} | {subj['old_name']} | {subj['new_code']} | {subj['new_name']} | {subj['operation']} | {subj['category']} | {subj['auxiliary']} |\n")
            if len(subjects) > 50:
                f.write(f"\n*（仅显示前50个，共{len(subjects)}个）*\n")
            f.write("\n")

print(f"✅ Markdown报告已保存: {md_file}")
