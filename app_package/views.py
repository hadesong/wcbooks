#coding:utf-8
from app_package import app , atoken , menu
from flask import request , make_response , redirect , render_template
import urllib2 , urllib , sqlite3 , time , re 
from random import choice
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
from getbook import book


app.register_blueprint(book)


@app.errorhandler(404)
def page_not_found(value):
    return "<h1>404</h1>"

#首页测试
@app.route('/index')
def indexcz():
    return redirect('/')
@app.route('/')
def index():
    return "<h1>Index</h1>"


#微信通过get方式传递 signature\timestamp\nonce\echostr 到服务器
## 经过服务器端加密验证这些信息无误后返回 echostr 给微信
### 其实i直接不做验证返回 echostr 也是可以的....
@app.route('/weixin' , methods=['POST' , 'GET'])
def token():
    base_url = app.config['BASE_URL']
    echostr = request.args.get('echostr')

    if echostr:
        return echostr

    if request.method == 'POST':
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        toUser = xml_rec.find('ToUserName').text
        frUser = xml_rec.find('FromUserName').text
        crTime = xml_rec.find('CreateTime').text
        msType  = xml_rec.find('MsgType').text
        
        ti = str(int(time.time()))
        if msType == "text":
            #con = urllib.quote(xml_rec.find("Content").text.encode('utf-8'))
            con =xml_rec.find("Content").text.encode('utf-8')
            #随机图片
            img_dict = {
                "p1":"https://ooo.0o0.ooo/2016/06/05/5754e8cbd027e.jpg",
                "p2":"https://ooo.0o0.ooo/2016/06/05/5754e8cbddd79.jpg",
                "p3":"https://ooo.0o0.ooo/2016/06/05/5754e8cd0be3b.jpg",
                "p4":"https://ooo.0o0.ooo/2016/06/05/5754e8cdac846.jpg",
                "p5":"https://ooo.0o0.ooo/2016/06/05/5754e8ce6ff49.jpg",
                "p6":"https://ooo.0o0.ooo/2016/06/05/5754e8ceb37b9.jpg",
                "p7":"https://ooo.0o0.ooo/2016/06/05/5754e8d6addb0.jpg",
                "p8":"https://ooo.0o0.ooo/2016/06/05/5754e8d6b2f86.jpg",
                "p9":"https://ooo.0o0.ooo/2016/06/05/5754e8d824d0e.jpg",
                "pa":"https://ooo.0o0.ooo/2016/06/05/5754e8d8e8887.jpg",
                "pb":"https://ooo.0o0.ooo/2016/06/05/5754e8d92054b.jpg",
                "pc":"https://ooo.0o0.ooo/2016/06/05/5754e8d93423c.jpg",
                "pd":"https://ooo.0o0.ooo/2016/06/05/5754ed0f29c10.jpg",
                "pe":"https://ooo.0o0.ooo/2016/06/05/5754ed1113213.jpg",
                "pf":"https://ooo.0o0.ooo/2016/06/05/5754ed1128218.jpg",
                "pg":"https://ooo.0o0.ooo/2016/06/05/5754ed1175271.jpg",
                "ph":"https://ooo.0o0.ooo/2016/06/05/5754ed122bf1b.jpg",
                "pi":"https://ooo.0o0.ooo/2016/06/05/5754ed1373c80.jpg"
                }
            img = img_dict[choice(img_dict.keys())]
            #回复图文消息
            msg = '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[news]]></MsgType>
                <ArticleCount>2</ArticleCount>
                <Articles>
                <item>
                <Title><![CDATA[→_→ 《%s》]]></Title>
                <Description><![CDATA[人家是搜索结果啦]]></Description>
                <PicUrl><![CDATA[%s]]></PicUrl>
                <Url><![CDATA[%sgetname?bookname=%s]]></Url>
                </item>
                <item>
                <Title><![CDATA[说明]]></Title>
                <Description><![CDATA[酱紫 , 宝宝教你]]></Description>
                <PicUrl><![CDATA[https://ooo.0o0.ooo/2016/06/05/5754ee95b4f05.jpg]]></PicUrl>
                <Url><![CDATA[%sins]]></Url>
                </item>
                </Articles>
                </xml>
                '''%(frUser , toUser ,ti , con , img , base_url ,con , base_url)



        elif msType == "image":
            im =  xml_rec.find('PicUrl').text
            info="图片保存在这里了\n\n-->%s"%im
            msg= '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>
            '''%(frUser , toUser , ti , info)

        elif msType == "voice":
            #msg =  xml_rec.find('MediaId').text,
            info= "是谁在唱歌 , 温暖我心窝\n\n  O(∩_∩)O~~"
            msg= '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>
            '''%(frUser , toUser , ti , info)
        elif msType == "video":
            #msg =  xml_rec.find('MediaId').text,
            info= "老司机要开车了吗 ??\n\n (づ￣3￣)づ╭～"
            msg= '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>
            '''%(frUser , toUser , ti , info)
        elif msType == "shortvideo":
            #msg =  xml_rec.find('MediaId').text,
            info= "小电影什么的..我才没有看过!\n\n(=￣ω￣=)"
            msg= '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>
            '''%(frUser , toUser , ti , info)
        elif msType == "location":
            #msg="经度:"+xml_rec.find('Location_x').text+"纬度"+xml_rec.find('Location_y').text
            info="我晚上去你家 , 等我哟~~\n\n(⊙ ▽ ⊙)"
            msg= '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>
            '''%(frUser , toUser , ti , info)
        elif msType == "link":
            info=xml_rec.find('Url').text
            msg= '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>
            '''%(frUser , toUser , ti , info)
        elif msType == "event":
            get_info=xml_rec.find('Event').text
            event_dict = {
            "subscribe":"亲 , 果然有眼光 !/::)\n\n\t\t/:rose请输入要找的书名\n\t\t/:rose当然,你也可以给我发送任意信息",
            "unsubscribe":"没有你的日子里, 我会好好珍惜自己..."
            }



            info = event_dict.get(get_info)
            msg= '''
                <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[text]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                </xml>
            '''%(frUser , toUser , ti , info)

        ##回复构造的xml
        response = make_response(msg)
        response.content_type='application/xml'
        return response
    return "<h2>不能说的秘密</h2>"





@app.route('/ins')
def ins():
    return render_template('ins.html')

# 获取 access token 测试.....
@app.route('/wwww')
def wwww():
    return atoken.select_at()




