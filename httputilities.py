from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import time


import urllib.request

def Setupbrowser ():
    chromeOptions = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images":2}
    chromeOptions.add_experimental_option("prefs",prefs)
    driver = webdriver.Chrome(chrome_options=chromeOptions)
    driver.maximize_window()
    
    return driver

def getpage (browser, url):
    browser.maximize_window()
    browser.get(url)
    return browser

def GetDivOfPageAsText(browser, url, divname):
    text = None
    try:
        browser = getpage(browser, url) 
        item = browser.find_element_by_class_name(divname)
        text = item.text
    except:
        print("ERROR") 
    finally:
        return text

    
def GetAllUrlsOnPage(browser, url):
    links = []
    try:
        browser = getpage(browser, url) 
        time.sleep(3)
        AllLinks = browser.find_elements_by_xpath("//*[@href]")
        for item in AllLinks: 
            foodpage = item.get_attribute('href')
            links.append(foodpage)
    finally:
        return links

def GetAllOfClassesOnPage(browser, url, ClassNames):
    browser = getpage(browser, url) 
    ReturnValues = {}

    for ClassTofind in ClassNames:
        try:
            AllElements = browser.find_elements_by_class_name(ClassTofind)
            Values = list()

            for Element in AllElements:
                Values.append(Element.text)

            ReturnValues[ClassTofind] = Values
        except: 
            print("Couldn't find each item on page: " + url)

    return ReturnValues

    "productDetail-nutritionTableColumn"
def GetWebPage(url):
    page = None
    Response = urllib.request.urlopen(url)
    try:
        Response = urllib.request.urlopen(url)
        encoding = Response.headers.get_content_charset('utf-8')
        page = Response.read().decode(encoding)
    finally:
        return page
        
