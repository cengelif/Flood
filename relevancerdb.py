# Healthtags
# 556ba07faaa98a2a661aac29 - 556ba080aaa98a2a661aac31
# 557f66ff23f6e29a04dafcf5 - 557f670023f6e29a04dafcf7

# Flood
# 54a48df38a8d5e2e4016a736 - 54a48e078a8d5e2e4016a796

import relevancer as rlv
import pandas as pd
from sklearn.naive_bayes import MultinomialNB 
from bson.objectid import ObjectId

my_token_pattern=r"[#@]?\w+\b|[\U00010000-\U0010ffff]"

collection = 'healthtags_big'
done_collection = 'healthtags_id_clusters'

rlvdb, rlvcl = rlv.connect_mongodb(configfile='data/mongodb.ini',coll_name=collection) #Db and the collection that contains the tweet set to be annotated.
donedb, donecl = rlv.connect_mongodb(configfile='data/mongodb.ini',coll_name=done_collection) #Db and the collection that contains the tweet set that was annotated.

begin = ObjectId('55950fb4d04475ee9867f3a4')
end = ObjectId('55950fc9d04475ee986841c3')
#tweetlist = rlv.read_json_tweets_database(rlvcl, mongo_query={}, tweet_count=3000, reqlang='en')
#tweetlist = rlv.read_json_tweets_database(rlvcl, mongo_query={'_id': {'$gte': begin, '$lte': end}}, tweet_count=10000, reqlang='en')

#This list is just for test.
annotated_tw_ids = [] #You should get the actual annotated tweet ids from the annotated tweets collection.

for cluster in donecl.find({'classes': {'$ne': None}}):
   annotated_tw_ids += cluster['ctweettuplelist']



tweetlist = rlv.read_json_tweet_fields_database(rlvcl, mongo_query={}, annotated_ids=annotated_tw_ids)
# tweetlist = rlv.read_json_tweets_database(rlvcl, mongo_query={'_id': {'$gte': begin, '$lte': end}}, tweet_count=3000, reqlang='en')
# tweetlist = rlv.read_json_tweets_database(rlvcl, mongo_query={'_id': {'$gte': begin}}, tweet_count=50000, reqlang='in')
# tweetlist = rlv.read_json_tweets_database(rlvcl, mongo_query={}, tweet_count=5000000, reqlang='in')

rlv.logging.info("Number of tweets:" + str(len(tweetlist)))
#print(len(tweetlist))	

tweetsDF = rlv.create_dataframe(tweetlist)
	
tok = rlv.tok_results(tweetsDF, elimrt = True)

start_tweet_size = len(tweetsDF)
rlv.logging.info("\nNumber of the tweets after retweet elimination:"+ str(start_tweet_size))

tw_id_list = rlv.get_ids_from_tw_collection(rlvcl)
print ("Length of the tweet ids and the first then ids",len(tw_id_list),tw_id_list[:10])

tst_https = tweetsDF[tweetsDF.text.str.contains("https")]#["text"]
tst_http = tweetsDF[tweetsDF.text.str.contains("http:")]#["text"]
tstDF = tst_http
tstDF = rlv.normalize_text(tstDF)
print(tstDF["text"].iloc[10])
print("normalization:",tstDF["active_text"].iloc[10])

cluster_list = rlv.create_clusters(tweetsDF, my_token_pattern, nameprefix='2-', selection=False) # those comply to selection criteria
#cluster_list2 = rlv.create_clusters(tweetsDF, selection=False) # get all clusters. You can consider it at the end.
print (len(cluster_list))  
a_cluster = cluster_list[0]

print("cluster_no", a_cluster['cno'] )

print("cluster_str", a_cluster['cstr'] )

print("cluster_tweet_ids", a_cluster['twids'] )

print("cluster_freq", a_cluster['rif'] )

print("cluster_prefix", a_cluster['cnoprefix'] )

print("cluster_tuple_list", a_cluster['ctweettuplelist'] )

collection_name = collection + '_clusters'
rlvdb[collection_name].insert(cluster_list) #Each iteration results with a candidate cluster list. Each iteration will have its own list. Therefore they are not mixed.
print("Clusters were written to the collection:", collection_name)

# After excluding tweets that are annotated, you should do the same iteration as many times as the user would like.
# You can provide a percentage of annotated tweets to inform about how far is the user in annotation.

'''
tweets_as_text_label_df = pd.DataFrame({'label' : ['relif', 'social'] , 'text' : ["RT @OliverMathenge: Meanwhile, Kenya has donated Sh91 million to Malawi flood victims, according to the Ministry of Foreign Affairs." , "Yow ehyowgiddii! Hahaha thanks sa flood! #instalike http://t.co/mLaTESfunR"]})
print("tweets_as_text_label_df:", tweets_as_text_label_df)

# get vectorizer and classifier
vect_and_classifier = rlv.get_vectorizer_and_mnb_classifier(tweets_as_text_label_df, my_token_pattern, pickle_file="vectorizer_and_classifier_dict")
vectorizer, mnb_classifier = vect_and_classifier["vectorizer"], vect_and_classifier["classifier"]

# get label for a new tweet:
ntw = vectorizer.transform(["Why do you guys keep flooding TL with smear campaign for a candidate you dont like.You think you can actually influnece people's decision?"])
predictions = mnb_classifier.predict(ntw)
print("Predictions:", predictions)
'''

rlv.logging.info('\nscript finished')