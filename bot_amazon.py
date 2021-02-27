from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bot_messenger,time,random

class amazon():
    def __init__(self,u,p,ui,a,c,w,r,link,id,wb):
        self.user=u
        self.pwd=p
        self.upi=ui
        self.api=a
        self.group=c
        self.wait=w
        self.retry=r
        self.url=link
        self.id=id
        self.type=wb
        self.done=False

    def __out(self,text):
        print(self.id+' : '+text)

### initiate sign in process
    def __sign_in(self,browser):
        self.__out('starting login procedure...')
        for i in range(self.retry):
            if i+1 == self.retry:
                self.__out('max retry limit reached...exiting process')
                return False
            try:
                browser.find_element_by_id('nav-link-accountList-nav-line-1').click()
                break
            except:
                self.__out('could not find button to login..will retry')
                time.sleep(self.wait)
        
        for i in range(self.retry):
            if i+1 == self.retry:
                self.__out('max retry limit reached...exiting process')
                return False
            try:
                em=browser.find_element_by_id('ap_email')
                break
            except:
                self.__out('could not find text field...will retry')
                time.sleep(self.wait)
        self.__out('entering username...')
        for letter in self.user:
            em.send_keys(letter)
            time.sleep(0.2)
        em.send_keys(Keys.RETURN)
        
        for i in range(self.retry):
            if i+1 == self.retry:
                self.__out('max retry limit reached...exiting process')
                return False
            try:
                pas=browser.find_element_by_id('ap_password')
                break
            except:
                self.__out('could not find password field...will retry')
                time.sleep(self.wait)
        self.__out('entering password...')
        for letter in self.pwd:
            pas.send_keys(letter)
            time.sleep(0.2)

        try:
            browser.find_element_by_id('signInSubmit').click()
        except:
            return False
        return True

### check product availability
    def __check_availability(self,browser):
        for i in range(self.retry):
            if i+1 == self.retry:
               return False
            try:
                but=browser.find_element_by_id("add-to-cart-button")
                break
            except:
                try:
                    but=browser.find_element_by_id('a-autoid-0-announce')
                    break
                except Exception as e:
#                    print(e)
                    time.sleep(self.wait)
        if but.text == 'Join Prime':
            return False
        else:
            try:
                but.click()
            except:
                self.__out('cannot click on button...need human help!!')
                return False
        self.__out('item is being added to cart')
        try:
            browser.find_element_by_id('nav-cart').click()
        except:
            self.__out('could not click on "go to cart" browser is automatically redirecting')
        return True

    def __next(self,browser):
        for i in range(self.retry):
            try:
                browser.find_elements_by_xpath('//input[@value="Continue"]')[0].click()
                return True
            except:
                time.sleep(self.wait)
        return False

### start process to buy product
    def __start_buy(self,browser):
#       in cart - clicking proceed to buy button
        for i in range(self.retry):
            if i+1 == self.retry:
                return False
            try:
                browser.find_element_by_id('sc-buy-box-ptc-button').click()
                break
            except:
                self.__out('could not find button to click')
                time.sleep(self.wait)
        time.sleep(1)
#       if prompted to re-enter password
        try:
            text=browser.find_element_by_id('a-spacing-small').text
        except:
            text=''
        if text:
            field=browser.find_element_by_id('ap_password')
            for letter in self.pwd:
                field.send_keys(letter)
                time.sleep(0.2)
            browser.find_element_by_id('signInSubmit').click()

#       deliver here button
        for i in range(self.retry):
            if i+1 == self.retry:
                self.__out('max retry limit exceeded')
                return False
            try:
                browser.find_elements_by_xpath('//a[@data-action="page-spinner-show"]')[0].click()
                break
            except Exception as e:
                self.__out('error - '+str(e))
                time.sleep(self.wait)

        time.sleep(3)
#       if prompted directly to coninue
        self.__next(browser)

#       upi option
        for i in range(self.retry):
            if i+1 == self.retry:
                self.__out('could not find upi option...retry limit exceeded')
                return False
            try:
                browser.find_elements_by_xpath('//input[@name="ppw-instrumentRowSelection"]')[4].click()
                break
            except:
                time.sleep(self.wait)

#       upi entry field
        for i in range(self.retry):
            if i+1== self.retry:
                self.__out('could not find text field to enter upi...retry limit exceeded')
                return False
            try:
                upi_entry=browser.find_element_by_xpath('//input[@placeholder="Ex: MobileNumber@upi"]')
                break
            except:
                time.sleep(self.wait)

#       enter upi id
        upi_entry.send_keys(self.upi)

#       verify
        for i in range(self.retry):
            if i+1==self.retry:
                self.__out('retry limit exceeded')
                return False
            try:
                browser.find_elements_by_class_name('a-button-inner')[4].click()
                break
            except:
                time.sleep(self.wait)

#       continue
        for i in range(self.retry):
            if i+1==self.retry:
                self.__out('retry limit exceeded')
                return False
            try:
                browser.find_elements_by_class_name('a-button-inner')[5].click()
                break
            except:
                time.sleep(self.wait)
        

#       only for non prime users
        for i in range(self.retry):
            if i+1==self.retry:
                self.__out('do not opt for prime - retry limit exceeded')
            try:
                browser.find_element_by_id('prime-interstitial-nothanks-button').click()
                break
            except:
                time.sleep(self.wait)
        

#       place order and pay button
        for i in range(self.retry):
            if i+1==self.retry:
                self.__out('retry limit exceeded')
                return False
            try:
                browser.find_element_by_xpath('//input[@value="Place Your Order and Pay"]').click()
                break
            except:
                time.sleep(self.wait)
        

        self.t_message='Complete you UPI payment from Amazon\nAccount - '+self.user+'\nUpi-id - '+self.upi+'\nProduct - '+self.item
        self.done=True
        print('Process Complete!!')
        return True
    
    def __get_title(self,browser):
        try:
            self.item=browser.find_element_by_id('productTitle').text
            return True
        except:
            self.item='could not fetch item name'
            return False

### public fuction to intiate all processes
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
        self.__get_title(browser)
        
        if self.__sign_in(browser):
            while not self.__check_availability(browser):
                print(self.id+' : item not available yet try again later')
                time.sleep(random.randint(5,10))
                browser.refresh()
            if self.__start_buy(browser):
                if self.done:
                    print(self.id+' : complete your Upi payment...sending telegram message')
                    bot_messenger.telegram(self.t_message,self.api,self.group)
                else:
                    print(self.id+' : process complete but could not send telegram message')
            else:
                print(self.id+' : something went wrong...try again after changing wait time or retry count')
        else:
            print(self.id+' : sign in failed...try again!')


