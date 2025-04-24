from bs4 import BeautifulSoup
import json
import os

# 设置 HTML 文件路径
path = "D:/Repos/random-2hu-stuff/_site/douga/index.html"

# 读取 HTML 文件
with open(path, "r", encoding="utf-8") as file:
    html_content = file.read()

# 解析 HTML
soup = BeautifulSoup(html_content, "html.parser")

# 存储索引数据的列表
index_data = []

# 处理 h3, h4, h5 标签
for tag in soup.find_all(["h1", "h2", "h3", "h4", "h5"]):
    id_attr = tag.get("id", "").strip()  # 获取 id 属性
    if id_attr:  # 仅处理有 id 的标签
        id_attr = f"/douga#{id_attr}"
    if not id_attr or "youtube" in id_attr.lower() or "bilibili" in id_attr.lower():
        continue  # 跳过包含 "youtube" 或 "bilibili" 的 id

    title = tag.get_text(strip=True)  # 获取标题内容
    link_tag = tag.find("a")  # 查找 a 标签
    content = (
        link_tag.get_text(strip=True) if link_tag else title
    )  # 提取 a 标签内文本，否则用标题

    index_data.append({"id": id_attr, "title": title, "content": content})

# 输出 JSON 文件路径
json_path = "D:/Repos/random-2hu-stuff/_scripts/douga/index.json"

# 确保输出目录存在
os.makedirs(os.path.dirname(json_path), exist_ok=True)

# 将数据保存到 JSON 文件
with open(json_path, "w", encoding="utf-8") as json_file:
    json.dump(index_data, json_file, ensure_ascii=False, indent=4)

print(f"索引已生成，保存为 {json_path}")
