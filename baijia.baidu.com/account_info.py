from util import *
from bs4 import BeautifulSoup
import json
import time
import re

last_names = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
              '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
              '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
              '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
              '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
              '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
              '熊', '纪', '舒', '屈', '项', '祝', '董', '梁']

first_names = ['的', '一', '是', '了', '我', '不', '人', '在', '他', '有', '这', '个', '上', '们', '来', '到', '时', '大', '地', '为',
               '子', '中', '你', '说', '生', '国', '年', '着', '就', '那', '和', '要', '她', '出', '也', '得', '里', '后', '自', '以',
               '会', '家', '可', '下', '而', '过', '天', '去', '能', '对', '小', '多', '然', '于', '心', '学', '么', '之', '都', '好',
               '看', '起', '发', '当', '没', '成', '只', '如', '事', '把', '还', '用', '第', '样', '道', '想', '作', '种', '开', '美',
               '总', '从', '无', '情', '己', '面', '最', '女', '但', '现', '前', '些', '所', '同', '日', '手', '又', '行', '意', '动',
               '方', '期', '它', '头', '经', '长', '儿', '回', '位', '分', '爱', '老', '因', '很', '给', '名', '法', '间', '斯', '知',
               '世', '什', '两', '次', '使', '身', '者', '被', '高', '已', '亲', '其', '进', '此', '话', '常', '与', '活', '正', '感',
               '见', '明', '问', '力', '理', '尔', '点', '文', '几', '定', '本', '公', '特', '做', '外', '孩', '相', '西', '果', '走',
               '将', '月', '十', '实', '向', '声', '车', '全', '信', '重', '三', '机', '工', '物', '气', '每', '并', '别', '真', '打',
               '太', '新', '比', '才', '便', '夫', '再', '书', '部', '水', '像', '眼', '等', '体', '却', '加', '电', '主', '界', '门',
               '利', '海', '受', '听', '表', '德', '少', '克', '代', '员', '许', '稜', '先', '口', '由', '死', '安', '写', '性', '马',
               '光', '白', '或', '住', '难', '望', '教', '命', '花', '结', '乐', '色', '更', '拉', '东', '神', '记', '处', '让', '母',
               '父', '应', '直', '字', '场', '平', '报', '友', '关', '放', '至', '张', '认', '接', '告', '入', '笑', '内', '英', '军',
               '候', '民', '岁', '往', '何', '度', '山', '觉', '路', '带', '万', '男', '边', '风', '解', '叫', '任', '金', '快', '原',
               '吃', '妈', '变', '通', '师', '立', '象', '数', '四', '失', '满', '战', '远', '格', '士', '音', '轻', '目', '条', '呢',
               '病', '始', '达', '深', '完', '今', '提', '求', '清', '王', '化', '空', '业', '思', '切', '怎', '非', '找', '片', '罗',
               '钱', '紶', '吗', '语', '元', '喜', '曾', '离', '飞', '科', '言', '干', '流', '欢', '约', '各', '即', '指', '合', '反',
               '题', '必', '该', '论', '交', '终', '林', '请', '医', '晚', '制', '球', '决', '窢', '传', '画', '保', '读', '运', '及',
               '则', '房', '早', '院', '量', '苦', '火', '布', '品', '近', '坐', '产', '答', '星', '精', '视', '五', '连', '司', '巴',
               '奇', '管', '类', '未', '朋', '且', '婚', '台', '夜', '青', '北', '队', '久', '乎', '越', '观', '落', '尽', '形', '影',
               '红', '爸', '百', '令', '周', '吧', '识', '步', '希', '亚', '术', '留', '市', '半', '热', '送', '兴', '造', '谈', '容',
               '极', '随', '演', '收', '首', '根', '讲', '整', '式', '取', '照', '办', '强', '石', '古', '华', '諣', '拿', '计', '您',
               '装', '似', '足', '双', '妻', '尼', '转', '诉', '米', '称', '丽', '客', '南', '领', '节', '衣', '站', '黑', '刻', '统',
               '断', '福', '城', '故', '历', '惊', '脸', '选', '包', '紧', '争', '另', '建', '维', '绝', '树', '系', '伤', '示', '愿',
               '持', '千', '史', '谁', '准', '联', '妇', '纪', '基', '买', '志', '静', '阿', '诗', '独', '复', '痛', '消', '社', '算',
               '义', '竟', '确', '酒', '需', '单', '治', '卡', '幸', '兰', '念', '举', '仅', '钟', '怕', '共', '毛', '句', '息', '功',
               '官', '待', '究', '跟', '穿', '室', '易', '游', '程', '号', '居', '考', '突', '皮', '哪', '费', '倒', '价', '图', '具',
               '刚', '脑', '永', '歌', '响', '商', '礼', '细', '专', '黄', '块', '脚', '味', '灵', '改', '据', '般', '破', '引', '食',
               '仍', '存', '众', '注', '笔', '甚', '某', '沉', '血', '备', '习', '校', '默', '务', '土', '微', '娘', '须', '试', '怀',
               '料', '调', '广', '蜖', '苏', '显', '赛', '查', '密', '议', '底', '列', '富', '梦', '错', '座', '参', '八', '除', '跑',
               '亮', '假', '印', '设', '线', '温', '虽', '掉', '京', '初', '养', '香', '停', '际', '致', '阳', '纸', '李', '纳', '验',
               '助', '激', '够', '严', '证', '帝', '饭', '忘', '趣', '支', '春', '集', '丈', '木', '研', '班', '普', '导', '顿', '睡',
               '展', '跳', '获', '艺', '六', '波', '察', '群', '皇', '段', '急', '庭', '创', '区', '奥', '器', '谢', '弟', '店', '否',
               '害', '草', '排', '背', '止', '组', '州', '朝', '封', '睛', '板', '角', '况', '曲', '馆', '育', '忙', '质', '河', '续',
               '哥', '呼', '若', '推', '境', '遇', '雨', '标', '姐', '充', '围', '案', '伦', '护', '冷', '警', '贝', '著', '雪', '索',
               '剧', '啊', '船', '险', '烟', '依', '斗', '值', '帮', '汉', '慢', '佛', '肯', '闻', '唱', '沙', '局', '伯', '族', '低',
               '玩', '资', '屋', '击', '速', '顾', '泪', '洲', '团', '圣', '旁', '堂', '兵', '七', '露', '园', '牛', '哭', '旅', '街',
               '劳', '型', '烈', '姑', '陈', '莫', '鱼', '异', '抱', '宝', '权', '鲁', '简', '态', '级', '票', '怪', '寻', '杀', '律',
               '胜', '份', '汽', '右', '洋', '范', '床', '舞', '秘', '午', '登', '楼', '贵', '吸', '责', '例', '追', '较', '职', '属',
               '渐', '左', '录', '丝', '牙', '党', '继', '托', '赶', '章', '智', '冲', '叶', '胡', '吉', '卖', '坚', '喝', '肉', '遗',
               '救', '修', '松', '临', '藏', '担', '戏', '善', '卫', '药', '悲', '敢', '靠', '伊', '村', '戴', '词', '森', '耳', '差',
               '短', '祖', '云', '规', '窗', '散', '迷', '油', '旧', '适', '乡', '架', '恩', '投', '弹', '铁', '博', '雷', '府', '压',
               '超', '负', '勒', '杂', '醒', '洗', '采', '毫', '嘴', '毕', '九', '冰', '既', '状', '乱', '景', '席', '珍', '童', '顶',
               '派', '素', '脱', '农', '疑', '练', '野', '按', '犯', '拍', '征', '坏', '骨', '余', '承', '置', '臓', '彩', '灯', '巨',
               '琴', '免', '环', '姆', '暗', '换', '技', '翻', '束', '增', '忍', '餐', '洛', '塞', '缺', '忆', '判', '欧', '层', '付',
               '阵', '玛', '批', '岛', '项', '狗', '休', '懂', '武', '革', '良', '恶', '恋', '委', '拥', '娜', '妙', '探', '呀', '营',
               '退', '摇', '弄', '桌', '熟', '诺', '宣', '银', '势', '奖', '宫', '忽', '套', '康', '供', '优', '课', '鸟', '喊', '降',
               '夏', '困', '刘', '罪', '亡', '鞋', '健', '模', '败', '伴', '守', '挥', '鲜', '财', '孤', '枪', '禁', '恐', '伙', '杰',
               '迹', '妹', '藸', '遍', '盖', '副', '坦', '牌', '江', '顺', '秋', '萨', '菜', '划', '授', '归', '浪', '听', '凡', '预',
               '奶', '雄', '升', '碃', '编', '典', '袋', '莱', '含', '盛', '济', '蒙', '棋', '端', '腿', '招', '释', '介', '烧', '误',
               '乾', '坤']


