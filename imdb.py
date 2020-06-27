from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import csv
import sys
import time

#Path for the browser
PATH = "C:\Program Files (x86)\chromedriver.exe"

#Fix here for keyword
KW = "trying on clothes"

#Fix here for file name
FILENAME = "mov"

#When scraping years, there were a lot of strange patterns so i had to fix them with 'yearFixer' method
def yearFixer(year):

    #Finds all digits in year string
    x = re.findall("\d", year)
    try:
        if len(x) == 4:
            #Finds out if there is a '–'' next to 4 digits
            y = re.findall("[0-9][0-9][0-9][0-9][–]", year)

            #If there is not return 4 digits
            if not y:
                t = x[0]+x[1]+x[2]+x[3]
                return t

            #If there is return 4 digits and '–'
            else:
                return y[0]

        #If year string is '-' there is nothing to fix
        elif year=="-":
            return year

        #Otherwise find a pattern like 'dddd–dddd' and return it
        else:
            y = re.findall("[0-9][0-9][0-9][0-9][–][0-9][0-9][0-9][0-9]", year)
            return y[0]

    #If any error occurs in the code above just return '-'
    except:
        return "-"

def mainAlgorithm(r, writer):
    for i in range(0, r):

        #Scrapes the name
        try:
            name = driver.find_element_by_xpath("//*[@id=\"main\"]/div/div[2]/div[3]/div[" + str(i+1) + "]/div[2]/h3/a").text
        except:
            name = "-"
                
        #Scrapes the year
        try:
            year = driver.find_element_by_xpath("//*[@id=\"main\"]/div/div[2]/div[3]/div[" + str(i+1) + "]/div[2]/h3/span[@class=\"lister-item-year text-muted unbold\"]").text
        except:
            year = "-"
        fixedYear = yearFixer(year)

        #Scrapes the movie time
        try:
            movieTime = driver.find_element_by_xpath("//*[@id=\"main\"]/div/div[2]/div[3]/div[" + str(i+1) + "]/div[2]/p[1]/span[@class=\"runtime\"]").text
        except:
            movieTime = "-"

        #Scrapes the genre
        try:
            genre = driver.find_element_by_xpath("//*[@id=\"main\"]/div/div[2]/div[3]/div[" + str(i+1) + "]/div[2]/p[1]/span[@class=\"genre\"]").text
        except:
            genre = "-"

        #Scrapes the rating
        try:
            rating = driver.find_element_by_xpath("//*[@id=\"main\"]/div/div[2]/div[3]/div[" + str(i+1) + "]/div[2]/div/div[1]/strong").text
        except:
            rating = "-"

        #Adds scraped values into the .csv file
        writer.writerow({'name' : name, 'year' : fixedYear, 'movie_time' : movieTime, 'genre' : genre, 'rating' : rating})

#Formatting KW so that it can be written in url. Replacing all whitespaces with '+'.
KW = re.sub(r"\s+", '+', KW)

#When bo becomes false we'll understand that we're in the last page of the entry.
bo = True

#This variable holds the page number we are in.
counter = 1

#Adding some options in order to use chrome in a maximized screen.
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(PATH,options=options)

#Opening the imdb keyword page that user typed.
driver.get("https://www.imdb.com/find?s=kw&q=" + KW + "&ref_=nv_sr_sm")

#Exception handling in order to find 'Exact keyword matches' button.
try:
    exactKwButton = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id=\"main\"]/div/div[2]/div/a"))
    )

#If there is no such button then except section will be executed
except:
    driver.quit()
    print("There is no exact match with your input.")
    sys.exit()

exactKwButton.click()

#This exception handling section is written in order to handle loading time of the page.
try:
    kw = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@id=\"main\"]/div/div[2]/table/tbody/tr/td/a")))
finally:
    kw.click()

#Opens the file in order to write the content that we're scraping, into a .csv file
f = open(FILENAME+".csv", "a", newline="")
with f:

    #Creates column headers
    fnames = ['name', 'year', 'movie_time', 'genre', 'rating']

    #Creates a writer object in order to write in a file.
    writer = csv.DictWriter(f, fieldnames=fnames)
    writer.writeheader()

    #This exception handling section is for checking whether there is a button or not in order to traverse in pages
    try:
        tButton = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id=\"main\"]/div/div[2]/div[4]/div/div/a"))).text

        #Checks if button is a next button. Generally it must be a next button but still it's good to check for errors.
        if tButton == "Next »":

            #Inside of the while will be executed until the pages end.
            while bo:

                #Gets the last item number in the page and converts is to int.
                sLastItemNumber = driver.find_element_by_xpath("//*[@id=\"main\"]/div/div[2]/div[1]/div/div[2]/span[2]").text
                lastItemNumber = int(sLastItemNumber)

                #Inside of 'if' will be executed when we're on the last page.
                if lastItemNumber < (counter*50):

                    #This line indicates that we're on the last page and while loop will not be executed again.
                    bo = False

                    #Implemented in order to handle any crash.
                    try:
                        mainAlgorithm(lastItemNumber - 50*(counter-1), writer)

                    except:
                        print(f'There is an unexpected problem.')
                        driver.quit()
                        f.close()
                        sys.exit()

                #Inside of 'else' will be executed if we're not in the last page
                else:

                    #Implemented in order to handle any crash.
                    try:
                        mainAlgorithm(50, writer)

                        #If we're on the first page then next button will be on this xpath
                        if counter == 1:
                            nextBut = driver.find_element_by_xpath("//*[@id=\"main\"]/div/div[2]/div[4]/div/div/a")

                        #If we're not on the first page then next button will be implemented on this xpath
                        else:
                            nextBut = driver.find_element_by_xpath("//*[@id=\"main\"]/div/div[2]/div[4]/div/div/a[2]")
                        nextBut.click()
                        time.sleep(5)

                        #Increments the page number
                        counter = counter + 1

                    except:
                        print(f'There is an unexpected problem.')
                        driver.quit()
                        f.close()
                        sys.exit()
        else:
            print(f'There is an unexpected problem')
            driver.quit()
            f.close()
            sys.exit()

    #If there is only one page this 'except' section will be executed
    except:

        #These two lines finds how many movies are there in the page
        sTitleNum = driver.find_element_by_xpath("//*[@id=\"main\"]/div/div[2]/div[4]/div/div").text
        titleNum = int(re.search(r'\d+', sTitleNum).group(0))

        #Implemented in order to handle any crash.
        try:
            mainAlgorithm(titleNum, writer)

        except:
            print(f'There is an unexpected problem.')
            driver.quit()
            f.close()
            sys.exit()

f.close()
driver.quit()
