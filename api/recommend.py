
from django.http import JsonResponse
from study_group.models import Tag, UserTagLog
from user.models import User
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def create_recommand_csv(request):
   

# 질문 csv로 만들어야하는데 서버를 실행하고 만들어야하는지
# splite3파일을 직접 쿼리문을 작성하면서 csv파일로 만들어야하는지

    users_id = [user.id for user in User.objects.all()] # index 값 유저 고유 아이디
    tags_name = [tag.name for tag in Tag.objects.all()] # 태그 이름들 columns

    users = [user for user in User.objects.all()] # 사용할 유저 객체들
    tags = [tag for tag in Tag.objects.all()] # 사용할 태그 객체들
    user_log_count = [] # 유저가 태그를 방문한 횟수

    print(users)


    for user in users:
        ins_user_count = []
        for tag in tags:
            try:
                tag_log = user.usertaglog_set.get(tag = tag)
                count = tag_log.count
            except UserTagLog.DoesNotExist:

                count = 0

            ins_user_count.append(count)

        user_log_count.append(ins_user_count)

    df = pd.DataFrame(user_log_count, columns=tags_name, index=users_id)

    print(df)
    print(df.loc[6].sort_values(ascending=False))

    user_based_collab = cosine_similarity(df, df)
    user_based_collab = pd.DataFrame(user_based_collab, index=users_id, columns=users_id)
    recommend_tags_table = pd.DataFrame(users_id, columns=['user_id'])
    append_tags = []
    for id in users_id:
        similar = user_based_collab.loc[id].sort_values(ascending=False)[:10].index[1] # 인덱스 (순서 x)기반 인덱싱
        print(type(similar))
        my_tags = df.loc[id].sort_values(ascending=False).index.to_list()[:5]
        recommend_tags = df.loc[similar].sort_values(ascending=False).index.to_list()[:10]
        recommend_tags = list(set(recommend_tags)-set(my_tags))
        append_tags.append(recommend_tags)

    recommend_tags_table["tags"] = append_tags
    recommend_tags_table = recommend_tags_table.set_index("user_id")

    print(recommend_tags_table)
    recommend_tags_table.to_csv("recommand.csv", index=True)

    return JsonResponse('dd', safe=False)


import ast

def get_recommend_tags(request):

    data = pd.read_csv("recommand.csv")
    data = data.set_index("user_id")

    try:
        a = data.loc[request.user.id]
    except:
        return None
        
    a = a["tags"]
    x = ast.literal_eval(a) # str list to list

    return x
