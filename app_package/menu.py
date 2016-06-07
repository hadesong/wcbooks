#coding:utf-8
import urllib2 
#订阅号没有自定义菜单的权限.......
menu_post = '''
 {
     "button":[
     {	
          "type":"click",
          "name":"今日歌曲",
          "key":"V1001_TODAY_MUSIC"
      },
      {
           "name":"菜单",
           "sub_button":[
           {	
               "type":"view",
               "name":"搜索",
               "url":"http://www.soso.com/"
            },
            {
               "type":"view",
               "name":"视频",
               "url":"http://v.qq.com/"
            },
            {
               "type":"click",
               "name":"赞一下我们",
               "key":"V1001_GOOD"
            }]
       }]
 }
'''

def create_menu():
	at = "7DkTD_ossi2nWDYf_QWpquymZd1z7EaA6vb7IX9gK9_VKRxC18uMgC6NdUC0hqlCHSv8DLlNIkbKUD95zaZ6sEnV3Q1c_MiJMQdH2Yi0nmL_wlA7covnOZKaESjAs3JeIEXcAEAQMF"
	url ='https://api.weixin.qq.com/cgi-bin/menu/create?access_token='+at
	req = urllib2.urlopen(url , menu_post).read()

	return req


if __name__ == '__main__':
	print create_menu()