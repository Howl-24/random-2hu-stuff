import re


def generate_toc(md_file, output_file):
    """从 Markdown 文件中提取标题，生成目录（不包含图片，不生成 id，去掉 ## 目录 本身）"""

    def sanitize_link(title):
        """将标题中的特殊符号（如括号）替换为 URL-safe 格式"""
        title = title.lower()  # 转换为小写字母
        title = title.replace("（", "").replace("）", "")  # 去除中文括号（）
        title = (
            title.replace("（", "").replace("）", "").replace(" ", "-")
        )  # 用-代替空格

        return title

    with open(md_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    toc = []
    content = []

    for line in lines:
        match = re.match(r"^(#{1,2})\s+(.*)", line)  # mmd:1,2 douga:3,3 music:1,1
        if match:
            level = len(match.group(1))  # 计算标题级别
            title = match.group(2).strip()

            # 去除图片 `![](url)`
            title_cleaned = re.sub(r"!\[.*?\]\(.*?\)", "", title).strip()

            # 提取 `[文本](URL)` 只保留 "文本" 部分
            title_cleaned = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", title_cleaned).strip()

            # 目录中不包含“目录”本身
            if title_cleaned.lower() != "目录":
                sanitized_title = sanitize_link(title_cleaned)  # 对链接部分进行清理
                toc.append(
                    f"{'  ' * (level - 1)}- [{title_cleaned}](#{sanitized_title})"
                )

        content.append(line)  # 原内容不变

    # 生成目录部分，不包含“## 目录”标题
    if toc:
        toc_section = ["\n".join(toc) + "\n\n"]
        content = toc_section + content

    # 输出到新文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.writelines(content)

    print(f"✅ TOC 生成完成！结果保存在 {output_file}")


# 使用示例
md_input = "D:/Repos/random-2hu-stuff/_mmd/mmd.md"  # _mmd/mmd.md _douga/douga.md _music/music.md
md_output = "toc.md"  # 生成带 TOC 的新文件
generate_toc(md_input, md_output)
