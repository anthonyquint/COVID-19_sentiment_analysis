#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 29 00:27:32 2021

@author: anthonyquint
"""

import argparse
import json 
import math


def get_top_scores(final_scores,num_words,topic_dic,tweet_topics): 
    
    sorted_scores = topic_dic 
    top_n_scores = {"v":[], "cr":[], "p":[], "hec":[], "n":[], "scs":[],"cth":[],"s":[]}
    
    for topic in tweet_topics:
        
        temp = dict(sorted(final_scores[topic].items(), key=lambda item: item[1]))
 
        sorted_scores[topic] = temp
        
    # print(sorted_scores)

    
    for topic in tweet_topics: 
        top_words = list(sorted_scores[topic])[-int(num_words):]
        top_n_scores[topic] = top_words
        
        
       
        # for top_word in top_words: 
            
        #     top_n_scores[pony][top_word] = sorted_scores[pony][top_word]
            
        
    return top_n_scores 




def get_idf_denom(word,tweet_topics,input_dic): 
    
    sum = 0 
    
    for topic in tweet_topics: 
        if word in input_dic[topic]: 
            sum += 1 
    
    return sum
    

def compute_tfidf(topic_dic,input_dic,tweet_topics): 
    
    for topic in tweet_topics: 
        for word in input_dic[topic]:
            
            tf = input_dic[topic][word]
            
            idf_num = 8
            idf_denom = get_idf_denom(word,tweet_topics,input_dic)
            idf = math.log10(idf_num/idf_denom) 
            
            tfidf = tf*idf
            
            topic_dic[topic][word] = tfidf
            
    
    return topic_dic

def main(): 
     # Take input from user 
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--cinput', help = 'Provide input json file.')
    parser.add_argument('-n','--num', help = 'Provide input data file.')
    args = parser.parse_args()
    
    input_file = args.cinput
    num_words = args.num
    
    # Load input file 
    with open(input_file,'r') as file: 
        input_dic = json.load(file)
        
    
    # Compute TF-IDF for all ponies and all their words
    
    tweet_topics = ["v","cr","p","hec","n","scs","cth","s"]
    topic_dic = {"v":{}, "cr":{}, "p":{}, "hec":{}, "n":{}, "scs":{},"cth":{},"s":{}}  
    final_scores = compute_tfidf(topic_dic,input_dic,tweet_topics)
    
    # Get the num_words highest scores from the ponies 
    top_n_scores = get_top_scores(final_scores,num_words,topic_dic,tweet_topics)
    print(json.dumps(top_n_scores,indent=4))
    
    with open('idfScores_byTopic.json', 'w') as output:
        json.dump(top_n_scores,output,indent=4)
        
    
    return 



if __name__ == '__main__':
    main()
    