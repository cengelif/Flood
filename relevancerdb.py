# 556ba07faaa98a2a661aac29 - 556ba080aaa98a2a661aac31
# 557f66ff23f6e29a04dafcf5 - 557f670023f6e29a04dafcf7

import relevancer as rlv
from bson.objectid import ObjectId

rlvdb, rlvcl = rlv.connect_mongodb()

# begin = ObjectId('556ba080aaa98a2a661aac31')
begin = ObjectId('55266b24d202defa22d7d719')
# end = ObjectId('557f66ff23f6e29a04dafcf5')
end = ObjectId('5584043ba023cf5c336ba0cd')
tweetlist = rlv.read_json_tweets_database(rlvcl, mongo_query={'_id': {'$gte': begin, '$lte': end}}, tweet_count=3000, reqlang='en')
rlv.logging.info("number of tweets"+str(len(tweetlist)))
	
tweetsDF = rlv.create_dataframe(tweetlist)
	
tok = rlv.tok_results(tweetsDF)

start_tweet_size = len(tweetsDF)
rlv.logging.info("\nNumber of the tweets after retweet elimination:"+ str(start_tweet_size))

cluster_list = rlv.create_clusters(tweetsDF) # those comply to slection criteria
cluster_list2 = rlv.create_clusters(tweetsDF, selection=False) # get all clusters. You can consider it at the end.

print (len(cluster_list))  


a_cluster = cluster_list[0]

print("cluster_no", a_cluster['cno'] )

print("cluster_str", a_cluster['cstr'] )

print("cluster_tweet_ids", a_cluster['twids'] )

collection_name = 'clusters'
rlvdb[collection_name].insert(cluster_list)

print("Clusters were written to the collection:", collection_name)


# After excluding tweets that are annotated, you should do the same iteration as many times as the user would like.
# You can provide a percentage of annotated tweets to inform about how far is the user in annotation.
