##以公众号H5页面展示用户输入的关键字搜索到的豆瓣书籍内容

技术相关:
------------------------------------------------
	Flask \ Bootstarps \ Ajax \ BeautifulSoup4 \ JavaScript \ Sqlite \ ...

功能描述:
------------------------------------------------

	1. 在公众号(订阅号)中输入 关键字, 系统根据关键字返回带有关键字的豆瓣书籍搜索链接
	
		>公众号根据用户输入的信息类型  msgType 判断返回 , 若是text类型 则返回图文信息

		>图文信息主图从图床随机获取 , 副链接指向固定说明链接


	2. 根据搜索链接爬取书籍信息 , 并展示最多5条结果

		>打开 豆瓣书籍搜索页 并带上关键字 ,爬取超链接为 book.douban 开头的书籍

		>爬取信息包含 title\img\author\rating(评分)\info\url


	3. 点击结果通过Ajax返回书籍详情页面(ajax等待动画) , 包含书籍信息\简介\作者\以及评论

		>根据书籍url进入书籍详情页, 爬取书籍标题\封面\出版信息\书籍简介\作者简介\用户平路(最多显示10条)

		>ajax等待动画是网络上找的...

		>ajax加载完成后移动到页面顶部

		>屏蔽爬取的内容中包含的 超链接

		>添加购买书籍按钮 , 根据书籍ISBN指向亚马逊


![image](https://github.com/hadesong/wcbooks/raw/master/app_package/static/0.png)


![image](https://github.com/hadesong/wcbooks/raw/master/app_package/static/1.jpg)


![image](https://github.com/hadesong/wcbooks/raw/master/app_package/static/2.jpg)


![image](https://github.com/hadesong/wcbooks/raw/master/app_package/static/3.jpg)

公众号链接
![image](https://github.com/hadesong/wcbooks/raw/master/app_package/static/Hades.jpg)