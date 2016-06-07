#以公众号H5页面展示用户输入的关键字搜索到的豆瓣书籍内容

技术相关:
	Flask \ Bootstarps \ Ajax \ BeautifulSoup4 \ JavaScript \ Sqlite \ ...

功能描述:

	1. 在公众号(订阅号)中输入 关键字, 系统根据关键字返回带有关键字的豆瓣书籍搜索链接

	2. 根据搜索链接爬取书籍信息 , 并展示最多5条结果

	3. 点击结果通过Ajax返回书籍详情页面(ajax等待动画) , 包含书籍信息\简介\作者\以及评论

	4. 屏蔽爬取信息的超链接 , 添加书籍购买链接(指向亚马逊)

![image](https://github.com/hadesong/wcbooks/raw/master/app_package/static/0.png)


![image](https://github.com/hadesong/wcbooks/raw/master/app_package/static/1.jpg)


![image](https://github.com/hadesong/wcbooks/raw/master/app_package/static/2.jpg)


![image](https://github.com/hadesong/wcbooks/raw/master/app_package/static/3.jpg)
