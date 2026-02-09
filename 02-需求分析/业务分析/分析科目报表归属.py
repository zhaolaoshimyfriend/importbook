#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分析科目在资产负债表和利润表中的使用情况
基于小企业会计准则的科目分类规则
"""

import pandas as pd
import os

# 读取科目数据
csv_file = "04-参考资料/业务文档/小企业会计准则-默认科目.csv"
df = pd.read_csv(csv_file, encoding='utf-8-sig')

# 添加报表归属列
if '资产负债表' not in df.columns:
    df['资产负债表'] = ''
if '利润表' not in df.columns:
    df['利润表'] = ''
if '报表归属说明' not in df.columns:
    df['报表归属说明'] = ''

# 根据科目类别和性质判断报表归属
for idx, row in df.iterrows():
    category = str(row['类别']) if pd.notna(row['类别']) else ''
    code = str(row['科目代码']) if pd.notna(row['科目代码']) else ''
    name = str(row['科目名称']) if pd.notna(row['科目名称']) else ''
    debit_credit = str(row['借贷']) if pd.notna(row['借贷']) else ''
    
    # 资产负债表科目：资产、负债、权益类
    # 利润表科目：收入、费用类（成本、损益）
    balance_sheet = False
    profit_sheet = False
    explanation = ''
    
    if category == '资产':
        balance_sheet = True
        explanation = '资产类科目，用于资产负债表'
    elif category == '负债':
        balance_sheet = True
        explanation = '负债类科目，用于资产负债表'
    elif category == '权益':
        balance_sheet = True
        explanation = '所有者权益类科目，用于资产负债表'
    elif category == '成本':
        # 成本类科目：生产成本、制造费用等，期末转入存货，影响资产负债表
        # 但成本本身在利润表中体现（主营业务成本）
        balance_sheet = True  # 通过存货影响资产负债表
        profit_sheet = True   # 通过主营业务成本影响利润表
        explanation = '成本类科目，通过存货影响资产负债表，通过主营业务成本影响利润表'
    elif category == '损益':
        # 损益类科目：收入、费用
        profit_sheet = True
        if '收入' in name or code.startswith('5'):
            explanation = '收入类科目，用于利润表'
        elif '费用' in name or '成本' in name or code.startswith('56') or code.startswith('57') or code.startswith('58'):
            explanation = '费用类科目，用于利润表'
        else:
            explanation = '损益类科目，用于利润表'
    
    # 特殊科目处理
    # 本年利润、利润分配等权益类科目，既影响资产负债表也影响利润表
    if code in ['3103', '3104'] or '利润' in name:
        balance_sheet = True
        profit_sheet = True
        explanation = '利润相关科目，既影响资产负债表（权益）也影响利润表（净利润）'
    
    # 设置标记
    df.at[idx, '资产负债表'] = '是' if balance_sheet else '否'
    df.at[idx, '利润表'] = '是' if profit_sheet else '否'
    df.at[idx, '报表归属说明'] = explanation

# 保存更新后的CSV文件
output_dir = "04-参考资料/业务文档"
os.makedirs(output_dir, exist_ok=True)

csv_output = os.path.join(output_dir, "小企业会计准则-默认科目.csv")
df.to_csv(csv_output, index=False, encoding='utf-8-sig')
print(f"✅ CSV文件已更新: {csv_output}")

# 统计报表归属
balance_sheet_count = len(df[df['资产负债表'] == '是'])
profit_sheet_count = len(df[df['利润表'] == '是'])
both_count = len(df[(df['资产负债表'] == '是') & (df['利润表'] == '是')])

print(f"\n📊 报表归属统计:")
print(f"   - 资产负债表科目: {balance_sheet_count} 个")
print(f"   - 利润表科目: {profit_sheet_count} 个")
print(f"   - 同时影响两个报表: {both_count} 个")
print(f"   - 总计: {len(df)} 个科目")

# 显示各类别的统计
print(f"\n📋 按类别统计:")
for category in df['类别'].unique():
    if pd.notna(category):
        cat_df = df[df['类别'] == category]
        balance = len(cat_df[cat_df['资产负债表'] == '是'])
        profit = len(cat_df[cat_df['利润表'] == '是'])
        print(f"   {category}: {len(cat_df)}个科目 (资产负债表:{balance}, 利润表:{profit})")
