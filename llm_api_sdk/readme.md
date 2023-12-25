# 关于使用添加llm api的使用说明

## 文件结构
```
├── examples
│   ├── http_multiple_keys_api_model.py
│   └── http_parse_exampl_api_model.py
├── llm_api.py
├── readme.md
├── src
│   └── base_model.py
└── test_llm_api.py
```
http_multiple_keys_api_model.py 一个关于当需要多个api情景的样例

http_parse_exampl_api_model.py 一个关于书写解析resp的样例


## 如何使用

运行一下命令安装相应环境
```
conda create add_llm_api python=3.8
pip intall -r requirements.txt
```

按照*llm_api.py*中的要求完整填写方法即可。可以自行添加所需要的函数，但是请不要使用*requests.post*这样的同步请求方法，而是使用给出的*async_post()*。

填写完成后使用*test_llm_api.py*进行测试即可。

```
python -m test_llm_api
```

