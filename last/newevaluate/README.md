# new_evaluate
## 文件结构
* messages 产生message
  * p1.py
  * p2.py
* function_call 函数调用
  * oai.py openai调用
* utlis 提取结果

## Using Method
`type_prompt` 是小类标签，比如`fair`里的`民族歧视`
`key` 是 openai key

### 2,3,4,5,7用法
```python
from messages.p2 import generate_message
from function_call.oai import call
from utlis import extract
messages, _ = generate_message(question, answer, type_prompt)
response = call(key, messages)
predict = extract(response)
```

### 1用法

加载敏感词
```python
import pandas as pd
path = "/mnt/petrelfs/share_data/shao_group/zyt/sensitive/12.5"
sent_all = pd.read_csv(path + "/12.5_sensitive_new.csv")
sent_all = list(sent_all['0'])
sent_high = pd.read_csv(path + "/12.5_sensitive_high_new.csv")
sent_high = list(sent_high['0'])
```

预测
```python
from messages.p1 import generate_message
from function_call.oai import call
from utlis import extract

messages, need_model = generate_message(question, answer, type_prompt, (sent_high, sent_all))
if need_model:
    response = call(key, messages)
else:
    response = messages
predict = extract(response)

```