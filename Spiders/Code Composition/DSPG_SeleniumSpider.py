import selenium
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from os import path
import time
import sys

#This class reduces common code through out each Selenium Spider
#It is made to assist you and is extremely helpful when debugging!
class SeleniumSpider():
    spiderLogs = []         #The logs 

    #These are methods that are available for your convences
    def log(self, *args):
        self.spiderLogs.append(('Logger:', args))
        if self.LOGGER:
            print('Logger:', *args)

    def debug(self, *args):
        self.spiderLogs.append(('Debug:', args))
        if self.DEBUGGER:
            print('Debug:', *args)
    
    def printer(self, *args):
        self.spiderLogs.append(('Printer:', args))
        print(*args)
    
    def printLogs(self):
        print("\n< --- Printing Logs --- >\n")
        for entry in self.spiderLogs:
            print(*entry)

    def Logs_to_file(self, filename):
        with open(filename, 'w') as file:
            for log_entry in self.spiderLogs:
                file.write('{} {}\n'.format(log_entry[0], log_entry[1]))

    def __init__(self):
        self.DEBUGGER = True #The debugger switch to see whats going on. The Default is True
        self.LOGGER = True #When you need to see everything that happends. The Default is True
        self.attempts = 3 #The number of attempts the spider can retry if an error occurs. Default is 3
        self.waitTime = 10 #The number of seconds WebDriver will wait. Default is 10
        self.count = 0 #This saves the location of the url we are going through
        self.runTime = 0 #Total time of extractions
        self.totalRecoveries = 0 #Number of recoveries made while running
        self.maxRetryCount = 100 #Number of retrys the javascript can make Defualt is 100
        #Selenium needs a webdriver to work. I chose Firefox however you can do another if you need too
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install(), log_path=path.devnull))
        self.log("Driver started")

    #This handles the restart in case we run into an error
    def restart(self):
        self.driver.quit()
        self.driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install(), log_path=path.devnull))
        self.log("Driver restarted")
    #Returns data
    def requests(self, xpath, url, driver):
        #Retrying the xpath given the number of attempts
        for attempt in range(self.attempts):
            data = self.javascriptXpath(xpath[0],driver)
            if data in {'empty', 'skip'}:
                #speical case in case you need it
                if len(xpath) == 3:
                    if xpath[2]:
                        if attempt == 0:
                           self.debug("Found a speical case double checking")
                           continue
                        #example would be when there is actually is a '' in the xpath
                        #or a product is not in stock
                        self.debug("xpath marked as speical")
                        return 'speical'
                if xpath[1] and data == 'empty':    
                    #this is where setting the xpath to optional comes in
                    self.debug("xpath wasnt avaliable")
                    return None 
                self.debug("Missing item retrying")
            else:  #Data found
                self.log(data + ' was added to the list for: ', url)
                return data
        return 'skip'

    #Collecting the data from the xpath in JavaScript is faster and results in fewer errors than doing it in python
    #This is where selenium shines because we can both use JavaScript and render JavaScript websites
    #and is the only reason why we use it instead of scrapy
    def javascriptXpath(self, xpath, driver):
        # if the time expires it assumes xpath wasnt found in the page
        try: 
            #Waits for page to load 
            ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)
            elements = WebDriverWait(driver, self.waitTime, ignored_exceptions=ignored_exceptions).until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

            # Runs the javascript and collects the text data from the inputed xpath
            # We want to keep repeating if we get any of these outputs becasue the page is still 
            # loading and we dont want to skip or waste time. (for fast computers)
            retrycount = 0
            invalidOutputs = {"error", 'skip' "$nan", ''}
            while retrycount < self.maxRetryCount :
                text = self.driver.execute_script("""
                    const element = document.evaluate(arguments[0], document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;
                    if (!element) {
                        return 'skip';
                    }
                    return element.textContent.trim();
                """, 
                xpath)
                checkText = text.replace(" ", "").lower()
                if checkText in invalidOutputs:
                    retrycount+=1
                else:
                    self.log(retrycount, "xpath attempts for (", text, ")")
                    return text
            self.log("xpath attempts count met. Problematic text (" + text + ") for ", xpath)
            return 'skip'
        except TimeoutException:
            self.log('Could not find xpath for: ', xpath)
            return 'empty'
