import sys  
import getopt  
import re
import urllib
import requests
import time
import os
import io
from selenium import webdriver
from selenium.webdriver.support.ui import Select 
from time import sleep

def is_Element_Exist_by_id(driver,element):
    try:
        driver.find_element_by_id(element)
    except:
        return False
    return True
    
def is_Element_Exist_by_xpath(driver,element):
    try:
        driver.find_element_by_xpath(element)
    except:
        return False
    return True	
def wait_by_id(driver,element,message):
    while not is_Element_Exist_by_id(driver,element):
        print(message)
        sleep(1)
def wait_by_xpath(driver,element,message):
    while not is_Element_Exist_by_xpath(driver,element):
        print(message)
        sleep(1)    
def search(word1,word2,time1,time2):
    general_path=os.getcwd()+os.sep+'EV_download'
    if os.path.exists(general_path) is False:
        os.mkdir(general_path)
        print("创建目录%s"%general_path)
    url="https://www.engineeringvillage.com/search/quick.url"
    print('searching')
    #fireFoxOptions = webdriver.FirefoxOptions()
    #fireFoxOptions.set_headless()
    profile = webdriver.FirefoxProfile()
    profile.set_preference('browser.download.dir', general_path)
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.manager.showWhenStarting', False)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/x-no-such-app;charset=UTF-8')
    driver=webdriver.Firefox(firefox_profile=profile)#,firefox_options=fireFoxOptions)
    driver.set_page_load_timeout(600)
    driver.get(url)
    driver.find_element_by_name("searchWord1" ).send_keys(word1)
    driver.find_element_by_id("add-searchfield-link" ).click()
    driver.find_element_by_name("searchWord2" ).send_keys(word2)
    driver.find_element_by_id("date-tab").click()
    driver.find_element_by_id("select2-sect1-container").click()
    css=driver.find_element_by_xpath("//span[@class='select2-results']/ul")
    alloptions=css.find_elements_by_tag_name("li")
    for option in alloptions:
        if "Author affiliation" in option.text:
            option.click()
            break
    driver.find_element_by_xpath("//span[@class='selection']/span[@class='select2-selection select2-selection--single']/span[@title='All fields']").click()
    css=driver.find_element_by_xpath("//ul[@id='select2-field_c325-results']")
    alloptions=css.find_elements_by_tag_name("li")
    for option in alloptions:
        if "Author affiliation" in option.text:
            option.click()
            break    
    driver.find_element_by_id("select2-start-year-container").click()            
    css=driver.find_element_by_xpath("//span[@class='select2-results']/ul[@id='select2-start-year-results']")
    alloptions=css.find_elements_by_tag_name("li")
    for option in alloptions:
        if time1 in option.text:
            option.click()
            break           
    driver.find_element_by_id("select2-end-year-container").click()           
    css=driver.find_element_by_xpath("//span[@class='select2-results']/ul[@id='select2-end-year-results']")
    alloptions=css.find_elements_by_tag_name("li")
    for option in alloptions:
        if time2 in option.text:
            option.click()
            break   
    
    wait_by_id(driver,"searchBtn","waiting for searching")
    driver.find_element_by_id("searchBtn").click()
    wait_by_id(driver,"select2-results-per-page-select-container","waiting for searching")    
    driver.find_element_by_id("select2-results-per-page-select-container").click()     
    css=driver.find_element_by_xpath("//span[@class='select2-results']/ul[@id='select2-results-per-page-select-results']")
    alloptions=css.find_elements_by_tag_name("li")
    for option in alloptions:
        if "100" in option.text:
            option.click()
            break
    results=driver.find_element_by_id("results-count").get_attribute('textContent')
    countS=re.sub("\D", "",results)
    print(countS)
    countI=int(countS)
    if(countI<=500):
        print("数据数量小于等于500")
        print("采用一次下载模式")
        js="document.getElementById('select-page-arrow').click()"
        driver.execute_script(js)
        # js="document.getElementById('select-max').click()"
        # driver.execute_script(js)
        # wait_by_id(driver,"select-page-arrow","waiting for select-page")
        # driver.find_element_by_id("select-page-arrow").click()
        wait_by_id(driver,"select-max","waiting for select-max")
        driver.find_element_by_id("select-max").click()
        
        js = "document.getElementsByClassName('modal-backdrop fade in')[0].setAttribute(\"class\",\"\")"
        driver.execute_script(js)
        
        wait_by_id(driver,"select-max-confirm","waiting for confirm")
        js="document.getElementById('select-max-confirm').click()"
        driver.execute_script(js)       
        #driver.find_element_by_id("select-max-confirm").click()
        sleep(15)
        wait_by_xpath(driver,"//a[@id='downloadlink']/span[@class='ss-download']","waiting for download")    
        driver.find_element_by_xpath("//a[@id='downloadlink']/span[@class='ss-download']").click()
        
        wait_by_id(driver,"rdAsc","waiting for setting")
        js="document.getElementById('rdAsc').click()"
        driver.execute_script(js)
        js="document.getElementById('rdDet').click()"
        driver.execute_script(js)
        js="document.getElementById('clearBasket').click()"
        driver.execute_script(js)           
        driver.find_element_by_id("savePrefsButton").click()
        
    if(countI>500):
        print("数据数量大于500")
        print("采用多次下载模式")
        js="document.getElementById('select-page-arrow').click()"
        driver.execute_script(js)
        # js="document.getElementById('select-max').click()"
        # driver.execute_script(js)
        # wait_by_id(driver,"select-page-arrow","waiting for select-page")
        # driver.find_element_by_id("select-page-arrow").click()
        wait_by_id(driver,"select-max","waiting for select-max")
        driver.find_element_by_id("select-max").click()
        
        js = "document.getElementsByClassName('modal-backdrop fade in')[0].setAttribute(\"class\",\"\")"
        driver.execute_script(js)

        wait_by_id(driver,"select-max-confirm","waiting for confirm")
        js="document.getElementById('select-max-confirm').click()"
        driver.execute_script(js)
        # driver.find_element_by_id("select-max-confirm").click()
        sleep(15)
        wait_by_xpath(driver,"//a[@id='downloadlink']/span[@class='ss-download']","waiting for download")    
        driver.find_element_by_xpath("//a[@id='downloadlink']/span[@class='ss-download']").click()
        
        wait_by_id(driver,"rdAsc","waiting for setting")

        js="document.getElementById('rdAsc').click()"
        driver.execute_script(js)
        js="document.getElementById('rdDet').click()"
        driver.execute_script(js)
        js="document.getElementById('clearBasket').click()"
        driver.execute_script(js)
        sleep(2)
        js="document.getElementById('savePrefsButton').click()"
        driver.execute_script(js)    
        sleep(15)
        results=driver.find_element_by_xpath("//div[@id='page-nav']/span[@class='page-count']").get_attribute('textContent')
        print("a="+results)
        recentpage=str(results[1])
        maxpage=str(results[6]+results[7])
        print("recentpage="+recentpage)
        print("maxpage="+maxpage)
        recentpage=int(recentpage)
        maxpage=int(maxpage)
        driver.find_element_by_id("next-page-top").click()    
        while recentpage<5:            
            wait_by_id(driver,"detaillink_%d01"%recentpage,"waiting for next-page")  
            driver.find_element_by_id("next-page-top").click()    
            recentpage=recentpage+1
        while recentpage<maxpage:                      
            wait_by_id(driver,"detaillink_%d01"%recentpage,"waiting for next-page")  
            js="document.getElementById('page-select').click()"
            driver.execute_script(js)
            sleep(2)
            results=driver.find_element_by_xpath("//div[@id='ev-sub-nav-header']/ul/li[@id='ev-navigation-header-selectedrecords-section']/a/span[@class='ev-badge ev-hide']").get_attribute('textContent')
            print("Select Results="+results)            
            Iselect=int(results)
            recentpage=recentpage+1
            print("Recentpage=%d"%recentpage)          
            if Iselect==400:
                sleep(2)
                results=driver.find_element_by_xpath("//div[@id='ev-sub-nav-header']/ul/li[@id='ev-navigation-header-selectedrecords-section']/a/span[@class='ev-badge ev-hide']").get_attribute('textContent')
                print("Select Results="+results) 
                Iselect=int(results)        
            if Iselect==500:
                driver.find_element_by_id("oneclickDL").click()    
                sleep(15)
            if recentpage==maxpage:
                driver.find_element_by_id("oneclickDL").click()    
                sleep(15) 
            else:            
                driver.find_element_by_id("next-page-top").click()
    #driver.save_screenshot('1.png')
    #driver.quit()
