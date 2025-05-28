import argparse
import yt_dlp
import json
import os

# 创建命令行参数解析器
parser = argparse.ArgumentParser(description="使用 yt-dlp 提取播放列表或作者视频信息")
parser.add_argument('url_or_json', help='播放列表或作者主页的 URL')
parser.add_argument('-r', '--reverse', action='store_true', help='倒序生成 Markdown 文件')

# 解析命令行参数
args = parser.parse_args()

# 创建一个列表来存储 Markdown 内容
md_content_list = []

def extract_entries(entries, md_content_list):
    for entry in entries:
        # 如果entry本身还有entries字段，递归处理
        if 'entries' in entry and isinstance(entry['entries'], list):
            extract_entries(entry['entries'], md_content_list)
        else:
            title = entry.get('title')
            url = entry.get('url')
            if url and not url.startswith('http'):
                url = f"https://www.youtube.com/watch?v={url}"
            if title and url:
                md_content_list.append(f"#### [{title}]({url})\n")
            else:
                md_content_list.append("该条目没有找到URL或标题\n")

options = {
    'quiet': True,
    'extract_flat': True,
}
with yt_dlp.YoutubeDL(options) as ydl:
    result = ydl.extract_info(args.url_or_json, download=False)
    extract_entries(result.get('entries', []), md_content_list)

# 如果传入了 -r 或 --reverse 参数，倒序 Markdown 内容
if args.reverse:
    md_content_list.reverse()

# 将生成的 Markdown 内容写入文件
with open("youtube.md", "w", encoding="utf-8") as md_file:
    md_file.writelines(md_content_list)

# 打印确认信息
print("Markdown 文件已生成：youtube.md")
