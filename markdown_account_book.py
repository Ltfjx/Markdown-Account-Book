#
# 愁思萦绕夜空 朦胧月色高挂
# 无边际之梦 安然无恙
#

import datetime
import sys
import matplotlib.pyplot as plt
import numpy
import os

#----------配置----------

# 账本名称
_abname = "Markdown 账本" 

# 页脚(Markdown)
_pagefoot = "![](https://img.shields.io/badge/Generated%20by-MAB-blueviolet)"

# 是否启用0时区转换为8时区(如果本地运行,请关闭)
_converttz = False

# 为统计图表使用黑色字体
_useBlackText = False

# 为统计图表使用透明背景
_transparentBG = True

#----------配置----------


#----------函数----------

def genPie( sizes,explode,labels,name,title ): #饼图生成
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=False, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.


    path="./mab_statistics/" # 不存在目录则创建

    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)

    plt.title(title)

    try:
        os.remove(path + name+".png")
    finally:
        plt.savefig(path + name+".png", format='png', bbox_inches='tight', transparent=_transparentBG, dpi=600)
        plt.show()
#----------函数----------


#----------读取文件----------
file = open("./source.md",encoding='utf-8')
text = file.read()
text=text.replace("，",",")
#----------读取文件----------


#----------解析文件----------
try: 
    line = text.splitlines(False)
    # 去除前两行md表格格式
    del line[0]
    del line[0]
    data = [[] for i in range(len(line))]
    for i in range(len(line)):
        row = line[i].split("|")
        for ii in range(len(row)):
            data[i].append(row[ii])
        #去除开头空元素和结尾空元素
        del data[i][0]
        del data[i][7]
    TotalLineNum = len(line)


    # 时间自动填写
    a = datetime.datetime.today()
    if _converttz == True:
        o = datetime.timedelta(hours=8) # 由于github action服务器采用0时区，这里需要进行时区转换
    else:
        o = datetime.timedelta(hours=0)
    strTime = (a+o).strftime("%Y/%m/%d %H:%M")
    print(strTime)
    for i in range(TotalLineNum):
        if len(data[i][0].split("/"))!=3 or len(data[i][0].split(":"))!=2:
            print("Time fixed on Line %s"%(i+1))
            data[i][0] = strTime
except Exception as e:
    o_file = open("./README.md","w+",encoding='utf-8')
    o_file.write("# %s\n"%_abname)
    o_file.write("**>> 生成于 %s**\n"%strTime)

    o_file.write("解析 source.md 时发生了错误。请检查日志。\n")
    o_file.write(str(e))
    sys.exit(0)

#----------解析文件----------


#----------数据计算----------

# 0=时间 1=收支类型 2=操作者 3=分类 4=标签 5=备注 6=金额

    #>> 余额
try:
    Data_TotalMoney = 0
    for i in range(TotalLineNum):
        if data[i][1]=="收入":
            Data_TotalMoney = Data_TotalMoney + abs(float(data[i][6]))
        else:
            Data_TotalMoney = Data_TotalMoney - abs(float(data[i][6]))

    #>> 分类
    temp_category=[]
    for i in range(TotalLineNum):
        temp_category.append(data[i][3])
    temp_category = list(set(temp_category)) # 去重
    TotalCateNum = len(temp_category)
    Data_category = [[] for i in range(TotalCateNum)]
    for i in range(TotalCateNum):
        Data_category[i].append(temp_category[i])
        Data_category[i].append(0) # 1=帐单数
        Data_category[i].append(0) # 2=收入
        Data_category[i].append(0) # 3=支出
        Data_category[i].append(0) # 4=结余
    for i in range(TotalLineNum): # 每行
            for ii in range(TotalCateNum): # 从所有分类中查找当前分类
                if data[i][3] == Data_category[ii][0]:
                    Data_category[ii][1] = Data_category[ii][1]+1
                    if data[i][1]=="收入":
                        Data_category[ii][2] = Data_category[ii][2] + abs(float(data[i][6]))
                    else:
                        Data_category[ii][3] = Data_category[ii][3] - abs(float(data[i][6]))
                    Data_category[ii][4] = Data_category[ii][3] + Data_category[ii][2]

    #>> 标签
    # 获取标签数目
    temp_tag = []
    for i in range(TotalLineNum):
        temp_tag = temp_tag + data[i][4].split(",")
    temp_tag = list(set(temp_tag)) # 去重
    TotalTagNum = len(temp_tag)

    Data_tag = [[] for i in range(TotalTagNum)]
    for i in range(TotalTagNum):
        Data_tag[i].append(temp_tag[i])
        Data_tag[i].append(0) # 1=帐单数
        Data_tag[i].append(0) # 2=收入
        Data_tag[i].append(0) # 3=支出
        Data_tag[i].append(0) # 4=结余

    for i in range(TotalLineNum): # 每行
        temp_tag = data[i][4].split(",")
        for ii in range(len(temp_tag)): # 每个标签
            for iii in range(TotalTagNum): # 从所有标签中查找当前标签
                if temp_tag[ii] == Data_tag[iii][0]:
                    Data_tag[iii][1] = Data_tag[iii][1]+1
                    if data[i][1]=="收入":
                        Data_tag[iii][2] = Data_tag[iii][2] + abs(float(data[i][6]))
                    else:
                        Data_tag[iii][3] = Data_tag[iii][3] - abs(float(data[i][6]))
                    Data_tag[iii][4] = Data_tag[iii][3] + Data_tag[iii][2]
except Exception as e:
    o_file = open("./README.md","w+",encoding='utf-8')
    o_file.write("# %s\n"%_abname)
    o_file.write("**>> 生成于 %s**\n"%strTime)

    o_file.write("数据处理时发生了错误。请检查日志。\n")
    o_file.write(str(e))
    sys.exit(0)
