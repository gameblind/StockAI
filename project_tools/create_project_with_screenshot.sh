#!/bin/bash

# Define the base directory
BASE_DIR="/Users/wangchong/DEV/StockAI"

# Ensure the base directory exists
if [ ! -d "$BASE_DIR" ]; then
  echo "Base directory does not exist: $BASE_DIR"
  exit 1
fi

# Function to create directory if it doesn't exist
create_dir_if_not_exists() {
  if [ ! -d "$1" ]; then
    mkdir -p "$1"
    echo "Created directory: $1"
  fi
}

# Function to create file if it doesn't exist
create_file_if_not_exists() {
  if [ ! -f "$1" ]; then
    touch "$1"
    echo "Created file: $1"
  fi
}

# Create necessary directories
create_dir_if_not_exists "$BASE_DIR/src/data_fetcher"
create_dir_if_not_exists "$BASE_DIR/src/analyzer"
create_dir_if_not_exists "$BASE_DIR/src/llm"
create_dir_if_not_exists "$BASE_DIR/src/screenshot"
create_dir_if_not_exists "$BASE_DIR/src/upload_images"
create_dir_if_not_exists "$BASE_DIR/screenshots"
create_dir_if_not_exists "$BASE_DIR/config"
create_dir_if_not_exists "$BASE_DIR/tests"

# Create Python files in src/data_fetcher
create_file_if_not_exists "$BASE_DIR/src/data_fetcher/__init__.py"
create_file_if_not_exists "$BASE_DIR/src/data_fetcher/fetch_data.py"

# Create Python files in src/analyzer
create_file_if_not_exists "$BASE_DIR/src/analyzer/__init__.py"
create_file_if_not_exists "$BASE_DIR/src/analyzer/analyze.py"

# Create Python files in src/llm
create_file_if_not_exists "$BASE_DIR/src/llm/__init__.py"
create_file_if_not_exists "$BASE_DIR/src/llm/api_request.py"

# Create Python files in src/screenshot
create_file_if_not_exists "$BASE_DIR/src/screenshot/__init__.py"
create_file_if_not_exists "$BASE_DIR/src/screenshot/screen_capture.py"

# Create Python files in src/upload_images
create_file_if_not_exists "$BASE_DIR/src/upload_images/__init__.py"
create_file_if_not_exists "$BASE_DIR/src/upload_images/upload_images.py"

# Create configuration files
create_file_if_not_exists "$BASE_DIR/config/setting.json"
create_file_if_not_exists "$BASE_DIR/config/__init__.py"
create_file_if_not_exists "$BASE_DIR/config/settings.py"

# Create test files
create_file_if_not_exists "$BASE_DIR/tests/test_screenshot.py"
create_file_if_not_exists "$BASE_DIR/tests/test_llm.py"
create_file_if_not_exists "$BASE_DIR/tests/test_ocr.py"
create_file_if_not_exists "$BASE_DIR/tests/__init__.py"

# Create general project files
create_file_if_not_exists "$BASE_DIR/README.md"
create_file_if_not_exists "$BASE_DIR/requirements.txt"
create_file_if_not_exists "$BASE_DIR/.gitignore"
create_file_if_not_exists "$BASE_DIR/app.log"
create_file_if_not_exists "$BASE_DIR/stock_info.json"

# Feedback
echo "Missing files and directories have been created successfully."