import pandas as pd
import math

dataset = pd.read_csv('restaurants.csv')
df = pd.DataFrame(dataset)


def cmp(a, b):
    return [c for c in a if c.isalpha()] == [c for c in b if c.isalpha()]


def getCategoryList():
    categoryList = []
    for i in range(15752):
        category = str(df.loc[i, 'category'])
        category_list = category.split(',')

        for category_type in category_list:
            if category_type not in categoryList:
                categoryList.append(category_type)

    return categoryList

categories = getCategoryList()

def getAddress():
    address_dict = {}

    for i in range(15752):
        restaurant_name = df.loc[i, 'name']

        res_address = df.loc[i, 'full_address']

        address_dict.update({restaurant_name: res_address})

    return address_dict


def getCategory():
    category = {}

    for i in range(15752):
        restaurant_name = df.loc[i, 'name']

        category_name = df.loc[i, 'category']

        category.update({restaurant_name: category_name})

    return category


def getPriceRange():
    price_range = {}

    for i in range(15752):
        restaurant_name = df.loc[i, 'name']
        price = df.loc[i, 'price_range']
        price_range.update({restaurant_name: price})

    return price_range


def getCategoryVector():
    category = {}
    category_vec = {}

    for i in range(15752):
        category_lol = []
        restaurant_name = df.loc[i, 'name']
        category_name = str(df.loc[i, 'category'])
        category.update({restaurant_name: category_name})

        category_list = category_name.split(',')
        categoryVector = [0] * 466

        for j in category_list:
            category_lol.append(j)

        for categ in category_lol:
            for k in categories:

                if cmp(categ, k):
                    categoryVector[categories.index(k)] = 1
                    break

        category_vec.update({restaurant_name: categoryVector})

    return category_vec

category_vector = getCategoryVector()

def computePriceRangeSimilarity(user_price, prices):
    priceSim_map = {}
    priceSim = {}
    priceSim_list = []

    for i in range(15752):
        restaurant_name = df.loc[i, 'name']
        cur_price = prices[restaurant_name]
        diff = abs(len(str(cur_price)) - len(str(user_price)))
        sim = math.exp(-diff / 10.0)
        priceSim_list.append(sim)
        priceSim_map.update({restaurant_name: sim})

    sorted_sim = sorted(priceSim_map, key=priceSim_map.get, reverse=True)
    for k in sorted_sim:
        priceSim.update({k: priceSim_map[k]})

    return priceSim_list


def computeCategorySimilarity(user_category, category):
    category_score = {}
    similarity_scores = {}
    similarity_list = []

    category_list = user_category.split(',')
    restaurant_category = []

    for i in category_list:
        restaurant_category.append(i)

    user_category_vec = [0] * 466
    for categ in restaurant_category:
        for j in categories:

            if (cmp(categ, j)):
                user_category_vec[categories.index(j)] = 1
                break

    for i in range(15752):
        restaurant_name = df.loc[i, 'name']
        restaurant_categ_vec = category_vector[restaurant_name]
        sumxx, sumxy, sumyy = 0, 0, 0

        for j in range(len(restaurant_categ_vec) - 1):
            x = user_category_vec[j]
            y = restaurant_categ_vec[j]
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y

        similarity_score = sumxy / ((sumxx * sumyy) ** 0.5)
        similarity_list.append(similarity_score)
        category_score.update({restaurant_name: similarity_score})

    sorted_sim = sorted(category_score, key=category_score.get, reverse=True)
    for k in sorted_sim:
        similarity_scores.update({k: category_score[k]})

    return similarity_list

