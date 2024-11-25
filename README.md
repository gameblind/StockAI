# **StockAI**

StockAI 是一个基于 Python 的股票顾问 AI 项目，整合了大模型识别、必盈 API 接入、OCR 提取、历史数据分析等功能，为用户提供股票分析与决策支持。

---

## **目录**

- [项目简介](#项目简介)
- [功能模块](#功能模块)
- [项目结构](#项目结构)
- [安装与使用](#安装与使用)
- [项目工具](#项目工具)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## **项目简介**

StockAI 项目旨在构建一个轻量级的股票顾问系统，核心功能包括：
- 股票截图 OCR 解析。
- 基于大语言模型（LLM）的股票数据分析。
- 历史数据获取与技术指标分析。
- 股票图像自动上传与识别。

---

## **功能模块**

### 1. **截图与 OCR**
- **功能**：支持通过快捷键触发截图，并使用 OCR 提取图像中的股票信息。
- **模块**：
  - `src/screenshot/`: 截图功能实现。
  - `src/ocr/`: OCR 文本提取与股票信息解析。

### 2. **大模型识别**
- **功能**：调用 GPT-4 或其他 LLM 模型解析图片并预测股票走势。
- **模块**：
  - `src/llm/`: 大模型 API 接入与结果解析。

### 3. **历史数据获取**
- **功能**：集成必盈 API，获取股票的历史数据与实时行情。
- **模块**：
  - `src/data_fetcher/`: 提供历史与实时数据获取功能。

### 4. **数据分析**
- **功能**：对股票数据进行技术指标计算与趋势分析。
- **模块**：
  - `src/analyzer/`: 数据分析与技术指标计算。

### 5. **项目工具**
- **功能**：辅助项目管理，包括项目结构解析、环境设置等。
- **模块**：
  - `project_tools/`: 提供轻量级工具脚本与辅助文件。

---

## **项目结构**

```plaintext
StockAI/
├── src/                        # 核心代码模块
│   ├── screenshot/             # 截图功能
│   ├── ocr/                    # OCR 解析模块
│   ├── llm/                    # 大语言模型 API 接入
│   ├── data_fetcher/           # 股票数据获取模块
│   ├── analyzer/               # 数据分析与技术指标计算
│   ├── upload_images/          # 图像上传功能
│   ├── main.py                 # 项目主入口
├── config/                     # 配置文件目录
├── logs/                       # 日志文件目录
├── output/                     # 输出文件目录
├── resources/                  # 静态资源（如模板文件）
├── project_tools/              # 项目管理工具
│   ├── analyze_project.py      # 项目结构分析脚本
│   ├── create_project_with_screenshot.sh # 环境初始化脚本
│   ├── list_structure.py       # 项目函数与类结构解析
│   ├── function_structure.txt  # 项目函数结构输出
│   ├── project_structure.txt   # 项目整体结构输出
│   ├── setup.sh                # 一键项目配置脚本
├── tests/                      # 测试代码
├── README.md                   # 项目说明文档
├── requirements.txt            # Python 依赖包
└── .gitignore                  # Git 忽略文件
---

## **数据API**

[必盈api](https://ad.biyingapi.com/ssjy.html) 地址:https://ad.biyingapi.com/ssjy.html
事实数据接口：
```实时交易数据接口
API接口：http://api.biyingapi.com/hsrl/ssjy/股票代码(如000001)/您的licence

备用接口：http://api1.biyingapi.com/hsrl/ssjy/股票代码(如000001)/您的licence

包年版专用接口：http://n.biyingapi.com/hsrl/ssjy/股票代码(如000001)/您的licence

白金版专用接口：http://b.biyingapi.com/hsrl/ssjy/股票代码(如000001)/您的licence

接口说明：根据《股票列表》得到的股票代码获取实时交易数据（您可以理解为日线的最新数据）。

数据更新：交易时间段每1分钟

请求频率：1分钟20次 | 包年版1分钟3000次 | 白金版1分钟6000次

返回格式：标准Json格式 [{},...{}]

字段名称	数据类型	字段说明
fm	number	五分钟涨跌幅（%）
h	number	最高价（元）
hs	number	换手（%）
lb	number	量比（%）
l	number	最低价（元）
lt	number	流通市值（元）
o	number	开盘价（元）
pe	number	市盈率（动态，总市值除以预估全年净利润，例如当前公布一季度净利润1000万，则预估全年净利润4000万）
pc	number	涨跌幅（%）
p	number	当前价格（元）
sz	number	总市值（元）
cje	number	成交额（元）
ud	number	涨跌额（元）
v	number	成交量（手）
yc	number	昨日收盘价（元）
zf	number	振幅（%）
zs	number	涨速（%）
sjl	number	市净率
zdf60	number	60日涨跌幅（%）
zdfnc	number	年初至今涨跌幅（%）
t	string	更新时间yyyy-MM-dd HH:mm:ss
买卖五档盘口
API接口：http://api.biyingapi.com/hsrl/mmwp/股票代码(如000001)/您的licence

备用接口：http://api1.biyingapi.com/hsrl/mmwp/股票代码(如000001)/您的licence

包年版专用接口：http://n.biyingapi.com/hsrl/mmwp/股票代码(如000001)/您的licence

白金版专用接口：http://b.biyingapi.com/hsrl/mmwp/股票代码(如000001)/您的licence

接口说明：根据《股票列表》得到的股票代码获取实时买卖五档盘口数据。

数据更新：交易时间段每2分钟

请求频率：1分钟20次 | 包年版1分钟3000次 | 白金版1分钟6000次

返回格式：标准Json格式 [{},...{}]

字段名称	数据类型	字段说明
t	string	更新时间yyyy-MM-dd HH:mm:ss
vc	number	委差（股）
vb	number	委比（%）
pb1	number	买1价（元）
vb1	number	买1量（股）
pb2	number	买2价（元）
vb2	number	买2量（股）
pb3	number	买3价（元）
vb3	number	买3量（股）
pb4	number	买4价（元）
vb4	number	买4量（股）
pb5	number	买5价（元）
vb5	number	买5量（股）
ps1	number	卖1价（元）
vs1	number	卖1量（股）
ps2	number	卖2价（元）
vs2	number	卖2量（股）
ps3	number	卖3价（元）
vs3	number	卖3量（股）
ps4	number	卖4价（元）
vs4	number	卖4量（股）
ps5	number	卖5价（元）
vs5	number	卖5量（股）
当天逐笔交易
API接口：http://api.biyingapi.com/hsrl/zbjy/股票代码(如000001)/您的licence

备用接口：http://api1.biyingapi.com/hsrl/zbjy/股票代码(如000001)/您的licence

包年版专用接口：http://n.biyingapi.com/hsrl/zbjy/股票代码(如000001)/您的licence

白金版专用接口：http://b.biyingapi.com/hsrl/zbjy/股票代码(如000001)/您的licence

接口说明：根据《股票列表》得到的股票代码获取当天逐笔交易数据，按时间倒序。

数据更新：每天20:00开始更新，当日23:59前完成

请求频率：1分钟20次 | 包年版1分钟3000次 | 白金版1分钟6000次

返回格式：标准Json格式 [{},...{}]

字段名称	数据类型	字段说明
d	string	数据归属日期（yyyy-MM-dd）
t	string	时间（HH:mm:dd）
v	number	成交量（股）
p	number	成交价
ts	number	交易方向（0：中性盘，1：买入，2：卖出）
当天分时成交
API接口：http://api.biyingapi.com/hsrl/fscj/股票代码(如000001)/您的licence

备用接口：http://api1.biyingapi.com/hsrl/fscj/股票代码(如000001)/您的licence

包年版专用接口：http://n.biyingapi.com/hsrl/fscj/股票代码(如000001)/您的licence

白金版专用接口：http://b.biyingapi.com/hsrl/fscj/股票代码(如000001)/您的licence

接口说明：根据《股票列表》得到的股票代码获取当天分时成交数据，按时间倒序。

数据更新：每天20:00开始更新，当日23:59前完成

请求频率：1分钟20次 | 包年版1分钟3000次 | 白金版1分钟6000次

返回格式：标准Json格式 [{},...{}]

字段名称	数据类型	字段说明
d	string	数据归属日期（yyyy-MM-dd）
t	string	时间（HH:mm:dd）
v	number	成交量（股）
p	number	成交价
当天分价成交占比
API接口：http://api.biyingapi.com/hsrl/fjcj/股票代码(如000001)/您的licence

备用接口：http://api1.biyingapi.com/hsrl/fjcj/股票代码(如000001)/您的licence

包年版专用接口：http://n.biyingapi.com/hsrl/fjcj/股票代码(如000001)/您的licence

白金版专用接口：http://b.biyingapi.com/hsrl/fjcj/股票代码(如000001)/您的licence

接口说明：根据《股票列表》得到的股票代码获取当天每个价格成交的数量占总成交数量的百分比。

数据更新：每天20:00开始更新，当日23:59前完成

请求频率：1分钟20次 | 包年版1分钟3000次 | 白金版1分钟6000次

返回格式：标准Json格式 [{},...{}]

字段名称	数据类型	字段说明
d	string	数据归属日期（yyyy-MM-dd）
v	number	成交量（股）
p	number	成交价
b	number	占比（%）
当天逐笔大单交易
API接口：http://api.biyingapi.com/hsrl/zbdd/股票代码(如000001)/您的licence

备用接口：http://api1.biyingapi.com/hsrl/zbdd/股票代码(如000001)/您的licence

包年版专用接口：http://n.biyingapi.com/hsrl/zbdd/股票代码(如000001)/您的licence

白金版专用接口：http://b.biyingapi.com/hsrl/zbdd/股票代码(如000001)/您的licence

接口说明：根据《股票列表》得到的股票代码获取当天大单成交数据（暂时认为大于等于400手一笔属于大单），按时间倒序。

数据更新：每天20:00开始更新，当日23:59前完成

请求频率：1分钟20次 | 包年版1分钟3000次 | 白金版1分钟6000次

返回格式：标准Json格式 [{},...{}]

字段名称	数据类型	字段说明
d	string	数据归属日期（yyyy-MM-dd）
t	string	时间（HH:mm:dd）
v	number	成交量（股）
p	number	成交价
ts	number	交易方向（0：中性盘，1：买入，2：卖出）
Copyright © 2018-2024 必盈网络科技服务有限公司
客服电话：184-3512-8452    客服微信ID：biyingapiclient
网站备案号：晋ICP备2023021176号
风险提示：本站所有免费及收费信息和数据仅供参考，不构成投资建议，本站不承担由此导致的任何法律责任。```
---

## **安装与使用**

1. 克隆项目到本地：
   ```bash
   git clone https://github.com/your_username/StockAI.git
   cd StockAI
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```