def usage():
    print ("                                                    ")  
    print ("********************************************************")
    print ("************      Rubb1shK1d 版权所有       ************")
    print ("*********             爬虫命令举例             *********")
    print ("********************************************************")    
    print ("python crawler.py -h  使用帮助"  )
    print ("python crawler.py --help " )
    print ("————————————————————————————" )
    print ("python crawler.py -a word word starttime endtime"  )
    print ("python crawler.py --author word word starttime endtime"  )
    print ("————————————————————————————" )
def main():     
    # 读取命令行选项,若没有该选项则显示用法  
    try:  
        # opts：一个列表，列表的每个元素为键值对  
        # args:其实就是sys.argv[1:]  
        # sys.argv[1:]：只处理第二个及以后的参数  
        # "ts:h"：选项的简写，有冒号的表示后面必须接这个选项的值（如 -s hello）  
        # ["help", "test1", "say"] :当然也可以详细地写出来，不过要两条横杠（--）  
        opts, args = getopt.getopt(sys.argv[1:], "a:h",["help", "author"]) 
        # 具体处理命令行参数
        if len(args)==0:
            usage()
        else:
            for o,v in opts:                    
                if o in ("-h","--help"):  
                    usage()  
                elif o in ("-a", "--author"):                
                    search(sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
                    
    except getopt.GetoptError:  
        # print str(err)  
        usage()  
main()