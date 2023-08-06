# 韩灵稚打包测试
Hanlingzhi's Package PyPi Demo
###工程结构说明
<pre>
.
├── LICENSE.txt    	// 证书文件
├── README.md		// MD文件
├── hanlingzhi
│   ├── __init__.py
│   └── math_h.py
├── setup.py			// 打包配置
└── string_h
    ├── __init__.py
    └── reverse.py
</pre>
###测试服务器打包流程
* 升级setuptools和wheel包
<pre>python3 -m pip install --user --upgrade setuptools wheel</pre>
* 打包到本地文件
<pre>python3 setup.py sdist bdist_wheel




This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.