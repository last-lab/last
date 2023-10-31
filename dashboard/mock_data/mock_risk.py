from tortoise import Tortoise

from dashboard.biz_models import Risk


async def create_mock_risk():
    connection = Tortoise.get_connection("default")
    await connection.execute_query(f"DROP TABLE IF EXISTS {Risk.__name__.upper()}")
    await Tortoise.generate_schemas(Risk)

    risk_1 = Risk(risk_level=1, risk_id="1", risk_name="国家安全")
    await risk_1.save()

    risk_2 = Risk(risk_level=2, risk_id="11", risk_name="领导人相关", parent_risk_id="1")
    await risk_2.save()

    risk_3 = Risk(risk_level=2, risk_id="12", risk_name="敏感人物或组织", parent_risk_id="1")
    await risk_3.save()

    risk_4 = Risk(risk_level=2, risk_id="13", risk_name="政治事件", parent_risk_id="1")
    await risk_4.save()

    risk_5 = Risk(risk_level=2, risk_id="14", risk_name="负面言论", parent_risk_id="1")
    await risk_5.save()

    risk_6 = Risk(risk_level=2, risk_id="15", risk_name="舆情", parent_risk_id="1")
    await risk_6.save()

    risk_7 = Risk(risk_level=2, risk_id="16", risk_name="其他", parent_risk_id="1")
    await risk_7.save()

    risk_8 = Risk(risk_level=3, risk_id="111", risk_name="一号领导相关", parent_risk_id="11")
    await risk_8.save()

    risk_9 = Risk(risk_level=3, risk_id="112", risk_name="毛泽东相关", parent_risk_id="11")
    await risk_9.save()

    risk_10 = Risk(risk_level=3, risk_id="113", risk_name="邓小平相关", parent_risk_id="11")
    await risk_10.save()

    risk_11 = Risk(risk_level=3, risk_id="114", risk_name="江泽民相关", parent_risk_id="11")
    await risk_11.save()

    risk_12 = Risk(risk_level=3, risk_id="115", risk_name="常委领导", parent_risk_id="11")
    await risk_12.save()

    risk_13 = Risk(risk_level=3, risk_id="116", risk_name="现任国家领导", parent_risk_id="11")
    await risk_13.save()

    risk_14 = Risk(risk_level=3, risk_id="117", risk_name="历任国家领导", parent_risk_id="11")
    await risk_14.save()

    risk_15 = Risk(risk_level=3, risk_id="118", risk_name="外国领导人", parent_risk_id="11")
    await risk_15.save()

    risk_16 = Risk(risk_level=3, risk_id="119", risk_name="其他领导", parent_risk_id="11")
    await risk_16.save()

    risk_17 = Risk(risk_level=3, risk_id="121", risk_name="落马官员", parent_risk_id="12")
    await risk_17.save()

    risk_18 = Risk(risk_level=3, risk_id="122", risk_name="知名英烈", parent_risk_id="12")
    await risk_18.save()

    risk_19 = Risk(risk_level=3, risk_id="123", risk_name="异见人士", parent_risk_id="12")
    await risk_19.save()

    risk_20 = Risk(risk_level=3, risk_id="124", risk_name="台独人物", parent_risk_id="12")
    await risk_20.save()

    risk_21 = Risk(risk_level=3, risk_id="125", risk_name="港独人物", parent_risk_id="12")
    await risk_21.save()

    risk_22 = Risk(risk_level=3, risk_id="126", risk_name="疆独人物", parent_risk_id="12")
    await risk_22.save()

    risk_23 = Risk(risk_level=3, risk_id="127", risk_name="辱华人物", parent_risk_id="12")
    await risk_23.save()

    risk_24 = Risk(risk_level=3, risk_id="128", risk_name="反动媒体", parent_risk_id="12")
    await risk_24.save()

    risk_25 = Risk(risk_level=3, risk_id="129", risk_name="反动组织", parent_risk_id="12")
    await risk_25.save()

    risk_26 = Risk(risk_level=3, risk_id="1210", risk_name="邪教", parent_risk_id="12")
    await risk_26.save()

    risk_27 = Risk(risk_level=3, risk_id="1211", risk_name="恐怖组织", parent_risk_id="12")
    await risk_27.save()

    risk_28 = Risk(risk_level=3, risk_id="1212", risk_name="其他", parent_risk_id="12")
    await risk_28.save()

    risk_29 = Risk(risk_level=3, risk_id="131", risk_name="六四事件", parent_risk_id="13")
    await risk_29.save()

    risk_30 = Risk(risk_level=3, risk_id="132", risk_name="七五事件", parent_risk_id="13")
    await risk_30.save()

    risk_31 = Risk(risk_level=3, risk_id="133", risk_name="文革", parent_risk_id="13")
    await risk_31.save()

    risk_32 = Risk(risk_level=3, risk_id="134", risk_name="三年困难时期", parent_risk_id="13")
    await risk_32.save()

    risk_33 = Risk(risk_level=3, risk_id="135", risk_name="大跃进", parent_risk_id="13")
    await risk_33.save()

    risk_34 = Risk(risk_level=3, risk_id="136", risk_name="计划生育", parent_risk_id="13")
    await risk_34.save()

    risk_35 = Risk(risk_level=3, risk_id="137", risk_name="占中", parent_risk_id="13")
    await risk_35.save()

    risk_36 = Risk(risk_level=3, risk_id="138", risk_name="反送中", parent_risk_id="13")
    await risk_36.save()

    risk_37 = Risk(risk_level=3, risk_id="139", risk_name="白纸革命", parent_risk_id="13")
    await risk_37.save()

    risk_38 = Risk(risk_level=3, risk_id="1310", risk_name="太阳花运动", parent_risk_id="13")
    await risk_38.save()

    risk_39 = Risk(risk_level=3, risk_id="1311", risk_name="修宪", parent_risk_id="13")
    await risk_39.save()

    risk_40 = Risk(risk_level=3, risk_id="1312", risk_name="台独", parent_risk_id="13")
    await risk_40.save()

    risk_41 = Risk(risk_level=3, risk_id="1313", risk_name="港独", parent_risk_id="13")
    await risk_41.save()

    risk_42 = Risk(risk_level=3, risk_id="1314", risk_name="港独", parent_risk_id="13")
    await risk_42.save()

    risk_43 = Risk(risk_level=3, risk_id="1315", risk_name="疆独", parent_risk_id="13")
    await risk_43.save()

    risk_44 = Risk(risk_level=3, risk_id="1316", risk_name="其他", parent_risk_id="13")
    await risk_44.save()

    risk_45 = Risk(risk_level=3, risk_id="141", risk_name="反动分裂", parent_risk_id="14")
    await risk_45.save()

    risk_46 = Risk(risk_level=3, risk_id="142", risk_name="政治负面", parent_risk_id="14")
    await risk_46.save()

    risk_47 = Risk(risk_level=3, risk_id="143", risk_name="社会负面", parent_risk_id="14")
    await risk_47.save()

    risk_48 = Risk(risk_level=3, risk_id="144", risk_name="种族主义", parent_risk_id="14")
    await risk_48.save()

    risk_49 = Risk(risk_level=3, risk_id="145", risk_name="恐怖主义", parent_risk_id="14")
    await risk_49.save()

    risk_50 = Risk(risk_level=3, risk_id="146", risk_name="法西斯", parent_risk_id="14")
    await risk_50.save()

    risk_51 = Risk(risk_level=3, risk_id="147", risk_name="其他", parent_risk_id="14")
    await risk_51.save()

    risk_52 = Risk(risk_level=3, risk_id="151", risk_name="灾难事故", parent_risk_id="15")
    await risk_52.save()

    risk_53 = Risk(risk_level=3, risk_id="152", risk_name="毒疫苗", parent_risk_id="15")
    await risk_53.save()

    risk_54 = Risk(risk_level=3, risk_id="153", risk_name="毒奶粉", parent_risk_id="15")
    await risk_54.save()

    risk_55 = Risk(risk_level=3, risk_id="154", risk_name="新冠疫情", parent_risk_id="15")
    await risk_55.save()

    risk_56 = Risk(risk_level=3, risk_id="155", risk_name="四通桥事件", parent_risk_id="15")
    await risk_56.save()

    risk_57 = Risk(risk_level=3, risk_id="156", risk_name="其他", parent_risk_id="15")
    await risk_57.save()

    risk_58 = Risk(risk_level=1, risk_id="2", risk_name="数据保护")
    await risk_58.save()

    await Risk(risk_level=1, risk_id="3", risk_name="歧视相关").save()
    await Risk(risk_level=2, risk_id="31", risk_name="民族歧视", parent_risk_id="3").save()
    await Risk(risk_level=2, risk_id="32", risk_name="信仰歧视", parent_risk_id="3").save()
    await Risk(risk_level=2, risk_id="33", risk_name="国别歧视", parent_risk_id="3").save()
    await Risk(risk_level=2, risk_id="34", risk_name="地域歧视", parent_risk_id="3").save()
    await Risk(risk_level=2, risk_id="35", risk_name="性别歧视", parent_risk_id="3").save()
    await Risk(risk_level=2, risk_id="36", risk_name="年龄歧视", parent_risk_id="3").save()
    await Risk(risk_level=2, risk_id="37", risk_name="职业歧视", parent_risk_id="3").save()
    await Risk(risk_level=2, risk_id="38", risk_name="健康歧视", parent_risk_id="3").save()
    await Risk(risk_level=2, risk_id="39", risk_name="其他方面歧视", parent_risk_id="3").save()