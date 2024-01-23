import re
def extract(response, model_name=None):
    if model_name.lower() == "labrewardmodel":
        # 不同模型格式不一定
        return response
    
    try:
        result = re.findall('判断结果.*[A|B]', response)[0][-1]
    except:
        result = re.findall('A|B', response)[0][-1]
    return '1' if result == 'B' else '4'