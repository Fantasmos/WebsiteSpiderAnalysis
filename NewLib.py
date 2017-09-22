from selenium import webdriver

def GetDivOfPage(driver, url, divname):
    data = driver.get(url) #navigate to the page
    item = driver.find_element_by_class_name(divname)
    url = "https://stackoverflow.com/questions/7862018/how-to-convert-upper-case-letters-to-lower-case"
    driver.get(url) 

    return item

def Setupbrowser():
    
      
    return driver