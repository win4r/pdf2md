# PDF 转 Markdown 转换器

一个使用 Gemini 2.5 Flash API 进行 OCR 的命令行工具，可将 PDF 文档转换为 Markdown 格式。

## 功能特点

- 将 PDF 文档转换为图像
- 使用 Gemini 2.5 Flash OCR API 从图像中提取文本
- 将提取的文本转换为结构化的 Markdown
- 简单的命令行界面
- 基于 Web 的用户界面

## 系统要求

- Python 3.8+
- Gemini API 密钥
- Poppler（用于 pdf2image）

## 安装步骤

1. 克隆此仓库
2. 安装依赖项：
   ```
   pip install -r requirements.txt
   ```
3. 安装 Poppler：
   - macOS: `brew install poppler`
   - Ubuntu/Debian: `apt-get install poppler-utils`
   - Windows: 从 [poppler releases](https://github.com/oschwartz10612/poppler-windows/releases/) 下载

4. 在项目根目录创建 `.env` 文件并添加您的 Gemini API 密钥：
   ```
   GEMINI_API_KEY=你的API密钥
   ```

## 使用方法

```
python -m pdf2md.cli --input 输入文件.pdf --output 输出文件.md
```

### 选项：
- `--input`：输入 PDF 文件的路径（必需）
- `--output`：输出 Markdown 文件的路径（可选，默认为输入文件名加 .md 扩展名）
- `--dpi`：图像转换的 DPI（可选，默认：300）
- `--format`：转换的图像格式（可选，默认：png）

## Web 应用使用方法

本项目还包含一个基于 Web 的 PDF 转 Markdown 用户界面。

1.  **确保所有依赖都已安装：**
    ```bash
    pip install -r requirements.txt
    ```
    (如果您尚未安装 Poppler 或设置 Gemini API 密钥，请参照上述主要安装说明进行操作。)

2.  **运行 Flask 应用：**
    ```bash
    python app.py
    ```
    应用通常会在您的网络浏览器中的 `http://127.0.0.1:5000/` 地址可用。

3.  **使用 Web UI：**
    - 在浏览器中打开该 URL。
    - 点击“选择文件”按钮选择一个 PDF 文件。
    - 点击“上传并转换”。
    - 转换后的 Markdown 文本将显示在结果页面上。

## 开发路线图

### MVP（当前版本）
- 基本的 PDF 到图像转换
- 使用 Gemini 2.5 Flash API 进行 OCR 处理
- 简单的 Markdown 格式化
- 命令行界面

### 未来增强
- 改进 Markdown 格式化（表格、列表等）
- 批量处理多个 PDF 文件
- 配置选项
- 性能优化
- 图形用户界面
- 支持受密码保护的 PDF
- 更好的错误处理和恢复机制
