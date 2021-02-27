from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random,time,bot_messenger

class flipkart():
    def __init__(self,u,p,ui,a,c,w,r,link,id,wb):
        self.user=u
        self.pwd=p
        self.upi=ui
        self.url=link
        self.api=a
        self.group=c
        self.wait=w
        self.retry=r
        self.id=id
        self.type=wb
        self.done=False

    def __out(self,text):
        print(self.id+' : '+text)
### sign in
    def __sign_in(self,browser):
        for i in range(self.retry):
            if i+1==self.retry:
                return False
            try:
                browser.find_element_by_class_name('_1_3w1N').click()
                break
            except:
                self.__out('cannot find button to login..will retry')
                time.sleep(self.wait)
        for i in range(self.retry):
            if i+1==self.retry:
                return False
            try:
                fields=browser.find_elements_by_class_name('VJZDxU')
                break
            except:
                self.__out('cannot locate text fields to enter data...will retry')
                time.sleep(self.wait)
        usr=fields[0]
        pas=fields[1]
        usr.clear()
        for letter in self.user:
            usr.send_keys(letter)
            time.sleep(0.2)
        for letter in self.pwd:
            pas.send_keys(letter)
            time.sleep(0.2)
        for i in range(self.retry):
            if i+1==self.retry:
                return False
            try:
                browser.find_element_by_class_name('_1D1L_j').click()
                break
            except:
                self.__out('could not click on Login Button...will retry')
                time.sleep(self.wait)
        return True

### INTERNAL USE ONLY - click on continue
    def __next(self,browser):
        for i in range(self.retry):
            if i+1==self.retry:
                return False
            try:
                browser.find_element_by_class_name('_3AWRsL').click()
                break
            except:
                self.__out('could not find button to click..will try again')
                time.sleep(self.wait)
        return True

### check item availability    
    def __check_availability(self,browser):
        self.item=browser.find_element_by_class_name('B_NuCI').text
        for i in range(self.retry):
            if i+1==self.retry:
                return False
            try:
                browser.find_element_by_class_name('_3AWRsL').click()
                break
            except:
                self.__out('item not available..will try again')
                time.sleep(random.randint(5,10))
        try:
            browser.find_element_by_class_name('_1bS9ic').click()
        except:
            self.__out('could not click on "cart" button..server is automatically redirecting there')
        return True

### start buying process    
    def __start_buy(self,browser):
        self.__out('starting buy procedure...')
        self.__out('selecting first available delivery address')
        if self.__next(browser):
            time.sleep(self.wait)
        else:
            return False

        self.__out('finalising order...')
        if self.__next(browser):
            time.sleep(self.wait)
        else:
            return False

        self.__out('choosing UPI option')
        for i in range(self.retry):
            if i+1==self.retry:
                return False
            try:
                browser.find_elements_by_class_name('_1XFPmK')[2].click()
                break
            except:
                self.__out('could not locate upi option..will try again')
                time.sleep(self.wait)

        for i in range(self.retry):
            if i+1==self.retry:
                return False
            try:
                browser.find_elements_by_class_name('_1BtQO5')[1].click()
                break
            except:
                self.__out('could not locate upi option..will try again')
                time.sleep(self.wait)


        for i in range(self.retry):
            if i+1==self.retry:
                return False
            try:
                browser.find_element_by_class_name('_2mFmU7').send_keys(self.upi)
                break
            except:
                self.__out('could not locate upi option...will try again')
                time.sleep(self.wait)

        for i in range(self.retry):
            if i+1==self.retry:
                return False
            try:
                browser.find_element_by_class_name('_2-Y9bv').click()
                break
            except:
                self.__out('could not click on verify')
                time.sleep(self.upi)

        self.__out('upi verified...proceed to click on Pay')
        if self.__next(browser):
            self.t_message='Complete your UPI Payment from Flipkart\nAccount - '+self.user+'\nUPI - '+self.upi+'\nProduct - '+self.item
            self.done=True
            self.__out('item ordered...complete your UPI payment')
        else:
            return False
        return True

### public rule to start above processes
    def run(self):
        try:
           if(self.type=='Chrome'):
               browser=webdriver.Chrome()
           elif(self.type=='Firefox'):
               browser=webdriver.Firefox()
           elif(self.type=='Edge'):
               pass
        except:
           self.__out('your OS does not contain Chrome,Edge or Firefox, please install one ,make it default and try again/nif you already have Edge kindly check your edge version number and download selenium edgedriver\nagainst that version number and paste it in application path')
           return

        browser.get(self.url)
        
        if self.__sign_in(browser):
            print(self.id + ' : succefully signed in to '+self.user)
            time.sleep(2)
            if self.__check_availability(browser):
                time.sleep(self.wait)
                if self.__start_buy(browser):
                    if self.done:
                        bot_messenger.telegram(self.t_message,self.api,self.group)
                    else:
                        self.__out('item ordered...but could not send telegram message')
                else:
                    self.__out('max retry limit exceeded..increase wait time or retry count and try again! ')
            else:
                self.__out('sorry item not available...run again or increase retry count in config.ini')
        else:
            self.__out('sign in failed...something went wrong')