def get_user_by_list_article(cat, skip):
    url = 'https://baijia.baidu.com/listarticle?ajax=json&cat={}&_limit=15&_skip={}'.format(
        cat, skip)
    req = build_request(url)
    data = req.json()['data']
    result = []
    for item in data['items']:
        user = {
            'app_id': item['app_id'],
            'writer_name': item['writer_name'],
            'updated_at': item['updated_at']
        }
        result.append(user)
    return result


def get_user_info(app_id):
    info_url = 'https://author.baidu.com/profile?context={{%22from%22:0,%22app_id%22:%22{app_id}%22}}&cmdType=&pagelets[]=root&reqID=0&ispeed=1'.format(
        app_id=app_id)
    session = requests.session()
    session.get('https://baijiahao.baidu.com/u?app_id={}'.format(app_id),headers=get_headers(),timeout=20)
    res_text = session.get(info_url,headers=get_headers(),timeout=20).text
    res_text = re.findall('onPageletArrive\((.*)\);', res_text)[0]
    data = json.loads(res_text)
    soup = BeautifulSoup(data['html'], 'lxml')
    fans = soup.find('div', {'class': 'fans'}).get_text()
    sign = soup.find('div', {'class': 'sign'}).get_text()
    name = soup.find('div', {'class': 'name'}).get_text()
    article_url='https://author.baidu.com/pipe?context={{%22from%22:0,%22app_id%22:%22{}%22}}&pagelets[]=article&reqID=1&ispeed=1'.format(app_id)
    res_text=session.get(article_url,headers=get_headers(),timeout=20).text
    res_text = re.findall('onPageletArrive\((.*)\);', res_text)[0]
    data = json.loads(res_text)
    update_time=BeautifulSoup(data['html'],'lxml').find('div',{'class':'time'}).get_text()
    return {
        'fans': fans,
        'app_id':app_id,
        'sign': sign,
        'name': name,
        'update_time':update_time,
        'url':'https://baijiahao.baidu.com/u?app_id={}&fr=bjharticle'.format(app_id)
    }


