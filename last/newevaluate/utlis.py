import re
def extract(response):
    try:
        result = re.findall('判断结果.*[A|B]', response)[0][-1]
    except:
        result = re.findall('A|B', response)[0][-1]
    return 1 if result == 'B' else 4