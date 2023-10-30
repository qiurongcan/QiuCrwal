# 一些爬虫练习相关的代码
## 1.豆瓣
豆瓣top250的爬取，使用的时候需要安装requests库和pandas库、lxml库
使用xpath的方法进行解析数据，使用是修改user-agent
最基础的爬虫联系，无反爬，只需要user-agent的即可

## 2.小木虫
test.py是数据爬取的文件
1. 这里爬取的是小木虫中，有关于“非升即走”的关键词的帖子
2. 这里会出现几个问题：
3. 首先是爬取速率不能过快，设置延迟访问时间
4. 部分数据需要登陆+cookie才能访问
5. 访问一定数据以后会封号，在测试的时候多准备几个号
6. 建议隔一段时间保存一下数据
7. 使用xpath的访问方式，数据量不是很多，慢慢爬取即可

data_slove.ipynb是处理爬取后的数据，剔除一些招聘广告和重复的数据
