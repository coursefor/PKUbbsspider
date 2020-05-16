"""
name:BBSspider简陋版
date:20200525
by:zfl@pku.edu.cn
packages:bs4 requests#需要安装这两个库，如果卡bug可百度或谷歌解决办法
本程序没有使用破解反爬的措施，亲测不会出问题。如果异常，可以在抓取数据时设置间隔
"""


####################################
#本处为使用者需要自己填写的信息
cookiee=''          #登录BBS后，将cookie复制到此。查看cookie的方式若不会可自行百度

bid=''              #想抓取的版面号，打开BBS一个版面后，如"北大发展"版网址 https://bbs.pku.edu.cn/v2/thread.php?bid=294 最后的bid是294，需把数字填在引号内
pagerange=(1,5)     #填写要抓取的版面的页面范围（每页包含20个帖子）。比如，如果要抓取鹊桥最近1000帖，则填写（1,51）

####################################
#本程序会产生的文件
datafile="data#"+bid+"@"+str(pagerange[0])+"-"+str(pagerange[1]-1)                     #最终生成的数据文件
hreffile="href#"+bid+"@"+str(pagerange[0])+"-"+str(pagerange[1]-1)             #所要抓取的版面范围的帖子
exceptionlog="exception#"++bid+"@"+str(pagerange[0])+"-"+str(pagerange[1]-1)   #抓取过程异常记录（没有抓取到的帖子的ID）

数据文件的格式={"帖子的相对链接":{"title":"帖子标题","content":[["楼主id","获赞数","点踩数","帖子文本内容","帖子回复（引用）内容","发布时间或最后修改时间"],["2楼..."]]},"第二个帖子链接":{[]}}
####################################






def ltoj(list,filename):#
    import json
    json_info = list
    file = open(filename+".json", 'w', encoding='utf-8')
    json.dump(json_info, file)
    return 0

def jtol(filename):
    import json
    file = open(filename+".json", 'r', encoding='utf-8')
    info = json.load(file)
    return info

def totext(inpu):
    import re
    inpu=inpu.replace("</p>","&hh&</p>")
    pre = re.compile('>(.*?)<')
    text = ''.join(pre.findall(inpu))
    return text


def paxsh(page,bid):
    page=str(page)
    import requests
    from bs4 import BeautifulSoup
    if page=="1":
        a = 'https://bbs.pku.edu.cn/v2/thread.php?bid='+bid
    else:
        a='https://bbs.pku.edu.cn/v2/thread.php?bid='+bid+'&mode=topic&page='+page
    header = {'User-Agent': 'bbsspider',
              'cookie':cookiee}
    r = requests.get(a, headers=header)
    r.encoding = "utf-8" # 编码
    des = r.text
    obs=BeautifulSoup(des,"html.parser")
    board=obs.find_all(class_="list-item-topic list-item")
    final=[]
    raw=des
    for each in board:
        temp=[]
        aclass=str(each.a)
        s=aclass.find('post-read')
        e=aclass.find('"',s)
        fin=aclass[s:e]
        title=each.find_all(class_="title l limit")[0]
        title=title.get_text()
        fin=str(fin.replace("&amp;","&"))
        # print(fin)
        temp.append(title)
        temp.append(fin)
        final.append(temp)
    return final,des


def pap(ur):
    import requests
    from bs4 import BeautifulSoup
    a="https://bbs.pku.edu.cn/v2/"+ur
    header = {'User-Agent': 'bbsspider',
              'cookie': cookiee}
    r = requests.get(a, headers=header)
    r.encoding = "utf-8"
    raw=r.text
    obs = BeautifulSoup(raw, "html.parser")
    board = obs.find_all(class_="post-card")
    title=obs.find_all("h3")[0].get_text()
    def singlepage(inboard):
        singlepagelis=[]
        for each in inboard:
            author = str(each.find_all(class_="username")[0])
            time=each.find_all(class_="sl-triangle-container")[0].find_all("span")[0].get_text()
            pr = author.find('''href="user''')
            s = author.find('>', pr)
            e = author.find("</a>", s)
            author = author[s + 1:e]
            eachstr = str(each)
            try:
                dzs = eachstr.find("upvote-count")
                dze = eachstr.find("</", dzs)
                dz = int(eachstr[dzs + 14:dze])
                dcs = eachstr.find("downvote-count")
                dce = eachstr.find("</", dcs)
                dc = int(eachstr[dcs + 16:dce])
            except:
                dz,dc=-1,-1
            xx = each.find_all(class_="body file-read image-click-view")[0]
            xxstr = str(xx)
            xxmid = xxstr.find("quotehead")
            pl = totext(xxstr[:xxmid] + ">").replace("&hh&", "\n")
            rep = totext(xxstr[xxmid:] + "<").replace("&hh&", "\n")
            singlepagelis.append([author, dz, dc, pl,rep,time])
        return singlepagelis
    pure=singlepage(board)
    yms=str(obs.find_all(class_="paging-input-wrapper")[0])
    ymstart=yms.find("max")+5
    ymend=yms.find('''"''',ymstart)
    yms=int(yms[ymstart:ymend])
    if yms>=1:
        for ymsn in range(2,yms+1):
            rhere = requests.get(a+"&page="+str(ymsn), headers=header)
            rhere.encoding = "utf-8"
            rawhere = rhere.text
            obshere = BeautifulSoup(rawhere, "html.parser")
            boardhere = obshere.find_all(class_="post-card")
            pure+=singlepage(boardhere)
    return raw,pure,title



def pindex(fname,ran):
    import time
    li = []
    # raw=[]
    for i in ran:
        try:
            a,b=paxsh(i)
            li += a[1:]
            # raw.append(b)
            time.sleep(1)
        except:
            pass
    ltoj(li, fname)



def run(hreff,dataf,exceptionf):
    error=[]
    s=jtol(hreff)
    purelis={}
    # rawlis={}
    for each in s:
        try:
            import time
            raw, pure,title = pap(each[1])
            purelis[each[1]]={"title":title,"list":pure}
            # rawlis[each[1]]=raw
            print(title)
        except:
            error.append(each[1])
            print("!!!!!!!!!!!!!!!!!!!!!!!!!error occur")
    ltoj(purelis,dataf)
    # ltoj(rawlis,"鹊桥1000源代码")
    ltoj(error,exceptionf)
    return purelis

pindex(hreffile,pagerange)
print("帖子索引抓取完成，以下抓取帖子详细内容")
run(hreffile,datafile,exceptionlog)
print("任务完成，数据文件："+datafile+"\n异常索引："+exceptionlog)
