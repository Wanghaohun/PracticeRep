import getopt  
import re
import urllib
import requests
import time
import os
import io
import hashlib
from sys import argv
def get_time():
    #返回本地时间
    localtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return localtime

def timing():
    time1=time.clock()
    return time1

def make_dir(user_id):
    #创建图片保存目录，每个user_id的日志和总日志
    general_path=os.getcwd()+os.sep+'image_download'
    if os.path.exists(general_path) is False:
        os.mkdir(general_path)
        print("创建目录%s"%general_path)    
    uid_path=general_path+os.sep+user_id
    if os.path.exists(uid_path) is False:
        os.mkdir(uid_path)
        print("创建目录%s"%uid_path)
    general_log_path=general_path
    if os.path.isfile(general_log_path+os.sep+'general_log.txt') is False:  
        f=open(general_log_path+os.sep+'general_log.txt','w')
        print("创建总日志%s"%general_log_path)       
    part_log_path=general_path+os.sep+user_id
    if os.path.isfile(part_log_path+os.sep+'part_log.txt') is False:  
        f=open(part_log_path+os.sep+'part_log.txt','w')
        f.close()
        print("创建分日志%s"%part_log_path)
        number=0
    else:
        number=1
    index_path=general_path
    if os.path.isfile(index_path+os.sep+'index.txt') is False:  
        f=open(index_path+os.sep+'index.txt','w')
        print("创建md5值记录表%s"%index_path)
    return (general_path,uid_path,general_log_path,part_log_path,index_path,number)

def same_name_addcheck(path,create_time,ext,number):
    #重名的处理
    global chongming
    temp='(%d)'%chongming
    full_path=path+os.sep+create_time+temp+ext
    if os.path.isfile(full_path) is True and number==0:
        return (1,full_path)
    if os.path.isfile(full_path) is False and number==0:
        return (1,full_path)
    if os.path.isfile(full_path) is True and number==1:
        return (0,full_path)
    if os.path.isfile(full_path) is False and number==1:
        return (1,full_path)

def print_log(msg,file):
    #将记录add到path
    print(msg)
    if file!='':
        open(file,'a').write(msg+'\n')
        open(file).close()
    return 0

def callbackfunc(blocknum, blocksize, totalsize):
    '''回调函数
    @blocknum: 已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
    '''
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    intper = int(percent)
    n = int(intper/2)
    m = 60
    show=m * '\b'+'['+n * '#'+(50-n) * '~'+']['+'%02d%%]'%percent
    sys.stdout.write(show)
    return 0

def multi_uid_from_txt(txt_path):
    #从txt读取user_id和screen_name，返回一个列表和uid数量
    idcount=0
    info=[]
    f = open(txt_path,'r')
    for line in f.readlines():
        line = line.strip()
        if not len(line) or line.startswitch:
            continue
        get_uid=re.findall('uid:(.*?) ')
        info=info.append(get_uid)
        idcount+=1
    return (info,idcount)

def get_page_by_uid(user_id,pg):
    #获得该user_id第pg页的内容
    url = "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=107603%s&page=%d"%(user_id,user_id,pg)
    #e.g.  https://m.weibo.cn/api/container/getIndex?type=uid&value=5884009876&containerid=1076035884009876&page=1
    code = requests.get(url).text
    return (code)

def get_mblogs(code):
    regular = '"mblog":(.*?)\}\}]},'
    mblogs = re.findall(regular,code)
    return mblogs
def get_guanzhu(user_id):
    user_id=(int)(user_id)
    starttime = timing()
    pg,i,x,y=0,0,0,0
    log_path=os.getcwd()+os.sep+'image_download'+os.sep+'GuanZhu.txt'
    while True:
        pg +=1
        url = "https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_%d&luicode=10000011&lfid=100505%d&featurecode=20000180&page=%d"%(user_id,user_id,pg)
        code = requests.get(url).text
        relink = '"user":{"id":(.*?),"screen_name":"(.*?)"'
        urllist = re.findall(relink,code)
        i += len(urllist)
        while x <= len(urllist)-1:
            urllist0=urllist[x]
            uid=urllist0[0]
            name=urllist0[1].encode('utf-8').decode('unicode_escape')
            combine='name:'+name+' '+'uid:'+uid
            print(combine)
            open(log_path,'a').write(combine+'\n')
            open(log_path,'a').close()
            time.sleep(0.1)
            x+=1
        x=0
        if(urllist==[]):
            break
    print("%d的关注列表爬取完毕，共%d条"%(user_id,i))
    print("保存地址为%s"%(log_path))
