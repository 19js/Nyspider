import openpyxl
import os
import json
from util import write_to_excel


def generate_images_html(img_list, title, file_path):
    template = '''
    <html>
        <title>{}</title>
        <body>
            <div>
                <h2>图片列表</h2>
                <ul>
                {}
                </ul>
            </div>
        </body>
    </html>
    '''
    img_list_html = ''
    for img_src in img_list:
        img_list_html += '<li><img src="{}"></li>\r\n'.format(img_src)
    html = template.format(title, img_list_html)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)


def main():
    for dir in ['mafengwo', 'tuniu']:
        html_num = 1
        try:
            os.mkdir(dir+'/images')
        except:
            pass
        result=[]
        for line in open(dir + '/travels.txt', 'r'):
            item = json.loads(line)
            base_info = item['baseinfo']
            content = item['content']
            img_list = item['images']
            title=base_info[0]
            file_path=dir+'/images/%s.html'%html_num
            generate_images_html(img_list,title,file_path)
            html_num+=1
            try:
                row=base_info+[content,'\n'.join([img for img in img_list if img is not None]),file_path]
            except:
                print(line)
                return
            result.append(row)
        write_to_excel(result,dir+'.xlsx')
        print(dir,'OK')
main()
