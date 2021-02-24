from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random,time,bot_messenger

class flipkart():
    def __init__(self,u,p,ui,a,c,w,r,link,id):
        self.user=u
        self.pwd=p
        self.upi=ui
        self.url=link
        self.api=a
        self.group=c
        self.wait=w
        self.retry=r
        self.id=id
        self.done=False

    def sign_in(self,browser):
        for i in range(self.retry):
            if i+1==self.retry:
                return False
            try:
                browser.find_element_by_class_name('_1_3w1N').click()
                break
            except:
                print(self.id+' : cannot find button to login..will retry')
                time.sleep(self.wait)
        for i in range(self.retry):
            if i+1==self.retry:
                return False
            try:
                fields=browser.find_elements_by_class_name('VJZDxU')
                break
            except:
                print(self.id+' : cannot locate text fields to enter data...will retry')
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
                print(self.id+' : could not click on Login Button...will retry')
                time.sleep(self.wait)
        return True

    def next(self,browser):
        for i in range(self.retry):
            if i+1==self.retry:
                return False
            try:
                browser.find_element_by_class_name('_3AWRsL').click()
                break
            except:
                print(self.id+' : could not find button to click..will try again')
                time.sleep(self.wait)
        return True

    def check_availability(self,browser):
        self.item=browser.find_element_by_class_name('B_NuCI').text
        for i in range(self.retry):
            if i+1==self.retry:
                return False
            try:
                browser.find_element_by_class_name('_3AWRsL').click()
                break
            except:
                print(self.id+' : item not available..will try again')
                time.sleep(random.randint(5,10))
        try:
            browser.find_element_by_class_name('_1bS9ic').click()
        except:
            print(self.id+' : could not click on "cart" button..server is automatically redirecting there')
        return True

    def start_buy(self,browser):
        print(self.id+' : starting buy procedure...')
        print(self.id+' : selecting first available delivery address')
        if self.next(browser):
            time.sleep(self.wait)
        else:
            return False

        print(self.id+' : finalising order...')
        if self.next(browser):
            time.sleep(self.wait)
        else:
            return False

        print(self.id+' : choosing UPI option')
        for i in range(self.retry):
            if i+1==self.retry:
                return False
            try:
                browser.find_elements_by_class_name('_1XFPmK')[2].click()
                break
            except:
                print(self.id+' : could not locate upi option..will try again')
                time.sleep(self.wait)

        for i in range(self.retry):
            if i+1==self.retry:
                return False
            try:
                browser.find_elements_by_class_name('_1BtQO5')[1].click()
                break
            except:
                print(self.id+' : could not locate upi option..will try again')
                time.sleep(self.wait)


        for i in range(self.retry):
            if i+1==self.retry:
                return False
            try:
                browser.find_element_by_class_name('_2mFmU7').send_keys(self.upi)
                break
            except:
                print(self.id+' : could not locate upi option...will try again')
                time.sleep(self.wait)

        for i in range(self.retry):
            if i+1==self.retry:
                return False
            try:
                browser.find_element_by_class_name('_2-Y9bv').click()
                break
            except:
                print(self.id+' : could not click on verify')
                time.sleep(self.upi)

        print(self.id+' : upi verified...proceed to click on Pay')
        if self.next(browser):
            self.t_message='Complete your UPI Payment from Flipkart\nAccount - '+self.user+'\nUPI - '+self.upi+'\nProduct - '+self.item
            self.done=True
            print(self.id+' : item ordered...complete your UPI payment')
        else:
            return False
        return True

    def run(self):
        browser=webdriver.Firefox()
        browser.get(self.url)
        
        if self.sign_in(browser):
            print(self.id + ' : succefully signed in to '+self.user)
            time.sleep(2)
            if self.check_availability(browser):
                time.sleep(self.wait)
                if self.start_buy(browser):
                    if self.done:
                        bot_messenger.telegram(self.t_message,self.api,self.group)
                    else:
                        print(self.id+' : item ordered...but could not send telegram message')
                else:
                    print(self.id+' : max retry limit exceeded..increase wait time or retry count and try again! ')
            else:
                print(self.id+' : sorry item not available...run again or increase retry count in config.ini')
        else:
            print(self.id+' : sign in failed...something went wrong')
