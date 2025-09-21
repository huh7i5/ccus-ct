#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os

def clean_ccus_data(input_file, output_file):
    """
    清洗CCUS数据，去除无意义的网址、特殊字符和格式符号
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 去除行号前缀 (如: "1→", "2→" 等)
    content = re.sub(r'^\s*\d+→', '', content, flags=re.MULTILINE)

    # 去除特殊字符和格式符号
    content = re.sub(r'[檲櫅]+', '', content)
    content = re.sub(r'[Ｖｏｌ．Ｎｏ．]+', '', content)
    content = re.sub(r'[０１２３４５６７８９]+', lambda m: ''.join(str(ord(c) - ord('０')) for c in m.group()), content)
    content = re.sub(r'[ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺ]+',
                     lambda m: ''.join(chr(ord(c) - ord('Ａ') + ord('A')) for c in m.group()), content)

    # 去除URL链接
    content = re.sub(r'https?://[^\s\]]+', '', content)
    content = re.sub(r'www\.[^\s\]]+', '', content)

    # 去除邮箱地址
    content = re.sub(r'\S+@\S+\.\S+', '', content)

    # 去除文档错误信息
    content = re.sub(r'处理\s+\d+\.pdf\s+时出错:错误:\s*document\s+closed', '', content)
    content = re.sub(r'=+\s*新文档\s*=+', '', content)

    # 去除页码和文档标题重复
    content = re.sub(r'中　国　地　质　调　查', '中国地质调查', content)
    content = re.sub(r'郭建强等：中国二氧化碳地质储存潜力评价与示范工程', '', content)

    # 清理多余空白字符
    content = re.sub(r'\s+', ' ', content)
    content = re.sub(r'\n\s*\n', '\n', content)

    # 去除过短的行（可能是噪声）
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        if len(line) > 10 and not re.match(r'^[0-9\s\-=]+$', line):
            cleaned_lines.append(line)

    # 合并相关句子
    merged_content = []
    current_paragraph = ""

    for line in cleaned_lines:
        if line.endswith(('。', '；', '：', '！', '？', '.', ';', ':', '!', '?')):
            current_paragraph += line
            if len(current_paragraph) > 50:  # 只保留有意义的段落
                merged_content.append(current_paragraph)
            current_paragraph = ""
        else:
            current_paragraph += line

    # 添加最后一段
    if current_paragraph and len(current_paragraph) > 50:
        merged_content.append(current_paragraph)

    # 保存清洗后的数据
    with open(output_file, 'w', encoding='utf-8') as f:
        for paragraph in merged_content:
            f.write(paragraph + '\n\n')

    print(f"数据清洗完成!")
    print(f"原始数据行数: {len(lines)}")
    print(f"清洗后段落数: {len(merged_content)}")
    return merged_content

if __name__ == "__main__":
    input_file = "/root/KnowledgeGraph-based-on-Raw-text-A27-main/KnowledgeGraph-based-on-Raw-text-A27-main/data/raw_data_ccus.txt"
    output_file = "/root/KnowledgeGraph-based-on-Raw-text-A27-main/KnowledgeGraph-based-on-Raw-text-A27-main/data/cleaned_ccus_data.txt"

    clean_ccus_data(input_file, output_file)