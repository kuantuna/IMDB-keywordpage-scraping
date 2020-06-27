# IMDB-keywordpage-scraping

## General Steps
-	This script can generally be used to scrape the properties of movie results in IMDB's keyword page and write them to a .csv file. 

![0](https://user-images.githubusercontent.com/66808459/85923446-c8653280-b893-11ea-8a54-cb55b36c927f.png)
-	When script is run (for example, KW = "robots" and FILENAME = "mov"), the page you see in the picture below opens first.

![1](https://user-images.githubusercontent.com/66808459/85923452-d4e98b00-b893-11ea-9178-fd944a84e412.png)
-	Then, it is checked whether there is an 'Exact keyword matches' button on this page. If not, the program is terminated by typing 'There is no exact match with your input'. If there is, the program goes to the page shown below by clicking the 'Exact keyword matches' button.

![3](https://user-images.githubusercontent.com/66808459/85923457-db780280-b893-11ea-9118-2a47d39f881a.png)
-	‘robots’ link is clicked.

![4](https://user-images.githubusercontent.com/66808459/85923458-de72f300-b893-11ea-8361-3b9fc8dcc91c.png)
-	When it comes to this page where the movies are sorted, marked movie features such as the name of the movie,  year of the movie was made, the movie duration, the genre of the movie and the rating of the movie are scrapped and saved in to a .csv file.

![5](https://user-images.githubusercontent.com/66808459/85923461-e2067a00-b893-11ea-9da3-c1f2f13ed0c5.png)
-	In the picture above, clicking the 'next' button I marked, scrapes all of the pages by going to them one by one.

![6](https://user-images.githubusercontent.com/66808459/85923685-e7fd5a80-b895-11ea-98fe-923bbd8a8d64.png)
- Finally all properties are saved in the 'mov.csv' file and if we open this file with excel we can get a view like above.
