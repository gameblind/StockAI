#!/bin/bash

# 项目根目录
PROJECT_NAME="StockAI"
echo "Creating project: $PROJECT_NAME"

# 创建主目录和子目录
mkdir -p $PROJECT_NAME/{config,src/{ocr,screenshot,data_fetcher,analyzer,llm},tests}

# 创建文件
touch $PROJECT_NAME/config/api_config.json
touch $PROJECT_NAME/config/settings.py
touch $PROJECT_NAME/src/ocr/{__init__.py,ocr_processor.py}
touch $PROJECT_NAME/src/screenshot/{__init__.py,screen_capture.py}
touch $PROJECT_NAME/src/data_fetcher/{__init__.py,fetch_data.py}
touch $PROJECT_NAME/src/analyzer/{__init__.py,analyze.py}
touch $PROJECT_NAME/src/llm/{__init__.py,llm_integration.py}
touch $PROJECT_NAME/src/main.py
touch $PROJECT_NAME/tests/{test_main.py,test_screenshot.py,test_llm.py}
touch $PROJECT_NAME/.gitignore
touch $PROJECT_NAME/README.md
touch $PROJECT_NAME/requirements.txt
touch $PROJECT_NAME/setup.sh

# 初始化 git
cd $PROJECT_NAME
git init
echo "Project structure with screenshot module created successfully!"