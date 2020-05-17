'''
MyTweetFetcher uses Tweepy's search.API method to obtain tweets given a keyword and language.
Developed by erickgch.

Usage:
my_tweet_fetcher.py <keyword> <language> <result type [optional]>
'''

#Import/install non-default packages
try:
    import tweepy
    import art
except:
    import sys
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'tweepy', 'art'])
    import tweepy
    import art

#Import all other packages
import sys, json, os, csv, datetime, random
from art import tprint
from tweepy import TweepError

dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
try:
    with open(os.path.join(dirname, "creds.json")) as cred_data:
        info = json.load(cred_data)
        consumer_key = info['twitter_cred']['CONSUMER_KEY']
        consumer_secret = info['twitter_cred']['CONSUMER_SECRET']
        access_key = info['twitter_cred']['ACCESS_KEY']
        access_secret = info['twitter_cred']['ACCESS_SECRET']
except:
    print(
        "\nJson file not found\nMake sure the json file contains the right keys and that it is in the same directory as this file")
    input("\nPress any key to exit... ")

# Time variables
current_time = datetime.datetime.now()
until_day = current_time.day - 5

# Print cool art
tprint("MyTweetFetcher")


def fetch_tweets():
    #Calling tweepy and API
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)
    except TweepError:
        print("It appears you have no internet connection. Check and try again.")
        exit()
    #Argument handling
    if len(sys.argv) > 4:
        print("\nToo many arguments\nExpected arguments: keyword, language, result type (optional).\n\nTry again.\n")
        exit()
    elif len(sys.argv) == 4:
        try:
            keyword_ = str(sys.argv[1])
            language_ = str(sys.argv[2])
            result_type_ = str(sys.argv[3])
            if result_type_ not in ['popular', 'mixed']:
                result_type_ = 'recent'
        except:
            print('Wrong input. Please include keyword and language arguments and try again.')
            exit()
    else:
        try:
            keyword_ = str(sys.argv[1])
            language_ = str(sys.argv[2])
            result_type_ = 'recent'
        except:
            print('Wrong input. Please include keyword and language arguments and try again.')
            exit()

    # Informing the user about his query
    if keyword_.startswith('#'):
        print("\n\nRetrieving " + (
            result_type_) + " tweets containing the hashtag '" + keyword_ + "' in '" + language_ + "' language.\n\n")
    elif keyword_.startswith('@'):
        print("\n\nRetrieving" + (
            result_type_) + " tweets containing the user '" + keyword_ + "' in '" + language_ + "' language.\n\n")
    else:
        print("\n\nRetrieving " + (
            result_type_) + " tweets containing the word '" + keyword_ + "' in '" + language_ + "' language.\n\n")

    location = input(
        '\nWould you like to look for tweets from a specific location?\nInsert coordinates and radius in the following format: latitude,longitude,radius (see README file for examples).\nOtherwise, hit ENTER to skip or "x" to exit.\n')
    print("\nWorking...\n")


    tweets = []
    # Actual fetching
    try:
        # No geolocation
        if location.lower() == 'x':
            print("Exiting.")
            exit()
        elif len(str(location)) == 0:
            for tweet in tweepy.Cursor(api.search, q=keyword_ + '-filter:retweets', tweet_mode='extended',
                                       lang=language_, result_type=result_type_,
                                       until=str(current_time.strftime("%Y-%m-" + str(until_day)))).items():
                tweets.append(tweet.full_text)
        # With geolocation
        else:
            for tweet in tweepy.Cursor(api.search, q=keyword_ + '-filter:retweets', tweet_mode='extended',
                                       lang=language_, result_type=result_type_, geocode=str(location).replace(" ", ""),
                                       show_user=True).items():
                tweets.append(tweet.full_text)
    except TweepError:
        print("\nWarning: Allowed number of requests exceeded.\n")
        pass
    except KeyboardInterrupt:
        print("\nProcess interrupted.\n")
    except:
        print("\nSomething went wrong. Try again.\n")
        exit()

    # Output message
    if len(tweets) == 0:
        print('\nNo tweets found :/\n')
        exit()
    elif len(tweets) >= 1:
        print("\nTweets retrieved!\n")

    return tweets

# Display-reduce-save
def output(a):
    print('\n' + str(len(a)) + ' tweets retrieved in total.\n')
    # Display
    while True:
        output_1 = input("\nVisualize tweets? [y/n]\n")
        if str(output_1).lower() not in ['y', 'n', 'yes' ,'no']:
            print("\nWrong input.")
            continue
        else:
            output_1 = str(output_1).lower()
            if output_1 in ["y", "yes"]:
                print(a)
                print('\n')
                print(str(len(a)) + " total tweets.\n")
                break
            else:
                print("Pass.\n")
                break

    # Saving
    while True:
        output_2 = input("Save as TXT or CSV? [no/csv/txt] ")
        if str(output_2).lower() in ['csv', 'txt']:
            # Subsampling
            while True:
                subsample = input("Would you like to obtain a subsample of this list? Insert number of elements desired. Otherwise, hit ENTER.\n")
                if len(subsample) == 0:
                    final_list = a
                    break
                elif not subsample.isnumeric():
                    print("\nWrong input (Number expected).")
                else:
                    final_list = random.sample(a, k=int(subsample))
                    break
            # ... as txt
            if output_2.lower() == 'txt':
                with open("my_tweets_out_" + str(sys.argv[1]) + str(current_time.strftime("%Y-%m-%d-%H-%M-%S")) + ".txt",
                          'w',encoding='utf-8') as f:
                    for i in final_list:
                        f.write("%s\n" % i+"-_-")
                print("\nmy_tweets_out_"+str(sys.argv[1])+str(current_time.strftime("%Y-%m-%d-%H-%M-%S"))+".txt\n")
                print('That is all from my part. Exiting.')
                break
            # ... as csv
            elif output_2.lower() == 'csv':
                with open("my_tweets_out_" + str(sys.argv[1]) + str(
                        current_time.strftime("%Y-%m-%d-%H-%M-%S")) + ".csv", "w", newline='',encoding='utf-8') as f:
                    writer = csv.writer(f)
                    for l in final_list:
                        writer.writerow([l + ","])
                    # writer.writerows(final_list)
                print("\nFile saved as my_tweets_out_"+str(sys.argv[1])+str(current_time.strftime("%Y-%m-%d-%H-%M-%S"))+".csv\n")
                print('That is all from my part. Exiting.')
                break
        elif output_2.lower() == 'no':
            print("\nExiting.")
            break
        else:
            print("\nWrong input")
            continue
    exit()
    sys.exit()


output(fetch_tweets())
