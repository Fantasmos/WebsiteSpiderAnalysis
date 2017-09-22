import stringutilities
import httputilities
import FileEditor
import json
import os.path


def ConvertFoodToCSVLine(Jsonfile):
    with open(Jsonfile) as data_file:    
        data = json.load(data_file)
        AllValuesAsSingleLine = ""
        
        Name = data["Name"][0] 
        AllValuesAsSingleLine +=  '"' + Name +  '"' + ", " 

        Price = data["Price"][0].split("\n")[0]
        Price = Price.replace("$ ", "")
        Price = Price.replace(" ", ".")
        AllValuesAsSingleLine += Price + ", "
        
        for value in data["WantedData1"]:
            AllValuesAsSingleLine += value + ", "
        for value in data["WantedData2"]:
            SeperatedValues = value.replace("\u2013 ", "") 
            SeperatedValues = SeperatedValues.replace(" ", ", ") 
            SeperatedValues = SeperatedValues.replace(",,", ",") 
            AllValuesAsSingleLine += SeperatedValues + ", "
           
        return AllValuesAsSingleLine





'''Get All Food Pages '''
def SaveAllFoodPagesToFile(driver, Append, ListOfUrls, MustStartWith, file):
    
    
    for key, value in ListOfUrls.items():
        DeadLink = False
        iterator = 0

        
      
        while (DeadLink == False):
            DeadLink = True
            UrlToOpen = value + Append + str(iterator)
            AllLinksOnPage = httputilities.GetAllUrlsOnPage(driver , UrlToOpen)
            LastAdded = None

            for Entry in AllLinksOnPage:
                
                '''See if we can find the next page link on the page''' 
                if Entry.startswith(value + Append):
                    Number = Entry[len(value + Append):]
                    
                    try:
                        Number = int(Number)
                        if Number > iterator:
                            DeadLink = False
                            print("Not dead!")
                    except:
                        print("Error occured, just ignore")


                if Entry.startswith(MustStartWith ):
                    if (driver.current_url == UrlToOpen):
                        if (Entry != LastAdded):
                            FileEditor.AppendToFile(file , Entry)
                            LastAdded = Entry

            iterator = iterator + 1

        print("Finished This one, ended at: ")
        print(iterator)
        FileEditor.AppendToFile("AllCategoryPages.txt" , UrlToOpen)
   

def CleanupResposne(input):
    input = input.replace('&', '')
    input = input.replace(' ', '-')
    input = input.replace("--" , "-")
    input = input.replace(",-" , "-")
    input = input.lower()
    AllPages = input.split('\n')
    return AllPages


def FileExists (file):
    return os.path.isfile(file)

def SaveElementsOfEachPageInFile(Driver, Sourcefile, ElementsToGet, StartAt = 0):
    
    i = 0

    with open(Sourcefile) as f:
        
        for line in f:
            filename = str(i) + ".json"
            if (i >= StartAt) & (FileExists(filename) == False) :
                AllNutrition = httputilities.GetAllOfClassesOnPage(Driver, line, ElementsToGet)
                with open(filename , 'w') as fp:
                    json.dump(AllNutrition, fp)
                    print("Saved to: " + filename)
            i = i + 1




def main(startat = 0):
    driver = httputilities.Setupbrowser()


    '''Get all categories by parsing navigation-bar'''
    MainWebPage = "https://www.website.com.au/shop/"
    StartDelim = 'StartDelim":"'
    EndDelim = '",'

    MainPage = httputilities.GetDivOfPageAsText(driver , MainWebPage,"categoryHeader-navigation")
    AllCategoryNames = CleanupResposne(MainPage)

    ListOfUrls = {}
    for CategoryName in AllCategoryNames :
        ResolvedURL = MainWebPage + "browse" + '/' + CategoryName
        ListOfUrls[CategoryName] = ResolvedURL



    '''Get All pages that contain products by going through each page of each category'''
    AllPagesFileLocation = "AllPages.txt"
    Append = '?pageNumber='
    MustStartWith = 'https://www.website.com.au/shop/details/'
    SaveAllFoodPagesToFile(driver, Append, ListOfUrls, MustStartWith , AllPagesFileLocation)




    '''Open Each page, and save to a seperate file'''
    AllElements = ["price", "WantedData1", "WantedData2"]
    SaveElementsOfEachPageInFile(driver, AllPagesFileLocation, AllElements, startat)
    
    subfolder = "foods"
    iterator = 0
    '''Open Each File and Parse into excel'''
    for filename in os.listdir(subfolder):
        iterator = iterator + 1
        try:
            line = ConvertFoodToCSVLine(filename)
            f = open("AllFoods", "a+")
            f.write(line + "\n")
        except :
            f = open("ERRORS", "a+")
            f.write(filename + "\n")
        
    