import ast
from django.http import JsonResponse
from study_group.models import Tag, UserTagLog
from user.models import User
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def create_recommand_csv(request):

    users_id = [user.id for user in User.objects.all()]
    tags_name = [tag.tag_name for tag in Tag.objects.all()]

    users = [user for user in User.objects.all()]
    tags = [tag for tag in Tag.objects.all()]
    user_log_count = []

    for user in users:
        ins_user_count = []
        for tag in tags:
            try:
                tag_log = user.usertaglog_set.get(tag=tag)
                count = tag_log.count
            except UserTagLog.DoesNotExist:

                count = 0

            ins_user_count.append(count)

        user_log_count.append(ins_user_count)

    df = pd.DataFrame(user_log_count, columns=tags_name, index=users_id)

    user_based_collab = cosine_similarity(df, df)
    user_based_collab = pd.DataFrame(
        user_based_collab, index=users_id, columns=users_id)
    recommend_tags_table = pd.DataFrame(users_id, columns=['user_id'])
    append_tags = []
    
    for id in users_id:

        similar = user_based_collab.loc[id].sort_values(
            ascending=False)[0:10].index[1]  # 인덱스 (순서 x)기반 인덱싱

        my_tags = df.loc[id].sort_values(ascending=False).index.to_list()[0:5]
        recommend_tags = df.loc[similar].sort_values(
            ascending=False).index.to_list()[0:10]
        recommend_tags = list(set(recommend_tags)-set(my_tags))
        append_tags.append(recommend_tags)

    recommend_tags_table["tags"] = append_tags
    recommend_tags_table = recommend_tags_table.set_index("user_id")


    recommend_tags_table.to_csv("recommand.csv", index=True)

    return JsonResponse('dd', safe=False)


def get_recommend_tags(request):

    data = pd.read_csv("recommand.csv")
    data = data.set_index("user_id")

    try:
        a = data.loc[request.user.id]
    except:
        return None

    a = a["tags"]
    x = ast.literal_eval(a)

    return x
