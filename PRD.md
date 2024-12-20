以下是对 **StockAI** 项目需求文档的回顾与总结：

**项目需求文档**

**项目背景**

StockAI 项目旨在创建一个基于人工智能技术的股票顾问工具，整合大模型分析、必盈 API 数据接口、OCR 技术、历史数据分析等功能模块，为用户提供从股票识别到技术分析的全链路支持。

**项目目标**

**	**1.**	**提供实时数据与历史分析，辅助用户进行股票决策。

**	**2.**	**利用 OCR 技术解析股票软件截图，自动提取关键信息。

**	**3.**	**集成大语言模型（如 GPT-4），进行智能分析与预测。

**	**4.**	**支持用户自定义 API 与提示词配置，提供灵活扩展能力。

**	**5.**	**打造轻量级、易用的全功能股票顾问工具。

**功能需求**

**1. OCR 模块**

**	**•**	**通过快捷键触发截图功能，自动保存图片。

**	**•**	**使用 OCR 技术识别股票软件截图，提取股票代码和其他关键信息。

**2. 数据获取模块**

**	**•**	**集成必盈 API，支持实时行情和历史数据拉取。

**	**•**	**可通过通用 **fetch_api_data** 函数调用不同 API。

**	**•**	**支持用户自定义 API 参数（如股票代码、时间区间等）。

**3. 大模型分析模块**

**	**•**	**调用大语言模型（如 GPT-4），结合历史数据和实时行情，生成对股票趋势的分析与预测。

**	**•**	**支持用户自定义提示词配置，用于指导大模型生成更准确的结果。

**4. 数据分析模块**

**	**•**	**提供常见技术指标计算（如 KDJ、MACD、BOLL）。

**	**•**	**支持历史趋势分析和多种时间周期对比。

**5. 上传模块**

**	**•**	**实现图像或分析结果自动上传，支持用户在不同平台查看。

**6. 日志与结果管理**

**	**•**	**记录用户操作日志和 API 调用情况。

**	**•**	**保存分析结果，支持按时间或关键词搜索。

**技术需求**

**1. 前端与交互**

**	**•**	**提供截图触发与结果展示的直观界面。

**	**•**	**支持通过命令行或快捷键触发特定功能。

**2. 后端与扩展**

**	**•**	**使用 Python 语言开发，模块化设计便于扩展。

**	**•**	**通过配置文件管理 API 密钥和其他敏感信息。

**	**•**	**使用日志模块记录关键操作和问题排查。

**3. 数据存储**

**	**•**	**支持将分析结果存储为 JSON、CSV 文件，便于后续查询与展示。

**4. 测试与部署**

**	**•**	**编写单元测试和集成测试，保证模块功能正确性。

**	**•**	**使用 Docker 进行环境封装，支持快速部署。

**项目结构**

**核心模块**

**	**1.**	** **截图模块** ：负责用户截图功能及文件管理。

**	**2.**	** **OCR 模块** ：负责截图内容识别与数据提取。

**	**3.**	** **数据获取模块** ：与必盈 API 交互，获取实时与历史数据。

**	**4.**	** **大模型模块** ：与 GPT-4 或其他大语言模型交互，进行数据分析。

**	**5.**	** **数据分析模块** ：提供多种技术指标与趋势分析。

**	**6.**	** **日志模块** ：记录操作和数据分析的全过程。

**用户需求**

**	**1.**	** **目标用户** ：股票投资者、金融分析师、技术爱好者。

**	**2.**	** **核心需求** **：**

**	**•**	**高效的股票信息获取与分析。

**	**•**	**灵活的自定义 API 和参数。

**	**•**	**直观的操作界面和高质量分析结果。

**开发计划**

**	**1.**	** **阶段一** **：**

**	**•**	**实现截图和 OCR 基础功能。

**	**•**	**集成必盈 API，实现实时数据拉取。

**	**•**	**编写初步日志记录功能。

**	**2.**	** **阶段二** **：**

**	**•**	**接入大语言模型，完成基础分析模块。

**	**•**	**实现常见技术指标计算。

**	**•**	**开发自动上传功能。

**	**3.**	** **阶段三** **：**

**	**•**	**优化用户界面与操作体验。

**	**•**	**扩展 API 支持范围，支持更多金融数据源。

**	**•**	**完善测试与部署文档。

**当前进展**

**	**1.**	****完成：**

**	**•**	**截图功能、OCR 模块、必盈 API 数据获取。

**	**•**	**基础日志记录和 README 文档撰写。

**	**2.**	****进行中：**

**	**•**	**数据分析模块优化。

**	**•**	**大语言模型集成与提示词自定义。

**	**3.**	****待实现：**

**	**•**	**图像与结果自动上传。

**	**•**	**用户界面优化。

**预期成果**

**	**1.**	**提供完整的从截图到分析的股票顾问工具。

**	**2.**	**支持用户灵活扩展和定制。

**	**3.**	**提高股票分析的准确性与效率。

希望以上复习内容清晰全面，有助于后续开发和优化！
