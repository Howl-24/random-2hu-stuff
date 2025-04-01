import subprocess
import json

output_file = "youtube.md"

# 读取 b.txt，逐行获取每个 URL
with open('b.txt', 'r', encoding='utf-8') as f:
    urls = [line.strip() for line in f if line.strip()]  # 去除空行和首尾空格

# 处理每个 URL，并追加到 Markdown 文件
with open(output_file, 'a', encoding='utf-8') as f_out:
    for url in urls:
        # 组装命令
        command = ['lux', '-j', url]
        
        # 执行命令并获取 JSON 输出
        result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')

        try:
            # 解析 JSON 输出
            data = json.loads(result.stdout.strip())

            # 处理 JSON 可能是列表或单个对象
            if isinstance(data, list):
                for item in data:
                    f_out.write(f"[{item.get('title', 'No Title')}]({item.get('url', 'No URL')}) <br>\n")
            else:
                f_out.write(f"[{data.get('title', 'No Title')}]({data.get('url', 'No URL')}) <br>\n")

        except json.JSONDecodeError:
            print(f"解析 JSON 失败，跳过该 URL: {url}")

print(f"数据已保存至 {output_file}")
