#coding:utf-8
from flask import Blueprint , request , render_template
from bs4 import BeautifulSoup
import urllib2 , urllib , sqlite3 , time , re

book= Blueprint("bn" , __name__)

@book.route("/getname" , methods=['POST' , 'GET'])
def getname():
    ###
    #
    #当请求中有空格会出现400 错误... 待解决
    # 	2016年6月7日03:33:40 编码问题 , 
    # 	request get得到UNicode , encode为utf-8(使识别中文) , 
    # 	urllib.qoute 转换为url编码(使识别特殊字符 如空格)
    ##
    bookname = urllib.quote(request.args.get('bookname').encode('utf-8'))
    #bookname = request.args.get('bookname').encode('utf-8')

    search_url = "https://book.douban.com/subject_search?search_text=%s"%bookname
    #search_url = "https://book.douban.com/subject_search?search_text=我们+就是"

    #服务器欺骗-----------
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36" , "Referer":"https://book.douban.com"}
    
    req = urllib2.Request(search_url , headers=header) 

    res = urllib2.urlopen(req).read()

    soup = BeautifulSoup(res , 'html.parser')

    ### 开始爬了... 获取class_为'subject-item' 的所有li 标签 , 
    ### 得到的是一个soup对象 它是可迭代的...
    item = soup.find_all('li' , class_='subject-item')
    book_name=[]
    pic=[]
    author=[]
    rating=[] ##星级评价(有些书籍没有星..)
    book_url=[]
    for x in item:
        #判断标签是否存在星级评价 \ 链接是否为book.douban , 若不 ,则放弃此书籍
        try:
            rating.append(x.find('span' , class_='rating_nums').string)
            book_url.append(x.find('a' , attrs={'href':re.compile("^https?://book")} ).get('href'))
        except :
            continue
            
        book_name.append(x.find('div' , class_='info').find('a').get('title'))
        pic.append(x.find('img')['src'])
        author.append(x.find('div' , class_='pub').string)
    list_len = len(pic) if len(pic)<5 else 5


    return render_template('book.html' , book_name=book_name ,  pic=pic , author=author ,  book_url=book_url , rating=rating ,  list_len=list_len)
    #return str(book_url)






@book.route('/bookinfo' , methods=['POST' , 'GET'])
def bookinfo():
    if request.method=='POST':
        url = request.form['bookurl']

        header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36" , "Referer":"https://book.douban.com"}

        req = urllib2.Request(url , headers=header)

        res = urllib2.urlopen(req).read()

        soup = BeautifulSoup(res , 'html.parser')

############### 开始爬取
        img = str(soup.find('div' , id='mainpic').find('img').get('src'))

        info= str(soup.find('div' , id='info'))

        title=soup.find('div' ,id='wrapper').find('span').string.encode('utf-8')

        ## ISBN 使用正则表达式获取...因为内容不再标签中
        try:
            isbn = re.findall('ISBN:</span>(.*?)<br/>' , res , re.S)
            isbn =isbn[0].strip()
            if isbn:
                buy_url = "https://www.amazon.cn/gp/aw/s/ref=is_s_?k="+isbn
        except :
            buy_url = "https://www.amazon.cn/gp/aw/s/ref=is_s_?k=97875060111688"
            pass

        #书籍评分
        try:
            rating=soup.find('strong' , class_='rating_num').string.encode('utf-8')
        except :
            rating='0'

        ##获取书籍信息
        try:
            book_intro = str(soup.find('span' , class_="all").find('div' , class_='intro'))
        except :
            book_intro = str(soup.find('div' , class_='intro'))

        ##获取作者信息
        try:
            author_intro = str(soup.find('div' , class_='indent ').find('span' , class_='all').find('div' , class_='intro'))
        except :
            try:
                author_intro = str(soup.find('div' , class_='indent ').find('div' , class_='intro'))
            except :
                author_intro = '暂时没有作者简介 Orz...'


        comment_info = soup.find_all('span' , class_='comment-info')
        comment_cont = soup.find_all('p' , class_='comment-content')
        if len(comment_info):
            c_cont = []
            for i in comment_cont:
                c_cont.append(i)
            c_info = []
            for i in comment_info:
                c_info.append(i)
        else:
            c_info= [""]
            c_cont= ["这本书还木有评论 o(≧口≦)o"]


        html_part_1= '''
<body id="body">
        <script type="text/javascript">
        $(document).ready(function() {
            $("a").click(function(event) {
                event.preventDefault();
            });
        });

        </script>

        <script type="text/javascript">
            $(document).ready(function(){
                $('#but').click(function(){
                    window.location.href="%s" ;
                });
            });
        </script>
    <div class="page-header">
        <h1>%s
            <small>&nbsp;&nbsp;&nbsp;</small></h1>
    </div>
    <div class="media" >
        <div class="media-left media-middle">
            <a href="#">
                <img class="media-object" src="%s" alt="...">
            </a>
        </div>
        <div class="media-body">
            <h4 class="media-heading"></h4> %s
        </div>
    </div>
    <div class="container">
    <br>

    <button id="but" type="button" class="btn btn-primary" onclick="buy()">我要购买</button>

        <hr>
        <div class="starter-template">
            <h4><b>书籍简介</b></h4>
            <p >%s</p>
        </div>
    </div>
    <div class="container">
    <hr>
        <div class="starter-template">
            <h4><b>作者简介</b></h4>
            <p >%s</p>
        </div>
    </div>
    <div class="container">
    <hr>
        <div class="starter-template">
            <h4><b>读者评论</b></h4>
</body>
        '''%(buy_url , title , img , info ,book_intro, author_intro)


        #html_part_2 = u'<h3>读者评论</h3><a href="#">豆瓣评分<span class="badge">%s</span></a>'%rating
        html_part_2=""
        for x , y in zip( c_cont,c_info):
            html_part_2+='''
<div class="panel panel-default">
  <div class="panel-body">
  <p style="float:left">%s</p>
  <p style="float:right">%s</p>
  </div>
</div>
            '''%(x, y)

        html_part_3='''
        </div>
    </div>
        <br>
        <br>
        <div id="foot">
          <span class="glyphicon glyphicon-heart-empty">~~这是一首简单的小情歌~~<span class="glyphicon glyphicon-heart-empty"></span></span>
        </div>
    </body>

        '''
        if isinstance(html_part_2,str):
            aa  = "Yes..."
        else:
            aa =  "No..."



        return html_part_1+html_part_2+html_part_3
    else:
        return "WTF"