def load_user_from_feed(channel_id=3):
    url = 'https://feed.baidu.com/feed/api/wise/feedlist?sid=110314_100805_122155_123291_100099_123570_120137_118896_118860_118841_118833_118788_120549_107319_122863_117437_123573_122960_114820_123381_110085_123338_123289&channel_id={}'.format(
        channel_id)
    req = build_request(url)
    res_text = req.text.replace('\\&quot;', '"')
    result = re.findall('"mthid(.*?),', res_text)
    result = re.findall('"(\d+)', str(result))
    return result


def load_exists(filename='./files/app_id'):
    exists = {}
    for line in open(filename, 'r'):
        user = json.loads(line)
        exists[user['app_id']] = 1
    return exists


def crawl_user_list():
    # cat_list = ['']
    # exists = load_exists()
    # for cat in cat_list:
    #     skip = 0
    #     num = 0
    #     while num < 3000:
    #         try:
    #             user_list = get_user_by_list_article(cat, skip)
    #         except:
    #             print(cat, skip, 'fail')
    #             time.sleep(2)
    #             continue
    #         f = open('./files/user_list', 'a')
    #         for user in user_list:
    #             if user['app_id'] in exists:
    #                 continue
    #             exists[user['app_id']] = 1
    #             f.write(json.dumps(user)+'\n')
    #             num += 1
    #         f.close()
    #         skip += 15
    #         print(current_time(), cat, num, skip, 'OK')
    #         time.sleep(1)
    exists = load_exists()
    num = 0
    while True:
        try:
            channel_id = random.randint(0, 18)
            result = load_user_from_feed(channel_id)
        except:
            print(current_time(), 'fail')
            time.sleep(1)
            continue
        f = open('./files/app_id', 'a')
        for app_id in result:
            if app_id in exists:
                # print(app_id,'exists')
                continue
            exists[app_id] = 1
            f.write(json.dumps({'app_id': app_id})+'\n')
            num += 1
        f.close()
        print(current_time(), num, len(result))
        # time.sleep(1)


def focus():
    url = 'https://mbd.baidu.com/webpage?action=resource2&type=subscribe&format=json&cate_id={}&size=10&start={}'
    exists = load_exists()
    cate_id = 120
    num = 0
    while cate_id < 150:
        start = 0
        while True:
            try:
                req = build_request(url.format(cate_id, start))
                data = req.json()['data']['list'][0]['items']
            except Exception as e:
                print(cate_id, start, 'fail', req.text)
                break
            f = open('./files/app_id', 'a')
            for item in data:
                app_id = item['third_id']
                if app_id in exists:
                    continue
                exists[app_id] = 1
                f.write(json.dumps({'app_id': app_id})+'\n')
                num += 1
            f.close()
            start += 10
            print(current_time(), cate_id, num, start, len(data))
            time.sleep(1)
        cate_id += 1


