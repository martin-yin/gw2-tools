import requests
from bs4 import BeautifulSoup

# 读取本地HTML文件
with open('./1.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

list = []
# 解析HTML内容
soup = BeautifulSoup(html_content, 'html.parser')

# 查找 class 为 sortable 的表格
table = soup.find('table', class_='sortable')

if table:
    # 提取表头
    headers = [header.text.strip() for header in table.find_all('th')]

    # 遍历表格中的每一行
    for row_index, row in enumerate(table.find_all('tr')[1:], start=1):
        Objective = ""
        Map = ""
        Location = ""
        Closest_landmark = ""
        Game_link = ""
        Notes = ""
        for col_index, col in enumerate(row.find_all('td'), start=1):
            header = headers[col_index - 1]
            if header == "Objective":
                Objective = col.text.strip()
            if header == "Map":
                img_src = col.find('img')['src']
                Map = "https://wiki.guildwars2.com/" + img_src
            if header == "Location":
                img_src = col.find('img')['src']
                Location = "https://wiki.guildwars2.com/" + img_src
            if header == "Closest landmark":
                a_tag = col.find_all('a')[1]

                # span_tag = 
                # 找 class gamelink 的span标签
                span_tag = col.find('span', class_='gamelink')
                Game_link = span_tag.text.strip()
                Closest_landmark  = a_tag.text.strip()
            if header == "Notes":
                Notes = col.text.strip()
        list.append({
            "Objective": Objective,
            "Map": Map,
            "Location": Location,
            "Closest landmark": Closest_landmark,
            "Game_link": Game_link,
            "Notes":Notes  
        })
            
    # 格式化成json
    import json
    with open('spa.json', 'w', encoding='utf-8') as f:
        json.dump(list, f, ensure_ascii=False, indent=4)
else:
    print("未找到 class 为 sortable 的表格")