def get_creat_time(mblog):
    regular = '"created_at":"(.*?)"'
    create_time = re.findall(regular,mblog)
    create_time = create_time[0]
    now=get_time()
    today=time.strftime("%Y-%m-%d", time.localtime())
    if len(create_time)<16:
        create_time='2017-'+create_time
    create_time=create_time.replace("：","_")
    create_time=create_time.replace(":","_")
    create_time=create_time.replace("\\u4eca\\u5929",today)
    create_time=create_time.replace("\\u5206\\u949f\\u524d",'minute before'+now)
    create_time=create_time.replace("\\u79d2",'seconds before'+now)
    return create_time

def get_img_urls(mblog):
    img_urls=[]
    regular = '"size":"large","url":"(.*?)"'
    urllists = re.findall(regular,mblog)
    for urllist in urllists:
        urllist = urllist.replace('\\/','/')
        img_urls.append(urllist)
    return img_urls

def get_image(img_url,create_time,uid_path,number):
    
    (mode,download_location)=same_name_addcheck(uid_path,create_time,'.jpg',number)
    if mode==1:
        try:
            urllib.request.urlretrieve(img_url,download_location,callbackfunc)
            download_time=get_time()
            status=1
        except:
            status=0
            download_time=get_time()
    else:
        status=0
        download_time=get_time()
    return (download_location,status,download_time)

def CalculateFileHash(file):  
    f = open(file, "rb")  
    content = f.read()  
    m = hashlib.md5()  
    #m = hashlib.sha1()  
    m.update(content)  
    s = m.hexdigest()  
    del m  
    f.close()  
    return s

def input_index(download_location,index_path):
    md5=CalculateFileHash(download_location)
    general_index='\n位置：'+download_location+'\nmd5值：'+md5
    f=open(index_path+os.sep+'index.txt','r')
    if re.search(md5,f.read()) == None:     
        (_,filename)=os.path.split(download_location)
        print_log(general_index,index_path+os.sep+'index.txt')
    else:
        return 0
    return 0

def anti_anti_crawler(last):
    if last < 1:
        time.sleep(1-last)
    return 0

def get_single(user_id):
    global chongming
    time_1a=timing()
    (general_path,uid_path,general_log_path,part_log_path,index_path,number)=make_dir(user_id)
    localtime_to_name=time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    pg,i,x,y=0,0,0,0
    last_create_time=''
    while True:
        pg+=1
        code=get_page_by_uid(user_id,pg)
        mblogs=get_mblogs(code)
        for mblog in mblogs:
            create_time=get_creat_time(mblog)
            if last_create_time != create_time:
                chongming=0
            last_create_time=create_time
            img_urls=get_img_urls(mblog)
            for img_url in img_urls:
                chongming+=1
                i+=1
                time_2a=timing()
                (download_location,status,download_time)=get_image(img_url,create_time,uid_path,number)
                if status:
                    x+=1
                    time_1b=timing()
                    use_time=time_1b-time_1a                    
                    msg='图片保存成功(%d) 已运行 %d 秒        '%(x,use_time)+get_time()
                    input_index(download_location,index_path)
                else:
                    y+=1
                    time_1b=timing()
                    use_time=time_1b-time_1a
                    msg1='图片保存失败(%d) 已运行 %d 秒        '%(y,use_time)+get_time()
                    print(msg1)
                    msg=img_url+'    '+get_time()
                    print_log(msg,uid_path+os.sep+'part_log.txt')
                time_2b=timing()
                last=time_2b-time_2a
                anti_anti_crawler(last)
            if img_urls==[]:
                break
        if(mblogs==[]):
            pg +=1
            url = "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=107603%s&page=%d"%(user_id,user_id,pg)
            code = requests.get(url).text
            regular = '"mblog":(.*?)\}\}]},'
            mblogs = re.findall(regular,code)
            pg -=1
            if(mblogs==[]):
                pg +=2
                url = "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=107603%s&page=%d"%(user_id,user_id,pg)
                code = requests.get(url).text
                regular = '"mblog":(.*?)\}\}]},'
                mblogs = re.findall(regular,code)
                pg -=1
                if(mblogs==[]):                  
                    pg +=3
                    url = "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=107603%s&page=%d"%(user_id,user_id,pg)
                    code = requests.get(url).text
                    regular = '"mblog":(.*?)\}\}]},'
                    mblogs = re.findall(regular,code)
                    pg -=1
                    if(mblogs==[]):
                        pg +=4
                        url = "https://m.weibo.cn/api/container/getIndex?type=uid&value=%s&containerid=107603%s&page=%d"%(user_id,user_id,pg)
                        code = requests.get(url).text
                        regular = '"mblog":(.*?)\}\}]},'
                        mblogs = re.findall(regular,code)
                        pg -=1
                        if(mblogs==[]):                      
                            break
                            
    time_1b=timing()
    use_time=time_1b-time_1a
    return (i,x,y,use_time)