def search():
    url = 'https://mbd.baidu.com/webpage?action=searchresource3&type=subscribe&format=json&word={}'
    #words=[i for i in range(10)]+[chr(i) for i in range(97,123)]
    words = first_names
    exists = load_exists()
    num = 0
    headers = get_headers()
    headers['Cookie'] = 'BIDUPSID=DE76B39EB69C4FC2257A6115B8B71466; PSTM=1518760412; __cfduid=d6b3b210a0bd67d6c7b0b03e44cd423831522046031; BDRCVFR[feWj1Vr5u3D]=I67x6TjHwwYf0; BDUSS=JLeG9HZGxic1k0N25nM2YwT2w1YWtLRlQ2YmhBUnpqYnBBYn5NeGR-V2IxaE5iQUFBQUFBJCQAAAAAAAAAAAEAAAB3wvgatd~F5tauz8QAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAJtJ7FqbSexaQX; BDORZ=AE84CDB3A529C0F8A2B9DCDD1D18B695; SE_LAUNCH=5%3A25423947_0%3A25423947_3%3A25423990; BAIDUID=CCCBCB9AEFF2B44A7170831455AD82AA:FG=1; BCLID=13124145665428365287; BDSFRCVID=SsFsJeC627lJl_bANMv8hixNyx5jJuoTH6aItQ7oar-cPrx6TTFdEG0PDx8g0Kub1yFKogKKLgOTHUQP; H_BDCLCKID_SF=Jnkj_C_5f-3sDTrnh4O_KICShUFs5tJR-2Q-5KL-f4Q58n5CLJ7_qjk3LRJhJPbiKGr93MbdJJjosU0zQxn5ej__0GAqLMTk32TxoUJF5DnJhhvGqJ--QUPebPRiJPr9Qg-q_xtLtDK5MKDmDjK3Kn0e-U4XKP50K-o2WDv52hj5OR5Jj65ThbLRyGJCX40f0Cb0XprXalkKqt343MA--fFrQh3XtqTP-TnL0Kbx5xbfsq0x0MOWe-bQypoahJ5x3COMahv15h7xOM5h05CKjjQ3eH-ft6nq264X0ROE5RbEHjrnhPF_-P6M0pblbMT-0bFH_bRFaU7DEqrE567sMJkN2qAtafTtaan7_JjYbUDbDnj4qtbmKRvB3bOlKUQxtNRRXInjtpvhHCjwQxRobUPUXMJ9LUvPLG4E3-oJqC8MhCKl3j; BDPASSGATE=IlPT2AEptyoA_yiU4VGI3kIN8ejzZriA1f3GSDRxQVePpiyWmhHoB_2EUjD6YnSgBC3gzDCweMpkkUXKXlVXcqFCh4sAmWlubFu6wNb6xsOAGBRAzbIZCb4jKUg2p3XvhBEax3ET0QFX4G9FbQDxpuo4ivKl7AhMae8R7802g2XuBlOR2Y4_zWyaOolmO-0APNu5cPrljygdPk_cWe8oRi_2gC1iVp1XzNCndtEXAOzLzH9HIenbOhwpJ9rkI9pd0eKo1faYlMKBAFITmJppKUUtnUKY-qLxSSxR2NTtzcZzM_z-La_WVTjuH_cmjbOKLOFNTBawhbcaOTU66WcUUXhq1PL9CGKWQEgxELGYmRjKCXMT6UCrCBnU-Z9QO4414uMWUwdqUERMela; H_WISE_SIDS=123089_102569_122148_123486_115654_123291_123093_123571_120172_118883_118876_118852_118826_118794_120549_107319_121924_122862_117328_122788_123572_123381_110085_123290_100457'
    for word in words:
        try:
            req = build_request(url.format(word), headers=headers)
            data = req.json()['data']['items']['user']['item']
        except Exception as e:
            print(word, 'fail')
            time.sleep(1)
            continue
        f = open('./files/app_id', 'a')
        for item in data:
            try:
                app_id = item['third_id']
            except:
                continue
            if len(app_id) < 10:
                continue
            if app_id in exists:
                continue
            exists[app_id] = 1
            f.write(json.dumps({'app_id': app_id})+'\n')
            num += 1
        f.close()
        print(current_time(), word, num)
        time.sleep(1)


def crawl_user_info():
    success=0
    fail=0
    for line in open('./files/app_id','r'):
        user=json.loads(line)
        if len(user['app_id']) < 10:
            continue
        try:
            result=get_user_info(user['app_id'])
        except Exception as e:
            f = open('./files/fail', 'a')
            f.write(json.dumps(user)+'\n')
            f.close()
            fail+=1
            print(current_time(),success,fail)
            continue
        success+=1
        f = open('./files/result', 'a')
        f.write(json.dumps(result)+'\n')
        f.close()
        print(current_time(),success,fail)
        
crawl_user_info()