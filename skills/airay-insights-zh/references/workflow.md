# 详细工作流程

本文档提供 insights-zh 技能的详细工作流程说明。

## 文本块分析策略

### analyze_html.py 工作原理

1. **HTML 解析**：使用 Python 的 `HTMLParser` 解析 HTML 结构
2. **文本提取**：提取所有非 script/style 标签内的文本
3. **上下文记录**：记录每个文本块的上下文（所在标签层级）
4. **均衡分配**：按字符长度均衡分配到 8-10 个块中

### 输出格式

生成的 `/tmp/insights-analysis.json` 格式：

```json
{
  "total_blocks": 120,
  "chunks": [
    {
      "id": 0,
      "blocks": [
        {
          "index": 0,
          "original": "Original text",
          "context": "h1 > div",
          "translation": null
        }
      ]
    }
  ]
}
```

## 翻译策略

### 并行执行加速

- 所有 chunks 同时翻译，大幅提升速度
- 使用 haiku 模型降低延迟和成本
- 每个块独立翻译，避免长度限制

### 翻译代理提示模板

```
你是专业的技术文档翻译专家。将以下文本块翻译为中文。

## 重要规则

1. **必须保留**：
   - 所有 HTML 标签（<div>、<span>、<a> 等）
   - HTML 属性名和值（class、id、style、href 等）
   - CSS 类名和 ID
   - 代码和技术术语

2. **需要翻译**：
   - 用户可见的文本内容
   - 标题、段落、按钮文本
   - 链接文本（保留 href 属性）

3. **保持格式**：
   - 缩进和换行
   - HTML 结构完整
   - 确保翻译后 HTML 语法正确

## 待翻译文本块

{blocks}

## 输出格式

返回 JSON 数组，每个元素对应一个翻译后的文本块：
["翻译1", "翻译2", ...]
```

## 合并策略

### merge_translations.py 工作原理

1. **按长度降序替换**：避免短文本被先替换导致的误匹配
2. **精确匹配**：只替换完全匹配的原始文本
3. **保留结构**：保留所有 HTML 标签和属性
4. **文本节点替换**：只替换文本节点内容

### 合并算法

```python
# 按原始文本长度降序排序（避免短文本误匹配）
sorted_blocks = sorted(blocks, key=lambda b: len(b['original']), reverse=True)

html_content = original_html
for block in sorted_blocks:
    if block['translation']:
        html_content = html_content.replace(
            block['original'],
            block['translation']
        )
```

## 完整示例

### 输入 HTML

```html
<div class="container">
  <h1>Weekly Insights</h1>
  <p>You wrote 5000 lines of code.</p>
</div>
```

### 分析结果

```json
{
  "total_blocks": 2,
  "chunks": [
    {
      "id": 0,
      "blocks": [
        {
          "index": 0,
          "original": "Weekly Insights",
          "context": "h1",
          "translation": null
        },
        {
          "index": 1,
          "original": "You wrote 5000 lines of code.",
          "context": "p",
          "translation": null
        }
      ]
    }
  ]
}
```

### 翻译结果

```json
{
  "total_blocks": 2,
  "chunks": [
    {
      "id": 0,
      "blocks": [
        {
          "index": 0,
          "original": "Weekly Insights",
          "context": "h1",
          "translation": "每周洞察"
        },
        {
          "index": 1,
          "original": "You wrote 5000 lines of code.",
          "context": "p",
          "translation": "您编写了 5000 行代码。"
        }
      ]
    }
  ]
}
```

### 输出 HTML

```html
<div class="container">
  <h1>每周洞察</h1>
  <p>您编写了 5000 行代码。</p>
</div>
```
