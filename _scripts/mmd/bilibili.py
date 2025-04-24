import subprocess
import json
import re

output_file = "bilibili.md"

# 先清空 Markdown 文件
open(output_file, "w", encoding="utf-8").close()

# 读取 bilibili.txt，逐行获取每个 URL 及其标记
with open("bilibili.txt", "r", encoding="utf-8") as f:
    url_entries = []
    for line in f:
        line = line.strip()
        if line:  # 确保非空行
            parts = line.split()  # 按空格拆分成两个部分
            url = parts[0]  # URL
            tag = parts[1] if len(parts) > 1 else ""  # 标签，默认为空
            url_entries.append((url, tag))  # 存储 (URL, tag)

# 处理每个 URL，并追加到 Markdown 文件
with open(output_file, "a", encoding="utf-8") as f_out:
    for url, tag in url_entries:
        # 组装命令
        command = ["lux", "-j", url]

        # 执行命令并获取 JSON 输出
        result = subprocess.run(
            command, capture_output=True, text=True, encoding="utf-8"
        )

        try:
            # 解析 JSON 输出
            data = json.loads(result.stdout.strip())

            # 处理 JSON 可能是列表或单个对象
            items = data if isinstance(data, list) else [data]

            for item in items:
                title = item.get("title", "No Title")
                raw_url = item.get("url", "No URL")

                # 仅保留 `/video/BVxxxxxxxxx` 或 `/video/avxxxxxxxxx` 格式，去掉后续所有特殊符号
                match = re.search(
                    r"(https://www\.bilibili\.com/video/(BV[\w\d]+|av[\w\d]+))", raw_url
                )
                clean_url = (
                    match.group(1) if match else raw_url
                )  # 匹配成功就取匹配值，否则保留原始 URL

                # 根据标记选择合适的输出格式
                if tag == "r":
                    suffix = " 暂无翻译\n"
                elif tag == "c":
                    suffix = " CC字幕\n"
                elif tag == "t":
                    suffix = " 中文内嵌\n"
                elif tag == "n":
                    suffix = " 不用翻\n"
                else:
                    suffix = "\n"

                # 判断是否包含“内嵌”或“字幕”
                if "内嵌" in title or "字幕" in title or "熟肉" in title:
                    suffix = " 中文内嵌\n"

                # 写入 Markdown 文件
                f_out.write(f"##### [{title}]({clean_url}){suffix}")

        except json.JSONDecodeError:
            print(f"解析 JSON 失败，跳过该 URL: {url}")

print(f"数据已保存至 {output_file}")
