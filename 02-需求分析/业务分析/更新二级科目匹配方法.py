#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
更新二级科目的匹配方法，改为使用大模型匹配
"""

import pandas as pd
import os

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

# 判断是否为二级或多级科目（编码长度>4或包含层级结构）
def is_multi_level(code):
    """判断是否为多级科目"""
    code_str = str(code) if pd.notna(code) else ''
    # 编码长度大于4位，通常是二级或以上科目
    if len(code_str) > 4:
        return True
    return False

# 更新匹配方法
for idx, row in df.iterrows():
    code = row['科目代码']
    name = row['科目名称'] if pd.notna(row['科目名称']) else ''
    auxiliary = row['辅助核算'] if pd.notna(row['辅助核算']) else ''
    
    # 有辅助核算的科目
    if pd.notna(auxiliary) and str(auxiliary).strip() != '':
        df.at[idx, '匹配方法'] = '智能语义匹配（大模型）'
        df.at[idx, '匹配方法说明'] = '有辅助核算，需要大模型匹配并处理辅助核算映射'
    # 二级及多级科目
    elif is_multi_level(code):
        df.at[idx, '匹配方法'] = '智能语义匹配（大模型）'
        df.at[idx, '匹配方法说明'] = '二级/多级科目，层级和名称可能不完全相同，建议使用大模型进行语义匹配'
    # 一级科目
    else:
        df.at[idx, '匹配方法'] = '传统精确匹配'
        df.at[idx, '匹配方法说明'] = '一级科目，建议使用完全匹配（编码+名称）或编码匹配'

# 保存更新后的CSV文件
output_dir = "04-参考资料/业务文档"
os.makedirs(output_dir, exist_ok=True)

csv_output = os.path.join(output_dir, "小企业会计准则-默认科目.csv")
df.to_csv(csv_output, index=False, encoding='utf-8-sig')
print(f"✅ CSV文件已更新: {csv_output}")

# 统计匹配方法分布
print("\n📊 匹配方法统计:")
match_method_stats = df['匹配方法'].value_counts()
for method, count in match_method_stats.items():
    percentage = (count / len(df) * 100) if len(df) > 0 else 0
    print(f"   {method}: {count} 个科目 ({percentage:.1f}%)")

print(f"\n总计: {len(df)} 个科目")

# 统计二级科目数量
multi_level_count = sum(1 for _, row in df.iterrows() if is_multi_level(row['科目代码']))
print(f"\n二级及多级科目: {multi_level_count} 个")
