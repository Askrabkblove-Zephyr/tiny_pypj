"""
MIT License

Copyright (c) 2025 Askrabkblove-Zephyr

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from xml.dom.expatbuilder import theDOMImplementation

import requests
from bs4 import BeautifulSoup
import re
import json
import time
import random

# 请求URL
url = "https://forestry.nefu.edu.cn/szdw/jzyg.htm"

# 添加请求头，伪装成浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# 发送HTTP请求
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'  # 明确指定编码，防止乱码

# 使用BeautifulSoup解析HTML内容
soup = BeautifulSoup(response.text, 'html.parser')

# 找到所有包含导师信息的td标签
td_list = soup.find_all('td')
teacher_info_list = []
i = 0
# 遍历所有a标签
for spv_td in td_list:
    spv_a = spv_td.find('a')
        # 找到导师信息所在td标签
    if spv_a and spv_a.get('href'):
        name = spv_a.get_text(strip=True)  # 提取文本并去除首尾空白
        href = spv_a['href']
        print(f"=== 处理导师: {name} ===")

        # 处理相对链接
        if href.startswith('../'):
            href = 'https://forestry.nefu.edu.cn' + href[2:]
        elif href.startswith('/'):
            href = 'https://forestry.nefu.edu.cn' + href

        print(f"详细页面链接: {href}")

        # 发送请求到导师的详细页面
        try:
            teacher_response = requests.get(href, headers=headers, timeout=10)
            teacher_response.encoding = 'utf-8'  # 明确指定编码，防止乱码
            teacher_soup = BeautifulSoup(teacher_response.text, 'html.parser')

            # 初始化导师的其他信息
            spv_phone = ""
            spv_email = ""
            spv_photo = ""
            spv_introduction = "个人简介："
            spv_achievement = ""
            spv_college = "林学院"
            teacher_id = href
            learning_experience = "学习经历："

            # 找到导师照片的URL
            photo_p = teacher_soup.find('p', class_='vsbcontent_img')
            if photo_p:
                photo_img = photo_p.find('img')
                if photo_img and 'src' in photo_img.attrs:
                    photo_src = photo_img['src']
                    if photo_src.startswith('../'):
                        spv_photo = 'https://forestry.nefu.edu.cn' + photo_src[2:]
                    elif photo_src.startswith('/'):
                        spv_photo = 'https://forestry.nefu.edu.cn' + photo_src
                    else:
                        spv_photo = 'https://forestry.nefu.edu.cn' + photo_src

            # 找到导师邮箱信息
            email_p = teacher_soup.find('p', string=re.compile(r'^邮箱：'))
            if email_p:
                email_text = email_p.get_text(strip=True)
                spv_email = email_text.split("：")[1] if "：" in email_text else ""

            # 找到导师电话信息
            phone_p = teacher_soup.find('p', string=re.compile(r'^电话：'))
            if phone_p:
                phone_text = phone_p.get_text(strip=True)
                spv_phone = phone_text.split("：")[1] if "：" in phone_text else ""

            # 找到导师简介信息
            all_paragraphs = teacher_soup.find_all('p')
            for p in all_paragraphs:
                strong_tag = p.find('strong')
                if strong_tag and '个人简介' in strong_tag.get_text():
                    # 获取下一个兄弟p标签
                    next_p = p.find_next_sibling('p')
                    # 循环获取所有连续的内容段落，直到遇到下一个strong标签
                    while next_p and not next_p.find('strong'):
                        content = next_p.get_text(strip=True)
                        # 跳过空内容
                        if content:
                            if spv_introduction:
                                spv_introduction += content
                            else:
                                spv_introduction = content
                        # 移动到下一个兄弟p标签
                        next_p = next_p.find_next_sibling('p')
                    p = next_p
                elif strong_tag and '学习经历' in strong_tag.get_text():
                    # 获取下一个兄弟p标签
                    next_p = p.find_next_sibling('p')
                    # 循环获取所有连续的内容段落，直到遇到下一个strong标签
                    spv_introduction += "学习经历："
                    while next_p and not next_p.find('strong'):
                        content = next_p.get_text(strip=True)
                        # 跳过空内容
                        if content:

                            if spv_introduction:
                                spv_introduction += content
                            else:
                                spv_introduction = content
                        # 移动到下一个兄弟p标签
                        next_p = next_p.find_next_sibling('p')
                elif strong_tag and '工作经历' in strong_tag.get_text():
                    # 获取下一个兄弟p标签
                    next_p = p.find_next_sibling('p')
                    spv_introduction += "工作经历："
                    # 循环获取所有连续的内容段落，直到遇到下一个strong标签
                    while next_p and not next_p.find('strong'):
                        content = next_p.get_text(strip=True)
                        # 跳过空内容
                        if content:
                            if spv_introduction:
                                spv_introduction += content
                            else:
                                spv_introduction = content
                        # 移动到下一个兄弟p标签
                        next_p = next_p.find_next_sibling('p')
                    break
            # 找到代表性成果
            all_paragraphs = teacher_soup.find_all('p')
            for p in all_paragraphs:
                strong_tag = p.find('strong')
                if strong_tag and '代表性成果' in strong_tag.get_text():
                    next_p = p.find_next_sibling('p')
                    continue
                elif strong_tag and '项目' in strong_tag.get_text():
                    # 获取下一个兄弟p标签
                    next_p = p.find_next_sibling('p')
                    spv_achievement += "项目："
                    # 循环获取所有连续的内容段落，直到遇到下一个strong标签
                    while next_p and not next_p.find('strong'):
                        content = next_p.get_text(strip=True)
                        # 跳过空内容
                        if content:
                            if spv_achievement:
                                spv_achievement += content
                            else:
                                spv_achievement = content
                        # 移动到下一个兄弟p标签
                        next_p = next_p.find_next_sibling('p')
                    p = next_p
                elif strong_tag and '论文' in strong_tag.get_text():
                    # 获取下一个兄弟p标签
                    next_p = p.find_next_sibling('p')
                    spv_achievement += "论文："
                    # 循环获取所有连续的内容段落，直到遇到下一个strong标签
                    while next_p and not next_p.find('strong'):
                        content = next_p.get_text(strip=True)
                        # 跳过空内容
                        if content:
                            if spv_achievement:
                                spv_achievement += content
                            else:
                                spv_achievement = content
                        # 移动到下一个兄弟p标签
                        next_p = next_p.find_next_sibling('p')
                    p = next_p
                elif strong_tag and '联系方式' in strong_tag.get_text():
                    # 获取下一个兄弟p标签
                    next_p = p.find_next_sibling('p')
                    spv_achievement += "联系方式："
                    # 循环获取所有连续的内容段落，直到遇到下一个strong标签
                    while next_p and not next_p.find('strong'):
                        content = next_p.get_text(strip=True)
                        # 跳过空内容
                        if content:
                            if spv_achievement:
                                spv_achievement += content
                            else:
                                spv_achievement = content
                        # 移动到下一个兄弟p标签
                        next_p = next_p.find_next_sibling('p')
                    p = next_p
                    break
            # 构建导师的json信息
            teacher_info = {
                "name": name,
                "school": "东北林业大学",
                "college": spv_college,
                "city": "哈尔滨",
                "province": "黑龙江",
                "photo": spv_photo,
                "phone": spv_phone,
                "email": spv_email,
                "url": href,
                "introduction": spv_introduction,
                "achievement": spv_achievement,
                "id": teacher_id
            }

            # 添加到导师信息列表
            teacher_info_list.append(teacher_info)

            print(f"✅ 完成处理: {name}\n")

        except Exception as e:
            print(f"❌ 处理导师 {name} 时出错: {e}")
            continue

        # 随机延迟，避免频繁请求
        time.sleep(random.uniform(1, 3))

# 打印导师信息列表
print("=== 最终结果 ===")
print(json.dumps(teacher_info_list, ensure_ascii=False, indent=2))

# 保存导师信息列表到JSON文件
with open('teachers_info.json', 'w', encoding='utf-8') as json_file:
    json.dump(teacher_info_list, json_file, ensure_ascii=False, indent=2)

print(f"\n✅ 导师信息已保存到 teachers_info.json 文件中，共 {len(teacher_info_list)} 位导师")
