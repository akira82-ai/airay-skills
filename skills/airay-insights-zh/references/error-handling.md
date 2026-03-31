# 错误处理指南

本文档提供 insights-zh 技能的详细错误处理策略。

## 错误类型和处理策略

### 1. 文件不存在错误

**场景**：`~/.claude/usage-data/report.html` 不存在

**检测**：
```bash
[ ! -f ~/.claude/usage-data/report.html ]
```

**处理策略**：
1. 检查用户是否运行过 `/insights` 命令
2. 提示用户先运行 `/insights` 生成报告
3. 提供备用路径选项（如果用户指定了 `--path` 参数）

**用户提示**：
```
❌ 未找到 insights 报告

请先运行 /insights 命令生成报告：
  /insights

或指定自定义路径：
  /insights-zh --path /path/to/your/report.html

检查报告目录：
  ls -la ~/.claude/usage-data/
```

### 2. Python 脚本执行失败

**场景**：`analyze_html.py` 或 `merge_translations.py` 执行失败

**检测**：
```bash
python3 script.py && echo "SUCCESS" || echo "FAILED"
```

**处理策略**：
1. 检查 Python 版本：`python3 --version`（需要 >= 3.6）
2. 检查脚本权限：`ls -l script.py`（需要可执行权限）
3. 查看错误消息：捕获 stderr
4. 提供修复建议

**用户提示**：
```
❌ 脚本执行失败

错误信息：{stderr}

修复建议：
1. 检查 Python 版本：python3 --version
2. 修复脚本权限：chmod +x {baseDir}/*.py
3. 查看详细日志
```

### 3. 翻译失败

**场景**：某个 chunk 的翻译任务失败或超时

**检测**：
- TaskOutput 返回错误状态
- 翻译结果为空
- 翻译结果格式错误

**处理策略**：
1. 记录失败的 chunk ID 和原因
2. 使用原文作为后备（`translation = original`）
3. 在最终报告中添加注释：`<!-- 翻译失败：{reason} -->`
4. 继续处理其他 chunk
5. 在完成提示中列出失败的 chunk

**用户提示**：
```
⚠️ 部分文本翻译失败

失败的块：[2, 5]
原因：翻译任务超时

已使用原文填充，请检查 report-zh.html 中的标记注释。
```

### 4. 合并失败

**场景**：`merge_translations.py` 执行失败或输出文件格式错误

**检测**：
```bash
python3 -m json.tool /tmp/insights-analysis.json
```

**处理策略**：
1. 验证 JSON 格式是否正确
2. 检查每个 block 是否有 `translation` 字段
3. 尝试逐个替换而非批量替换
4. 提供详细的错误日志
5. 生成部分翻译的文件（尽可能恢复）

**用户提示**：
```
❌ 合并翻译结果失败

可能原因：
1. JSON 格式错误
2. 翻译字段缺失
3. HTML 结构损坏

诊断命令：
  python3 -m json.tool /tmp/insights-analysis.json

已生成部分翻译文件：/tmp/report-zh-partial.html
```

### 5. 浏览器打开失败

**场景**：无法在浏览器中打开生成的 HTML 文件

**检测**：
```bash
open ./report-zh.html 2>&1 | grep -i error
```

**处理策略**：
1. 验证文件已成功生成：`ls -lh ./report-zh.html`
2. 尝试不同的打开命令（根据操作系统）
3. 如果失败，提示用户手动打开

**用户提示**：
```
⚠️ 无法自动打开浏览器

文件已生成：./report-zh.html

请手动在浏览器中打开：
  macOS: open ./report-zh.html
  Linux: xdg-open ./report-zh.html
  Windows: start ./report-zh.html
```

## 错误日志

### 日志位置

```
/tmp/insights-zh-debug-{timestamp}.log
```

### 日志内容

```
[INFO] 开始执行 insights-zh 技能
[INFO] 检查源文件：~/.claude/usage-data/report.html
[INFO] 分析 HTML 结构...
[INFO] 提取 120 个文本块，拆分为 8 个 chunk
[INFO] 开始并行翻译...
[INFO] 翻译完成：8/8 成功
[INFO] 合并翻译结果...
[ERROR] 合并失败：JSON 格式错误
[INFO] 生成部分翻译文件
[INFO] 执行完成，部分失败
```

## 健壮性改进建议

### 1. 输入验证

```python
def validate_html_file(path):
    """验证 HTML 文件是否有效"""
    if not os.path.exists(path):
        raise FileNotFoundError(f"文件不存在：{path}")
    if not path.endswith('.html'):
        raise ValueError(f"不是 HTML 文件：{path}")
    with open(path, 'r') as f:
        content = f.read()
        if not content.strip().startswith('<'):
            raise ValueError(f"不是有效的 HTML 文件")
    return True
```

### 2. 翻译结果验证

```python
def validate_translation(original, translation):
    """验证翻译结果是否有效"""
    if not translation:
        return False
    if len(translation) < len(original) * 0.3:
        return False  # 翻译过短，可能失败
    return True
```

### 3. 回退机制

```python
def translate_with_fallback(original):
    """带回退的翻译"""
    try:
        translation = translate(original)
        if validate_translation(original, translation):
            return translation
    except Exception as e:
        log_error(e)
    return original  # 回退到原文
```

## 测试错误处理

### 测试用例

```bash
# 测试文件不存在
rm ~/.claude/usage-data/report.html
/insights-zh
# 预期：显示错误提示

# 测试无效 HTML
echo "invalid" > ~/.claude/usage-data/report.html
/insights-zh
# 预期：捕获格式错误

# 测试部分翻译失败
# 模拟某些翻译任务超时
# 预期：使用原文填充，继续执行
```
