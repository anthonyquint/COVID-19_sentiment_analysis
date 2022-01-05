import pandas as pd
import sys
import json
import os

def check_args():
    if len(sys.argv) != 5:
        print('Expected : python count_topics.py -i <1000_tweets.csv> -o <output.json>')
        exit()

def load_csv(file_loc):
    try:
        tweet_data = pd.read_csv(file_loc, encoding= 'unicode_escape')
        return tweet_data
    except Exception as e:
        print("File Not found, check the address of .csv file")
        print("Hint: try entering ..\ for relative path, e.g ..\data\clean_dialog.csv")
        print("Error :", e)
        exit()

def count_word(file_content):
    tweet_dict = {}    
    tweet_dict['vaccination'] = { 'count' : 0, 'negative' : 0, 'positive' : 0, 'neutral' : 0}
    tweet_dict['covid_restrictions'] = {'count' : 0, 'negative' : 0, 'positive' : 0, 'neutral' : 0}
    tweet_dict['political'] = {'count' : 0, 'negative' : 0, 'positive' : 0, 'neutral' : 0}
    tweet_dict['health_effect_of_covid'] = {'count' : 0, 'negative' : 0, 'positive' : 0, 'neutral' : 0}
    tweet_dict['news'] = {'count' : 0, 'negative' : 0, 'positive' : 0, 'neutral' : 0}
    tweet_dict['spread_of_covid_in_society'] = {'count' : 0, 'negative' : 0, 'positive' : 0, 'neutral' : 0}
    tweet_dict['covid_test_healthcare'] = {'count' : 0, 'negative' : 0, 'positive' : 0, 'neutral' : 0}
    tweet_dict['spam'] = {'count' : 0, 'negative' : 0, 'positive' : 0, 'neutral' : 0}
    tweet_dict['total_sentiment'] = {'negative' : 0, 'positive' : 0, 'neutral' : 0}
    
    total_positve = 0
    total_negative = 0
    total_neutral = 0
    for i in range(len(file_content['topic'])):
        topic_content = str(file_content['topic'][i]).strip()
        sentiment_content = str(file_content['sentiment'][i]).strip()

        if (topic_content == "V"):         
            tweet_dict['vaccination']['count'] += 1
            if(sentiment_content == "P"):
                tweet_dict['vaccination']['positive'] += 1
                total_positve += 1
            elif (sentiment_content == "N"):
                tweet_dict['vaccination']['negative'] += 1
                total_negative +=1
            else:
                tweet_dict['vaccination']['neutral'] += 1
                total_neutral += 1

        elif (topic_content == "CR"):         
            tweet_dict['covid_restrictions']['count'] += 1
            if(sentiment_content == "P"):
                tweet_dict['covid_restrictions']['positive'] += 1
                total_positve += 1
            elif (sentiment_content == "N"):
                tweet_dict['covid_restrictions']['negative'] += 1
                total_negative +=1
            else:
                tweet_dict['covid_restrictions']['neutral'] += 1
                total_neutral += 1

        elif (topic_content == "P"):         
            tweet_dict['political']['count'] += 1
            if(sentiment_content == "P"):
                tweet_dict['political']['positive'] += 1
                total_positve += 1
            elif (sentiment_content == "N"):
                tweet_dict['political']['negative'] += 1
                total_negative +=1
            else:
                tweet_dict['political']['neutral'] += 1
                total_neutral += 1

        elif (topic_content == "HEC"):         
            tweet_dict['health_effect_of_covid']['count'] += 1
            if(sentiment_content == "P"):
                tweet_dict['health_effect_of_covid']['positive'] += 1
                total_positve += 1
            elif (sentiment_content == "N"):
                tweet_dict['health_effect_of_covid']['negative'] += 1
                total_negative +=1
            else:
                tweet_dict['health_effect_of_covid']['neutral'] += 1
                total_neutral += 1

        elif (topic_content == "N"):         
            tweet_dict['news']['count'] += 1
            if(sentiment_content == "P"):
                tweet_dict['news']['positive'] += 1
                total_positve += 1
            elif (sentiment_content == "N"):
                tweet_dict['news']['negative'] += 1
                total_negative +=1
            else:
                tweet_dict['news']['neutral'] += 1
                total_neutral += 1

        elif (topic_content == "SCS"):         
            tweet_dict['spread_of_covid_in_society']['count'] += 1
            if(sentiment_content == "P"):
                tweet_dict['spread_of_covid_in_society']['positive'] += 1
                total_positve += 1
            elif (sentiment_content == "N"):
                tweet_dict['spread_of_covid_in_society']['negative'] += 1
                total_negative +=1
            else:
                tweet_dict['spread_of_covid_in_society']['neutral'] += 1
                total_neutral += 1

        elif (topic_content == "CTH"):         
            tweet_dict['covid_test_healthcare']['count'] += 1
            if(sentiment_content == "P"):
                tweet_dict['covid_test_healthcare']['positive'] += 1
                total_positve += 1
            elif (sentiment_content == "N"):
                tweet_dict['covid_test_healthcare']['negative'] += 1
                total_negative +=1
            else:
                tweet_dict['covid_test_healthcare']['neutral'] += 1
                total_neutral += 1

        elif (topic_content == "S"):         
            tweet_dict['spam']['count'] += 1
            if(sentiment_content == "P"):
                tweet_dict['spam']['positive'] += 1
                total_positve += 1
            elif (sentiment_content == "N"):
                tweet_dict['spam']['negative'] += 1
                total_negative +=1
            else:
                tweet_dict['spam']['neutral'] += 1
                total_neutral += 1

        elif topic_content != "nan":
            print("ALERT!!!!!")
            print("TYPO AT :" + str(file_content['topic'][i]) + "Line no " + str(i))

        
    
    tweet_dict['total_sentiment']['neutral'] = total_neutral
    tweet_dict['total_sentiment']['positive'] = total_positve
    tweet_dict['total_sentiment']['negative'] = total_negative 

    print("Lines with annotation : ", total_positve + total_neutral + total_negative)

    return tweet_dict

def write_json(file_loc, file_content):

    json_object = json.dumps(file_content, indent = 4)  
    
    if os.path.dirname(file_loc):        
        os.makedirs(os.path.dirname(file_loc), exist_ok=True) 
  
    # Writing to sample.json
    with open(file_loc, "w") as outfile:
        outfile.write(json_object)

    print("File created successfully")

if __name__ == "__main__":
    check_args()       
    tweet_data = load_csv(sys.argv[2])
    tweet_dict = count_word(tweet_data)
    write_json(sys.argv[4],tweet_dict)