import os



def load_level():
    level={}
    for line in open('Cost_qualification.txt','r'):
        line=line.replace('\n','').split('\t')
        print(line)
        level[line[0]]=line[1]
    return level

def deal():
    keys=['姓名','性别','民族','学历','name','所属省市','联系地址','法人代表','工程监理资质','招标代理','造价咨询','一级注册建筑师','二级注册建筑师'
            ,'一级注册结构工程师','二级注册结构工程师','注册土木工程师（岩土）','注册公用设备工程师（暖通空调）','注册公用设备工程师（给水排水）','注册公用设备工程师（动力）'
                ,'注册公用设备工程师（发输变电）','注册公用设备工程师（供配电）','注册化工工程师','监理工程师','一级建造师','二级建造师','造价工程师']
    keys_two=['姓名','性别','民族','学历','name','所属省市','联系地址','法人代表']
    keys_three=['工程监理资质','招标代理','造价咨询','监理工程师','一级建造师','二级建造师']
    f=open('data.txt','w')
    level=loadLevel()
    for line in open('result.txt','r'):
        person={}
        item=eval(line)
        for key in keys:
            if key not in item:
                person[key]='N'
            else:
                person[key]='Y'
        for key in keys_two:
            person[key]=item[key]
        for key in keys_three:
            text=''
            try:
                for i in item[key]:
                    if i not in text:
                        text+=i+','
                person[key]=text[:-1]
            except:
                person[key]=text
        try:
            person['造价咨询']=level[item['name']]
        except:
            person['造价咨询']='-'
        text=''
        for key in keys:
            text+=person[key]+' ||'
        f.write(text+'\n')
    f.close()

deal()
