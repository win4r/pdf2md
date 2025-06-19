# PDF 转 Markdown 转换器

一个使用 Gemini 2.5 Flash API 进行 OCR 的命令行工具，可将 PDF 文档转换为 Markdown 格式。

## 功能特点

- 将 PDF 文档转换为图像
- 使用 Gemini 2.5 Flash OCR API 从图像中提取文本
- 将提取的文本转换为结构化的 Markdown
- 简单的命令行界面
- 现代化、交互式的 Web 用户界面，具有以下特点：
    - 文件上传支持点击选择和拖拽操作。
    - 上传和处理过程中的加载状态指示。
    - 转换结果的 Markdown 实时预览。
    - 一键复制 Markdown 内容到剪贴板。
    - 将转换结果下载为 `.md` 文件。
    - 清晰的用户反馈和错误提示。

## 系统要求

- Python 3.8+
- Gemini API 密钥
- Poppler（用于 pdf2image）
- 稳定的网络连接（Web UI 需要从 CDN 加载样式和脚本）

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
    - 通过点击美化的上传区域或直接将 PDF 文件拖拽到该区域来选择您的文件。
    - 文件选择后，您会看到文件名显示。
    - 点击“上传并转换”按钮。在文件上传和处理期间，按钮将显示加载动画和 "Processing..." 文本。
    - 成功转换后，您将被引导至结果页面。
    - 转换后的 Markdown 内容将以格式化预览的形式显示。
    - 您可以使用“Copy”按钮将原始 Markdown 文本复制到剪贴板，或使用“Download .md File”按钮将其保存到本地。
    - 如果在上传或处理过程中发生任何错误（例如，无效的文件类型，PDF 处理问题），将在上传页面顶部显示一条清晰的错误消息，您可以关闭该消息。
    - 点击“Convert Another File”可以返回上传页面。

## 日志记录
在非调试模式下运行时 (例如 `python app.py` 且未设置 `FLASK_DEBUG=1`)，应用程序的错误将被记录到项目根目录下的 `app_errors.log` 文件中。这有助于诊断生产环境中可能出现的问题。

## 开发路线图

### MVP（当前版本）
- 基本的 PDF 到图像转换
- 使用 Gemini 2.5 Flash API 进行 OCR 处理
- 简单的 Markdown 格式化 (通过 `MarkdownGenerator`)
- 命令行界面
- 现代化、交互式的 Web 用户界面 (已实现 v1)
- 基本的错误处理和用户反馈 (已改进)

### 未来增强
- **高级 Markdown 渲染**: 在 Web UI 中集成更完善的 Markdown 渲染，例如支持表格、任务列表，以及代码块的语法高亮 (可以考虑 `@tailwindcss/typography` 插件配合本地 Tailwind 构建，或引入如 Prism.js/Highlight.js 的库)。
- **批量处理**: 允许用户一次上传和转换多个 PDF 文件。
- **配置选项**: 在 UI 中提供选项让用户调整 OCR 参数或 Markdown 输出格式。
- **性能优化**: 针对非常大的 PDF 文件进行处理流程优化。
- **支持受密码保护的 PDF**: (需要探索 `PyPDF2` 或其他库处理加密 PDF 的能力，并安全地处理密码输入)。
- **本地 Tailwind CSS 构建**: 解决本地 Node.js/npm 环境问题，以便能够使用完整的 Tailwind CSS 功能 (如自定义配置、`@apply` 优化、PurgeCSS) 并移除对 CDN 的依赖。
- **更细致的 OCR 结果处理**: 分析 OCR 结果的结构，尝试生成更语义化的 Markdown (例如，识别标题层级、列表、粗体/斜体等)。
