from Algorithm import *
import itertools

res_category = getCategory()
prices = getPriceRange()

user_category = input('Enter the food category separated by commas: ')
user_price = input('Enter the price range you are looking for ($ = inexpensive, $$ = Moderately expensive, $$$ = Expensive, $$$$ = Very Expensive): ')

print('\nComputing similarity...')

category_similarity = computeCategorySimilarity(user_category, res_category)
price_similarity = computePriceRangeSimilarity(user_price, prices)

similarity_list = []
similarity_dict = {}
final_similarity = {}

for i in range(15752):
    similarity = category_similarity[i]*price_similarity[i]
    similarity_list.append(similarity)
    restaurant_name = df.loc[i, 'name']
    similarity_dict.update({restaurant_name:similarity})

sorted_sim = sorted(similarity_dict, key=similarity_dict.get, reverse=True)
for j in sorted_sim:
    final_similarity.update({j : similarity_dict[j]})

recommendations = dict(itertools.islice(final_similarity.items(), 10))
address = getAddress()

print('\nOur Top Recommendations:\n')
for restaurant in recommendations.keys():
    print(f'{restaurant}, {address[restaurant]}')
print('\n...Done.')


