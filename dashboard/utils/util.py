from dashboard.biz_models import DataSet, Risk


class Tool:
    @classmethod
    async def get_dataset_match_risk(cls, risk: Risk):
        match_dataset = []
        datasets = await DataSet.all()
        for dataset in datasets:
            if risk.risk_id in dataset.focused_risks:
                match_dataset.append(dataset)
        return {
            "dataset_count": len(match_dataset),
            "dataset_word_cnt": sum([obj.word_cnt for obj in match_dataset]),
            "dataset_name_list": [obj.name for obj in match_dataset],
        }
