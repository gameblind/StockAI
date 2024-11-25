# **StockAI 工作日志**

此文档用于记录 StockAI 项目每次开发和维护的详细工作内容，便于追踪项目进展和改动历史。

---

## **日志目录**
- [2024-11-24](#2024-11-24)

---

### **2024-11-24**
#### **主要任务**
1. 修复 `fetch_api_data` 函数中对 `api_key` 校验逻辑的冲突问题：
   - 修改逻辑以支持在 JSON 配置文件中动态获取 `api_key`。
   - 优化对参数缺失的校验，确保参数传递与默认值获取不冲突。

2. 完善 `test_main.py` 测试：
   - 添加对多个 API 的详细测试用例。
   - 测试内容覆盖以下 API：
     - `margin_trading_target_stocks`
     - `margin_trading_historical_trends`
     - `historical_intraday_trading`
     - `historical_intraday_macd`
   - 确保测试在逻辑更新后全部通过。

3. 重构 JSON 数据结构：
   - 修改 `API Code` 字段为英文，方便调用和维护。
   - 添加新的唯一主键字段 `API Key Combined`，通过 `Category Code` 和 `API Code` 组合生成。

4. 更新 `README.md`：
   - 增加详细的模块说明和安装使用指南。
   - 完整描述了集成的必盈 API 数据接口信息。

5. 修复 Git 同步冲突：
   - 遇到远端代码和本地代码冲突问题。
   - 使用本地代码为主的策略覆盖远端，并成功完成同步。

#### **输出文件**
- 更新后的 `README.md`。
- 新的工作日志文件 `work_log.md`。
- 测试通过的完整代码。

#### **问题记录**
1. **`fetch_api_data` 参数校验冲突问题**：
   - 解决：明确参数获取来源（传参优先，默认配置次之）。
2. **Git 同