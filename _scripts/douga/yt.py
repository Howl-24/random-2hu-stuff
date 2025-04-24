import argparse
import yt_dlp

# 创建命令行参数解析器
parser = argparse.ArgumentParser(description="使用 yt-dlp 提取播放列表的所有视频信息")
parser.add_argument('url', help='播放列表的 URL')
parser.add_argument('-r', '--reverse', action='store_true', help='倒序生成 Markdown 文件')

# 解析命令行参数
args = parser.parse_args()

# 定义 yt-dlp 配置选项
options = {
    'quiet': True,  # 静默模式，减少不必要的输出
    'extract_flat': True,  # 只提取元数据，不下载视频
}

# 创建一个列表来存储 Markdown 内容
md_content_list = []

# 提取视频信息
with yt_dlp.YoutubeDL(options) as ydl:
    result = ydl.extract_info(args.url, download=False)

    # 遍历顶层的 entries 列表
    for entry in result.get('entries', []):
        # 获取 title 和 url
        title = entry.get('title')
        url = entry.get('url')

        # 如果有 title 和 url，则生成 Markdown 格式
        if title and url:
            md_content_list.append(f"##### [{title}]({url})\n")
        else:
            md_content_list.append("该条目没有找到URL或标题\n")

# 如果传入了 -r 或 --reverse 参数，倒序 Markdown 内容
if args.reverse:
    md_content_list.reverse()

# 将生成的 Markdown 内容写入文件
with open("youtube.md", "w", encoding="utf-8") as md_file:
    md_file.writelines(md_content_list)

# 打印确认信息
print("Markdown 文件已生成：youtube.md")
