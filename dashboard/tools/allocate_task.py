import random


def distribute_labeling_task(len_dataset: int, assign_user_dict):
    # 传入的数据为[{"assign_user", 32}]这种格式
    # 采用某种算法，给不同的用户分配不同的item进行标注
    # 返回的结果为 {0: ['user1', 'user2'], ...}
    # 暂时返回每个用户都要标注所有的item
    assign_user_item_dict = allocate(len_dataset, assign_user_dict)
    item_assign_user_dict = {index: [] for index in range(len_dataset)}
    # 对这个item_assign_user_dict 进行反序遍历
    for index in range(len_dataset):
        for assign_user in assign_user_item_dict:
            if index in assign_user_item_dict[assign_user]:
                item_assign_user_dict[index].append(assign_user)

    # 返回{"user1": 10, "user2": 20, ...}
    assign_user_item_length = {
        assign_user: len(assign_user_item_dict[assign_user])
        for assign_user in assign_user_item_dict
    }

    # 配置一个标注进度字典 {"user1": 0, "user2": 0}等
    assign_user_labeling_progress = {assign_user: 0 for assign_user in assign_user_item_dict}

    return (
        item_assign_user_dict,
        assign_user_item_dict,
        assign_user_item_length,
        assign_user_labeling_progress,
    )


def distribute_audit_task(len_dataset: int, audit_user_list):
    audit_user_item_dict = allocate(len_dataset, audit_user_list)
    item_audit_user_dict = {index: [] for index in range(len_dataset)}
    # 对这个item_assign_user_dict 进行反序遍历
    for index in range(len_dataset):
        for audit_user in audit_user_item_dict:
            if index in audit_user_item_dict[audit_user]:
                item_audit_user_dict[index].append(audit_user)

    # 返回{"user1": 10, "user2": 20, ...}
    audit_user_item_length = {
        audit_user: len(audit_user_item_dict[audit_user]) for audit_user in audit_user_item_dict
    }

    # 配置一个标注进度字典 {"user1": 0, "user2": 0}等
    audit_user_labeling_progress = {audit_user: 0 for audit_user in audit_user_item_dict}

    return (
        item_audit_user_dict,
        audit_user_item_dict,
        audit_user_item_length,
        audit_user_labeling_progress,
    )


def allocate(total, dist_dict):
    # total表示的是一个整数
    # dist_dict分配字典
    results = {user: [] for user in dist_dict}
    nums = list(range(0, total))
    for user, ratio in dist_dict.items():
        num = int(float(ratio) * total / 100)
        for _ in range(num):
            rand_index = random.randrange(len(nums))
            results[user].append(nums.pop(rand_index))

    if len(nums) != 0:
        results[user] = results[user] + nums
    return {user: sorted(results[user]) for user in results}
