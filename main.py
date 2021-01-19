from selenium import webdriver
import time
import random
import fileinput

#variables
fbit_addr = "addr.txt"
fname = "out.txt"
fconf = "conf.txt"

#directories
auth_url = "https://oxt.me/auth"


def get_urls():
    f = open(fname,"r")
    lst = list()
    for ln in f:
        lst.append(ln)
    return lst

def get_last_pos():
    f = open(fconf)

    for l in f:
        s = str(l)
        s.strip()
        #print(s)
        param = "last_count ="
        index = s.find(param) #9
        #print(index)
        if index != -1:
            s = s[len(param):len(s)]
            return int(s)
        else:
            return 0

def set_seed():
    random.seed(time.ctime())

def get_rand_delay():
    return random.randint(30,50)

def auth(dr):
    dr.get(auth_url)
    time.sleep(4)
    login = dr.find_element_by_id("auth-login")
    login.send_keys("kirch")
    time.sleep(5)
    passwd = dr.find_element_by_id("auth-new-password")
    passwd.send_keys("!3BMwZF4nJTjkZc")
    time.sleep(2)
    login_btn = dr.find_element_by_id("signin-btn")
    login_btn.click()
    time.sleep(5)

def update_last_count(count):
    f = open(fconf,"w")
    f.write("last_count ="+str(count))
    f.close()
    # s = str()
    # s_all = str()
    # for line in f:
    #     s = str(line)
    #     if s.find("last_count =") != -1:
    #         s_all = str(line)
    #         break
    # f.close()


def get_addrs(dr,urls_lst,last_c):     
     for i in range(last_c,len(urls_lst)):
         update_last_count(i)
         web_addr_list = list()
         delay = get_rand_delay()
         print("i = " + str(i))
         print("delay = " + str(delay))
        
         time.sleep(delay)
         dr.get(urls_lst[i])
         time.sleep(20)
        
         # addr_tab
         btn = dr.find_element_by_xpath('//*[@id="AddressTab"]/li[8]/a')
         btn.click()
         time.sleep(get_rand_delay())
         
         #addr_list - заполнение адресами
         web_addr_list = dr.find_elements_by_css_selector("table.table-data.spaced tbody tr td:nth-child(1) a:nth-child(1)")
         print(len(web_addr_list))
         if (len(web_addr_list) != 0):
             sr = str(web_addr_list[0].get_attribute("title"))
             if sr.find("Go to address") == -1:
                 web_addr_list = list()
             else:
                print("addr_list len = " + sr)
        
         trying = 0
         max_tcount = 3

         #waiting for loading addressies
         while ((len(web_addr_list) == 0) and (trying < max_tcount)):
             dr.get(urls_lst[i])
             time.sleep(40)
             # addr_tab
             btn = dr.find_element_by_xpath('//*[@id="AddressTab"]/li[8]/a')
             btn.click()
             time.sleep(get_rand_delay())
             web_addr_list = dr.find_elements_by_css_selector("table.table-data.spaced tbody tr td:nth-child(1) a:nth-child(1)")
             print("addr_list len = "+str(len(web_addr_list)))
             if (len(web_addr_list) != 0):
              sr = str(web_addr_list[0].get_attribute("title"))
              if sr.find("Go to address") == -1:
                 web_addr_list = list()
             trying += 1
             print("trying count = " + str(trying))



         if trying != max_tcount:
             #el_title = lst[i].get_attribute("title")
             #print(el_title)
             #entity_name = str()
             #el = dr.find_element_by_xpath('//*[@id="entity"]/div[5]/entity-header-view/div/h2')
             #entity_name = el.get_attribute("text")
             print("entity name = " + entity_name+"\n")

             if len(web_addr_list) > 15:
                 f = open(fbit_addr,"a")
                 #f.write("\n\n"+urls_lst[i]+":\n")
                 f.write("\n\n"+entity_name+":\n")
                 s = str()
                 s = web_addr_list[0].get_attribute("title")
                 s = s.replace('Go to address','') #посмотреть как возвращает сайт
                 print(s)
                 f.write(s+"\n")
                 # f.write(addr_list[0]+"\n")
                 f.close()
             else:
                 f = open(fbit_addr,"a")
                 f.write("\n\n"+urls_lst[i]+":\n")
                 s = str()
                 for j in range(0,len(web_addr_list)):
                     s = web_addr_list[j].get_attribute("title")
                     s = s.replace('Go to address','')
                     f.write(s+"\n")
                 f.close()
             #update_last_count(i)


        
         


def main() :
    set_seed()
    driver = webdriver.Firefox()
    auth(driver)
    urls_lst = get_urls()
    urls_count = len(urls_lst)
    last_pos = get_last_pos() 
    print(urls_count)
    get_addrs(driver,urls_lst,last_pos)
    # print()
    # print(get_last_pos())


    auth(driver)








if __name__ == "__main__" :
    main()