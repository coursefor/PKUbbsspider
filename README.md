# PKUbbsspider
北大未名BBS简易版爬虫程序，可以抓取BBS任意版面任意范围有权限访问的帖子，包含帖子标题，内容，所有评论，内容和评论的作者和赞踩数等

由于仅用笔记本电脑运行，故采用单线程requests抓取。本人正则表达式没学好，网页解析部分写的有点乱。

## 使用介绍
需要用python3运行，需安装bs4和requests库
需要登录bbs（保持登录状态）获取cookie
具体使用方法代码中有注释

## 进一步数据分析
我使用的是jieba分词处理文本数据，代码就不放上来了。怎么分析数据大家可以大显神通


提供一个解析数据思路：比如鹊桥如果要分析交友贴的个人信息和对对方的要求，比如分析女生征友对身高要求。可以在文本中定位身高关键词，然后查询附近的三位数或者类似的数据；如果出现两次且不相等，通常高的那个/出现在后面的那个就是对对方的要求；此外，对对方的要求一般会加上“以上”等限定范围的词

分析学历，地点，喜好，年龄均可用类似方法。如果用机器学习当然也可。

