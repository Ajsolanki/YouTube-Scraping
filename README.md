# YouTube-Scraping
Scrap You tube Video details using Selenium
Precily Assesment Descripation:

1). First use Chrome Webdriver to automate the process to open the browser and pass the url to scrap the data. 
2). There is one problem occur that Page automatic not scroll down so to overcome that problem use driver.execute_script to automate the whole process.
3). From scraped data fetch the user video link and if there any user channel then the link of user channel.
4). From the user channel scrap the all video they have in there Videos section.
5). After getting all the links for the videos. then open the every video page and get the details like Video Id, Video Tiltle and Video Description.
6). After getting all the details create a Dataframe.
7). For every category Do the same and get Dataframe for every category.
8). Then Concate all the Dataframe into One Dataframe.
9). After having all the data in dataframe then preprocess the data and clean the Data
10). After this we having preprocessed and encoded data (using LableEncoder).

Model Part 
Using the Gaussian Naive Bayes Model to train and Predicate the model
1). First split the Data into Training and Testing Data.
2). Train the data using training set.
3). Then Predict the model result on testing set.
4). Check the accuracy of the Model with sklearn.metrics
5). Print the Classification Report and confusion Metrix

Note: I have not that much resource(Internet) so I have scrap a small dataset. But code is efficiently working for the large data-set also.(Checked on one category)

I use Naive Bayes algorithms because fast and easy to predict class of test data. It also easily use for multiclass data.
It is easily handls the large size datasets. I also use other algorithms but I use Naive bayes.
	
