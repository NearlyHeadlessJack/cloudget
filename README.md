# cloudget

[![Python](https://img.shields.io/badge/python-%3E%3D3.12-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.x-green)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-yellow)](LICENSE)

从中央气象台（nmc.cn）爬取气象雷达拼图，通过 Flask 提供交互式网页浏览。

支持**全国、华北、东北、华东、华中、华南、西南、西北**八个区域的雷达拼图选择，可查看过去约 24 小时内每 6 分钟一帧的历史图像。

## 功能

- 八个区域雷达拼图，覆盖全国
- 下拉菜单选择地区和时间，确认后展示图像
- 每次区域页面包含约 240 个历史时间点（间隔 6 分钟）
- 浏览器本地存储记忆上次选择的地区
- 图片直接引用 NMC CDN，无需本地下载
- 5 分钟 API 缓存，减少重复请求
- 深色响应式主题，适配桌面和移动端

## 快速开始

### 环境要求

- Python >= 3.12

### 安装

```bash
git clone git@github.com:NearlyHeadlessJack/cloudget.git
cd cloudget
pip install -e .
```

### 启动

```bash
python -m cloudget
# 或者
python cloudget/main.py
```

浏览器访问 `http://127.0.0.1:9999`。

## API

| 路由 | 说明 |
|------|------|
| `GET /` | 主页面 |
| `GET /api/times/<slug>` | 获取指定区域的所有时间点，返回 JSON |
| `GET /api/radar/<slug>/<timestamp>` | 获取指定区域和时间戳的雷达图 URL |

### 示例

```bash
# 获取全国区域的时间列表
curl http://127.0.0.1:9999/api/times/chinaall

# 对应的区域 slug
# chinaall / huabei / dongbei / huadong / huazhong / huanan / xinan / xibei
```

## 项目结构

```
cloudget/
  __main__.py       # python -m cloudget 入口
  main.py           # Flask 应用、爬虫逻辑、API 路由
  templates/
    index.html      # 前端交互页面
pyproject.toml      # 项目配置
```

## 许可

MIT License
