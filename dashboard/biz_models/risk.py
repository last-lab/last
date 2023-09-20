from tortoise import Model, fields

# 暂定数据结构
# {
#     cid: str
#     first_risk: {
#         id: str,
#         name: str,
#         description: str
#     },
#     second_risk: {
#         id: str,
#         name: str,
#         description: str
#     },
#     third_risk: [
#         {
#             id: str,
#             name: str,
#             description: str
#         }
#     ]
# }


class Risk(Model):
    cid = fields.CharField(max_length=200)
    first_risk = fields.CharField(max_length=200)
    second_risk = fields.CharField(max_length=200)
    third_risk = fields.CharField(max_length=200)


