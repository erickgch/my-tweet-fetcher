# MyTweetFetcher
This project attempts to offer non-technical users an out-of-the-box application to fetch tweets using the official Twitter API. It has been designed specifically for those looking to create a corpus for further processing and analysis (e.g. NLP, corpus linguistics, journalism).

Given a keyword (or keyphrase) and a language, this application conducts a search and saves the resulting list of tweets as either a .txt or .csv file. 

## Step-by-step usage
1. Download and place the folder in a safe and easy-to-find directory.
2. Fill the blank spaces in the json file with your own credentials. The program will not work properly if the json file is missing information or is not located in the same folder as the .py file.
3. Run the program. `python my_tweet_fetcher.py text lang restype` <br />
    * The first argument is the word or phrase to be used in the search query.
    If the keyword is composed of multiple words, it must be written in quotation marks (e.g. singleword --> "multiple words"). 
    * The second argument refers to the language of the tweets we want to fetch (following the ISO 639-1 nomenclature).
    * The third (optional) argument refers to the type of result to be obtained. The search will be focused on either "popular", "recent" or "mixed" tweets.
 
 ## Additional notes
 * Please refer to https://developer.twitter.com/en to learn how to obtain dev credentials, as they are required to use this application. 
 * Only keyword-based searches can be performed.