def multi_blog_from_txt(txt_path):
    general_log_path=os.getcwd()+os.sep+'image_download'
    sum_all, sum_succ, sum_fail,sum_time, idcount, i = 0, 0, 0, 0, 0, 0    
    f = open(txt_path, 'r')                   #以读方式打开文件   
    for line in f.readlines():                          #依次读取每行  
        line = line.strip()                             #去掉每行头尾空白  
        if not len(line) or line.startswith('#'):       #判断是否是空行或注释行  
            continue                                    #是的话，跳过不处理  
        print(line)
        userid =re.findall('uid:(.*)',line)          #正则匹配user_id
        user_id=userid[0]
        back = get_single(user_id)  
        sum_all += back[0]
        sum_succ += back[1]
        sum_fail += back[2]
        sum_time += back[3]
        idcount += 1
    print('\n')
    print('----------------------------------------------------------------------')
    print('\n')
    print("已爬取用户ID列表：")
    all_general_info="%d个id的微博图片爬取完成\n\n共%d张图片，成功%d张，失败%d张\n\n"%(idcount,sum_all,sum_succ,sum_fail)+'\n\n保存路径'+os.getcwd()+'\\image_download\\'
    print_log(all_general_info,general_log_path+os.sep+'general_log.txt')
    
def usage():
    print ("                                                    ")  
    print ("********************************************************")
    print ("************      Rubb1shK1d 版权所有       ************")
    print ("*********             爬虫命令举例             *********")
    print ("********************************************************")    
    print ("python crawler.py -h  使用命令"  )
    print ("python crawler.py --help " )
    print ("————————————————————————————" )
    print ("python crawler.py -s user_id 新浪微博图片爬虫"  )
    print ("python crawler.py --sinablog user_id "  )
    print ("————————————————————————————" )
    print ("python crawler.py -g user_id 新浪微博关注爬虫")
    print ("python crawler.py --guanzhu user_id ")
    print ("————————————————————————————" )

def main():     
    chongming=0
    # 读取命令行选项,若没有该选项则显示用法  
    try:  
        # opts：一个列表，列表的每个元素为键值对  
        # args:其实就是sys.argv[1:]  
        # sys.argv[1:]：只处理第二个及以后的参数  
        # "ts:h"：选项的简写，有冒号的表示后面必须接这个选项的值（如 -s hello）  
        # ["help", "test1", "say"] :当然也可以详细地写出来，不过要两条横杠（--）  
        opts, args = getopt.getopt(argv[1:], "s:hg:",["help", "sinablog","guanzhu"]) 
        # print opts  
        
        # 具体处理命令行参数
        usage()
        for o,v in opts:
                    
            if argv[1]=='':
                usage()
            elif o in ("-h","--help"):  
                usage()  
            elif o in ("-s", "--sinablog"): 
                if argv[2].isdigit():
                    get_single(argv[2])
                elif os.path.exists(argv[2]):
                    multi_blog_from_txt(argv[2])
            elif o in ("-g","--guanzhu"):
                get_guanzhu(argv[2])
    except getopt.GetoptError:  
        # print str(err)  
        usage()  

if __name__=='__main__':  
    main()