#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 28 23:28:53 2021

@author: anthonyquint
"""

import argparse 
import pandas as pd 
import os 
import os.path as osp
from os import path
import json
import sys 


def get_totaloccurance(total_wordfreq_dic,word,tweet_topics): 
    
    sum = 0 
    
    for topic in tweet_topics: 
        if word in total_wordfreq_dic[topic]: 
            sum = sum + total_wordfreq_dic[topic][word]
    
    
    
    return sum



def get_stopwords(): 
    '''Loading stopwords, saving them in a list'''
    
    with open("stopwords.txt",'r') as file: 
        words_raw = file.readlines()
    
    # Removing the \n artificats in the words 
    words_clean = []
    for word in words_raw: 
        word = word.replace('\n', "")
        words_clean.append(word.lower())
    
    # Removing the first 5 "words" because it's just commented code he wrote there
    words_clean = words_clean[6:]
    
    
    return words_clean 


def clean_speech1(speech_act,stop_words): 
    # Replace punctuation in speach act with spaces 
    # punctuation includes ( ) [ ] , - . ? ! : ; # &
    punctuation = ['(',')','[',']',',', '-','.','?','!',':',';','#','&']
                   
    for symbol in punctuation: 
        speech_act = speech_act.replace(symbol, " ")
    
    # Splitting string into list of the words 
    speech_act = speech_act.split(' ')
    
    # Taking lowercase of all elements and dropping empty strings. 
    # And dropping words that aren't exclusively alphabetical
    # And dropping words that are in the stop words
    
    words = []
    for word in speech_act: 
        if word == '': 
            continue 
        if word.isalpha() == False: 
            continue 
        if word.lower() in stop_words: 
            continue 
        if word == 'https': 
            continue 
        else: 
            words.append(word.lower())
    
    # print(words)
            
    return words


def get_wordfreq(topic,df,stop_words): 
    
    df["topic"] = df["topic"].str.lower()
    df_trimmed = df.drop(df[df.topic != topic].index)
    # print(len(df_trimmed))
    
    wordfreq_dic = {}
    for speech_act in df_trimmed.tweet_text: 
        speech_act_words = clean_speech1(speech_act,stop_words)
        
        for word in speech_act_words: 
            if word not in wordfreq_dic: 
                wordfreq_dic[word] = 1
            else: 
                wordfreq_dic[word] = wordfreq_dic[word] + 1
    
    return wordfreq_dic

def main(): 
    
    # Take input from user 
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser()
        parser.add_argument('-o','--output', help = 'Provide desired json file.')
        parser.add_argument('-d','--data', help = 'Provide input data file.')
        args = parser.parse_args()
    
        output_file = args.output
        input_data = args.data
    
    # Load stop words and store them as a list
    stop_words = get_stopwords()
    
    
    # Load input data
    df = pd.read_csv(input_data,encoding= 'unicode_escape')
    # Initialize topics of interest (initially called pony_names)
    tweet_topics = ["v","cr","p","hec","n","scs","cth","s"]
    
    # Filling total_wordfreq_dic with keys of the ponys and values of their 
    # respective word frequency dictionaries 
    total_wordfreq_dic = {}
    for topic in tweet_topics: 
        wordfreq_dic = get_wordfreq(topic,df,stop_words)
        total_wordfreq_dic[topic] = wordfreq_dic
        
    # Determing the words that don't appear at least 5 times 
    # across all speach acts 
    rare_words = []
    for topic in tweet_topics: 
        for word in total_wordfreq_dic[topic]: 
            
            total_occurance = get_totaloccurance(total_wordfreq_dic,word, tweet_topics)
            
            if (total_occurance < 5) and (word not in rare_words):  
                rare_words.append(word)
                
    # creating a cleaned dictionary that doesn't contain any of the rare words 
    final_dic = {"v":{}, "cr":{}, "p":{}, "hec":{}, "n":{}, "scs":{},'cth':{},"s":{}}  
    for topic in tweet_topics: 
        for word in total_wordfreq_dic[topic]: 
            if word not in rare_words: 
                final_dic[topic][word] =  total_wordfreq_dic[topic][word]
            
    
    # Creating new directory if desired directory to save JSON DNE. 
    dirname = os.path.dirname(output_file)
    if path.exists(dirname) == False and dirname != '': 
        os.makedirs(dirname)
    
    # Saving JSON file 
    with open(output_file, 'w') as output:
        json.dump(final_dic, output,indent = 2)
         
    
    # print(final_dic)
    return 


if __name__ == '__main__':
    main()