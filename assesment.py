from selenium import webdriver
import time
import pandas as pd 
import all_df as get

def get_dataframe(str):
    driver = webdriver.Chrome(executable_path= r'C:\chromedriver_win32\chromedriver.exe')
    
    str_list = str.split(" ")
    url = "+".join(str_list)

    base = "https://www.youtube.com/results?search_query="
    html = base+url
    

    driver.get(html)
    SCROLL_PAUSE_TIME = 1.0


    while True:
        # Get scroll height
        ### This is the difference. Moving this *inside* the loop
        ### means that it checks if scrollTo is still scrolling 
        last_height = driver.execute_script("return window.scrollY")

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, window.scrollY+2000)")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return window.scrollY")
        
        if new_height == last_height:
            # try again (can be removed)
            driver.execute_script("window.scrollTo(0, window.scrollY+2000)")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return window.scrollY")
            print(new_height, last_height)
            # check if the page height has remained the same
            if new_height == last_height:
                # if so, you are done
                break
            # if not, move on to the next loop
            else:
                last_height = new_height
                continue

    user_data = driver.find_elements_by_xpath('//a[@id="video-title"]')
    channel_data = driver.find_elements_by_xpath('//*[@id="contents"]/ytd-channel-renderer/a')
    
    #Get the Videos link from the data
    user_link = [i.get_attribute('href') for i in user_data]
    #Get the channel link from the data
    channel_link = [i.get_attribute('href') for i in channel_data]
    
    #To Get the all Videos link from the channel
    channel_video_link = []
    for i in channel_link:
        html = i + '/videos'
        driver.get(html)
        user_data = driver.find_elements_by_xpath('//a[@id="video-title"]')
        user_link = [i.get_attribute('href') for i in user_data]
        channel_video_link = user_link + channel_video_link    

    user_df = get.get_video_details(user_link,str_list[0],driver)
    channel_df = get.get_video_details(channel_video_link,str_list[0],driver)
    frame = [user_df, channel_df]
    df_ = pd.concat(frame, axis=0, join='outer', join_axes=None, ignore_index=True,
                           keys=None, levels=None, names=None, verify_integrity=False, copy=True)    
    return df_ 


travel_df = get_dataframe('travel blog')
S_T_df = get_dataframe('science and technology blog')
food_df = get_dataframe('food blog')
manufacture_df = get_dataframe('manufacturing blog')
A_M_df = get_dataframe('art and music blog')


frames = [travel_df, S_T_df, food_df, manufacture_df, A_M_df]
df_ = pd.concat(frames, axis=0, join='outer', join_axes=None, ignore_index=True,
                           keys=None, levels=None, names=None, verify_integrity=False, copy=True)

#Before Start Cleaning Data we store all column separately for easily perform actions
df_link = pd.DataFrame(columns = ["link"])        
df_title = pd.DataFrame(columns = ["title"])        
df_description = pd.DataFrame(columns = ["description"])        
df_category = pd.DataFrame(columns = ["category"])        
df_link['link'] = df_['link'] 
df_title['title']= df_['title'] 
df_description['description'] = df_['description'] 
df_category['category'] = df_['category']


#clean corpus
from clean_corpus import clean_data_list

#make corpus for title and description
title_corpus = clean_data_list(df_link['link'])
des_corpus = clean_data_list(df_description['description'])

#convert these lists into Dataframes
title_df = pd.DataFrame({'title':title_corpus})
description_df = pd.DataFrame({'description':des_corpus})

'''label encode the categories
LabelEncoder()” function encodes labels with a value between 0 and n_classes – 1 
where n is the number of distinct labels'''

from sklearn.preprocessing import LabelEncoder
category_df = df_category.apply(LabelEncoder().fit_transform)

#Store cleaned and encoded data in new dataframe
df_new = pd.concat([df_link, title_df, description_df, category_df], axis=1, join_axes = [df_link.index])

#Create a bag of words to classify vidoes accordingly
from sklearn.feature_extraction.text import CountVectorizer   
cv = CountVectorizer(max_features = 1500) 
X = cv.fit_transform(title_corpus, des_corpus).toarray() 
y = df_new.iloc[:, 3].values

#Split Data into Training and Testing Data
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

#Import Gaussian Naive Bayes model
from sklearn.naive_bayes import GaussianNB

#Create a Gaussian Classifier
gnb = GaussianNB()

#Train the model using the training sets
gnb.fit(X_train, y_train)

#Predict the response for test dataset
y_pred = gnb.predict(X_test)

#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics

# Model Accuracy, how often is the classifier correct?
print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

#Print Classification report 
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))

#Print Confusion matrix
from sklearn.metrics import confusion_matrix
print(confusion_matrix(y_test, y_pred))