#----------数据计算----------


#----------统计图生成----------

plt.rcParams['font.family']='SimHei'
plt.rcParams['axes.unicode_minus']=False
plt.rcParams['font.size']=13
plt.rcParams['text.color'] = 'white' # 深色即是正义1111
if _useBlackText == True:
    plt.rcParams['text.color'] = 'black' # 浅色是异类11111111

#>> 标签收入
j=0
Data_tag_rm0 = Data_tag # 去除0数据行
for i in range(TotalTagNum):
    if Data_tag[i][2]==0:
        Data_tag_rm0 = numpy.delete(Data_tag_rm0, i-j, axis=0)
        j=j+1

for i in range(len(Data_tag_rm0)):
    Data_tag_rm0[i][0] = Data_tag_rm0[i][0] + "(" +Data_tag_rm0[i][2]+"CNY)"

sizes = [abs(number) for number in numpy.array(list(map(list,zip(*Data_tag_rm0))))[2].astype(float)] # 交换横纵轴，转换数据类型，取绝对值
explode = [0 for i in range(len(sizes))] 
labels = list(map(list,zip(*Data_tag_rm0)))[0] # 交换横纵轴
name = "TagIn"

genPie(sizes,explode,labels,name,"标签收入统计")

#>> 标签支出
j=0
Data_tag_rm0 = Data_tag # 去除0数据行
for i in range(TotalTagNum):
    if Data_tag[i][3]==0:
        Data_tag_rm0 = numpy.delete(Data_tag_rm0, i-j, axis=0)
        j=j+1

for i in range(len(Data_tag_rm0)):
    Data_tag_rm0[i][0] = Data_tag_rm0[i][0] + "(" +Data_tag_rm0[i][3]+"CNY)"

sizes = [abs(number) for number in numpy.array(list(map(list,zip(*Data_tag_rm0))))[3].astype(float)] # 交换横纵轴，转换数据类型，取绝对值
explode = [0 for i in range(len(sizes))] 
labels = list(map(list,zip(*Data_tag_rm0)))[0] # 交换横纵轴
name = "TagOut"

genPie(sizes,explode,labels,name,"标签支出统计")


#----------统计图生成----------


#----------Markdown输出----------
try:
    o_file = open("./README.md","w+",encoding='utf-8')
    o_file.write("# %s\n"%_abname)
    o_file.write("**>> 生成于 %s**\n"%strTime)


    o_file.write("|余额|\n|-|\n|%s|\n"%Data_TotalMoney)

    o_file.write("## 分类统计\n")
    o_file.write("|分类|帐单数|收入|支出|结余|\n|-|-|-|-|-|\n")
    for i in range(TotalCateNum):
        for ii in range(5):
            if ii==2 or ii==3 or ii==4: # 显示收入、支出、结余时强制补为两位小数
                o_file.write("|")
                if Data_category[i][ii]>0:
                    o_file.write("+")
                o_file.write("%.2f"%Data_category[i][ii])
            else:
                o_file.write("|")
                o_file.write(str(Data_category[i][ii]))
        o_file.write("|\n")


    o_file.write("## 标签统计\n")
    o_file.write("|标签|帐单数|收入|支出|结余|\n|-|-|-|-|-|\n")
    for i in range(TotalTagNum): 
        for ii in range(5):
            if ii==2 or ii==3 or ii==4: # 显示收入、支出、结余时强制补为两位小数
                o_file.write("|")
                if Data_tag[i][ii]>0:
                    o_file.write("+")
                o_file.write("%.2f"%Data_tag[i][ii])
            else:
                o_file.write("|")
                o_file.write(str(Data_tag[i][ii]))
        o_file.write("|\n")



    o_file.write("## 全部账单\n")
    o_file.write("|时间|收支类型|操作者|分类|标签|备注|金额|\n|-|-|-|-|-|-|-|\n")
    for i in range(TotalLineNum):
        for ii in range(7):
            if ii==6:
                if data[i][1]=="收入":
                    data[i][6]="+"+str(float(data[i][6]))
                else:
                    if float(data[i][6])<0:
                        data[i][6]=""+str(float(data[i][6]))
                    else:
                        data[i][6]="-"+str(float(data[i][6]))

                # 补0
                temp = data[i][6].split(".")
                if len(temp[1])==1:
                    data[i][6]=data[i][6]+"0"

            o_file.write("|")
            o_file.write(data[i][ii])

        o_file.write("|\n")




    o_file.write("---\n%s"%_pagefoot)
    o_file.close()

#----------Markdown输出----------

#----------source.md格式化----------
    o_file = open("./source.md","w+",encoding='utf-8')
    o_file.write("|时间|收支类型|操作者|分类|标签|备注|金额|\n|-|-|-|-|-|-|-|\n")
    for i in range(TotalLineNum):
        for ii in range(7):
            o_file.write("|")
            o_file.write(data[i][ii])
        o_file.write("|\n")
    o_file.close()

except Exception as e:
    o_file = open("./README.md","w+",encoding='utf-8')
    o_file.write("# %s\n"%_abname)
    o_file.write("**>> 生成于 %s**\n"%strTime)

    o_file.write("生成 Markdown 时发生了错误。请检查日志。\n")
    o_file.write(str(e))
    sys.exit(0)
#----------source.md格式化----------

#TotalMoney = TotalMoney + float(row[7])
#temp_tag = row[5].split(",")
#tag = list(set(tag+temp_tag))
#print(data[1][2])
#print(data[2][1])
#print(data)
#print(line[2])
#print(tag)
print("TotalMoney = "+str(Data_TotalMoney))

