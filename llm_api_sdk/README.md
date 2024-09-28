# 关于使用llm api SDK的使用说明

## 文件结构
```
├── examples
│   ├── base_model.py
│   ├── http_fundamentalt_api_model.py
│   ├── http_multiple_keys_api_model.py
│   └── http_parse_exampl_api_model.py
├── readme.md
├── requirements.txt
├── src
│   ├── base_model.py
│   ├── llm_api.py
│   └── utils.py
├── test_data
│   └── dataset.xlsx
└── test_llm_api.py
```
http_multiple_keys_api_model.py 一个关于当需要多个api情景的样例

http_parse_exampl_api_model.py 一个关于书写解析resp的样例


## 如何使用
- step 1

运行一下命令安装相应环境
```
(optional) conda create add_llm_api python=3.8
(optional) conda activate add_llm_api
pip intall -r requirements.txt
```
- step 2

按照*src/llm_api.py*中的要求完整填写方法即可。可以自行添加所需要的函数，但是请不要使用*requests.post()*这样的同步请求方法，而是使用给出的*async_post()*。为了方便使用，我们在examples目录中提供了一些样例作为参考，希望能有所帮助。

- step 3

修改*test_llm_api.py*中的**step**变量和**api_key**变量，前者意味着并发数(qps)，请选择合适的数字填入，后者表示所需要的密钥信息.

- step 4 (optional)

*./test_data*目录中放置了一些测试用数据，可以自行添加一些敏感数据用于测试。

- step 5

完成后使用*test_llm_api.py*进行测试即可。

在运行下面的命令之前，请删除*test_llm_api.py*中的 **@unittest.skip("Need develop")**
```
cd path/llm_api_sdk
python -m test_llm_api
```
