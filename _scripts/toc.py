import re

def generate_toc(md_file, output_file):
    """从 Markdown 文件中提取标题，生成目录（不包含图片，不生成 id，去掉 ## 目录 本身）"""

    with open(md_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    toc = []
    content = []
    
    for line in lines:
        match = re.match(r'^(#{1,2})\s+(.*)', line)
        if match:
            level = len(match.group(1))  # 计算标题级别
            title = match.group(2).strip()

            # 去除图片 `![](url)`
            title_cleaned = re.sub(r'!\[.*?\]\(.*?\)', '', title).strip()

            # 提取 `[文本](URL)` 只保留 "文本" 部分
            title_cleaned = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', title_cleaned).strip()

            # 目录中不包含“目录”本身
            if title_cleaned.lower() != "目录":
                toc.append(f"{'  ' * (level - 1)}- [{title_cleaned}](#{title_cleaned.replace(' ', '-')})")

        content.append(line)  # 原内容不变

    # 生成目录部分，不包含“## 目录”标题
    if toc:
        toc_section = ["\n".join(toc) + "\n\n"]
        content = toc_section + content

    # 输出到新文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.writelines(content)

    print(f"✅ TOC 生成完成！结果保存在 {output_file}")

# 使用示例
md_input = "mmd.md"   # 你的 Markdown 文件
md_output = "mmd_with_toc.md"  # 生成带 TOC 的新文件
generate_toc(md_input, md_output)
