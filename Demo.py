import base64
import os

import markdown
import requests
import html2text
from bs4 import BeautifulSoup
num_img = 1
num = 1
def DownloadExplo(url):
    global num_img
    for img_tag in url:
        img_src = img_tag.get('src')

        if img_src and img_src.startswith('data:image/'):
            img_data = img_src.split(',')[1]
            img_bytes = base64.b64decode(img_data)
            img_name = os.path.join('images', f'image_{num_img}.png')
            num_img = num_img+1
            try:
                # 保存图片
                with open(img_name, 'wb') as f:
                    f.write(img_bytes)
                print(f"下载成功: {img_name}")
            except Exception as e:
                print(f"保存图片失败: {img_name}, 错误: {e}")

def preprocess(lst):
    global num_img
    global num
    for page in lst:
        page = requests.get(page,headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(page.content, 'lxml')
        DownloadExplo(soup.find_all('img'))
        num = execute(soup,num)



def execute(url,num):
    content = []
    for i in url.descendants:
        if i.name =='h1'or i.name =='p':
            content.append(i.text)
        elif i.name =='img':
            content.append('\n![desc](' + f'./images/image_{num}.png' + ')''\n')
            num = num+1
    save_md(content)
    return num

def save_md(content):
    with open(f'./{content[0][:5]}.md', 'w', encoding="utf-8") as f:
        f.writelines(content)
    print(f'成功保存文件{content[0]}')




if __name__ == "__main__":
    if not os.path.exists('./images'):
        os.mkdir('images')
    # 在下方输入你的url列表
    lst = []
    # 从文件读取
    # with open('./ds.txt', 'r', encoding="utf-8") as f:
    #     lst.append(f.readline().strip())
    preprocess(lst)

