# Weather Center API 自动化测试

天气数据中心接口自动化测试平台，覆盖天气预报、城市搜索、空气质量三大业务模块。

## 项目简介

本项目针对天气数据查询服务进行接口自动化测试，采用分层架构设计，集成数据驱动、多环境配置、统一日志与CI/CD流水线，可作为团队接口测试框架的基础模板。

## 技术栈

| 类别 | 技术 |
|------|------|
| 测试框架 | pytest |
| HTTP客户端 | requests |
| 数据驱动 | PyYAML |
| 环境管理 | python-dotenv |
| CI/CD | GitHub Actions |
| 测试报告 | pytest-html |

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 运行测试

```bash
# 全部用例
pytest testcases/ -v

# 生成HTML报告
pytest testcases/ -v --html=reports/report.html --self-contained-html

# 只跑空气质量模块
pytest testcases/test_air.py -v

# 按关键字筛选
pytest -v -k "beijing"
```

## 项目架构

```
weather-center-test/
├── .github/workflows/       # CI/CD 配置
├── config/                  # 配置层：环境地址、超时参数
├── api/                     # 接口层：按业务域封装
│   ├── base_api.py          #   请求基类：session、超时、日志
│   ├── forecast_api.py      #   天气预报接口
│   ├── geocoding_api.py     #   城市搜索接口
│   └── air_api.py           #   空气质量接口
├── testcases/               # 测试用例层
│   ├── conftest.py          #   pytest fixtures
│   ├── test_forecast.py     #   预报接口测试
│   ├── test_geocoding.py    #   城市搜索测试
│   └── test_air.py          #   空气质量测试
├── utils/                   # 工具层
│   ├── logger.py            #   日志封装
│   ├── assert_util.py       #   自定义断言
│   └── data_loader.py       #   YAML数据加载
├── testdata/                # 测试数据层
│   └── cities.yaml          #   城市参数化数据
└── reports/                 # 测试报告输出
```

## 测试覆盖

| 业务模块 | 接口端点 | 用例数 |
|---------|---------|--------|
| 实时天气 | `/v1/forecast` (current) | 8 |
| 每日预报 | `/v1/forecast` (daily) | 6 |
| 逐小时预报 | `/v1/forecast` (hourly) | 2 |
| 城市搜索 | `/v1/search` | 11 |
| 空气质量 | `/v1/air-quality` | 6 |
| 边界值/异常 | 全模块 | 9 |
| **合计** | | **42** |

## 测试类型

- **正向测试**：正常参数返回200，校验响应结构与字段类型
- **参数化测试**：多城市、多单位，数据从YAML外部加载
- **边界值测试**：经纬度极值、预报天数边界、结果数量边界
- **异常测试**：缺失参数、非法坐标、错误变量名
