import numpy as np
from lightfm.datasets import fetch_movielens
from lightfm import LightFM

#fetch data and format it
data = fetch_movielens(min_rating=4.0)


#print training and testing data

print(repr(data['train']))
print(repr(data['test']))

#create model
model = LightFM(loss='warp') #weighted appr-rank pairwise

#train mode
model.fit(data['train'], epochs=30, num_threads=2)

def sample_recommendation(model, data, user_ids):
	#num of users and movies in training
	n_users, n_items = data['train'].shape

	#generate recommendations
	for user_id in user_ids:

		#mvies they already likes
		known_positives = data['item_labels'][data['train'].tocsr()[user_id].indices]

		#movies out model predicts they will like
		scores = model.predict(user_id, np.arange(n_items))

		#rank them in order of most liked to least
		top_items = data['item_labels'][np.argsort(-scores)]

		#print results
		print("User %s" % user_id)
		print("		Known positives:")

		for x in known_positives[:3]:
			print(" 			%s" % x)

		print(" 		Recommended:")

		for x in top_items[:3]:
			print("				%s" % x)

sample_recommendation(model, data, [1, 2, 3])