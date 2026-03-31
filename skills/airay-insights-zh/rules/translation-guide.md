# HTML 翻译指南

本指南提供将英文 HTML 内容翻译为中文的详细规则和示例。

## 核心原则

1. **保留 HTML 结构不变**：所有标签、属性、样式都必须完整保留
2. **只翻译文本内容**：仅翻译用户可见的文本节点
3. **保持格式完整**：缩进、换行、空格都应保持原样

## 翻译规则

### 1. 保留不翻译的内容

#### 1.1 HTML 标签和属性

**不要翻译**:
- HTML 标签名：`<div>`, `<span>`, `<h1>`, `<p>`, `<a>`, etc.
- HTML 属性名：`class`, `id`, `style`, `href`, `src`, `data-*`, etc.
- HTML 属性值：`class="container"`, `id="header"`, `data-value="123"`

**示例**:

```html
<!-- 输入 -->
<div class="header" id="main-header" data-theme="dark">
  <h1>Project Overview</h1>
</div>

<!-- 输出 -->
<div class="header" id="main-header" data-theme="dark">
  <h1>项目概览</h1>
</div>
```

#### 1.2 CSS 代码（`<style>` 标签内）

**完全保留** `<style>` 标签内的所有内容，不做任何翻译。

**示例**:

```html
<!-- 输入 -->
<style>
  .container {
    max-width: 1200px;
    margin: 0 auto;
  }
  .header {
    background-color: #f5f5f5;
    padding: 20px;
  }
</style>

<!-- 输出 -->
<style>
  .container {
    max-width: 1200px;
    margin: 0 auto;
  }
  .header {
    background-color: #f5f5f5;
    padding: 20px;
  }
</style>
```

#### 1.3 JavaScript 代码（`<script>` 标签内）

**完全保留** `<script>` 标签内的所有内容，不做任何翻译。

**示例**:

```html
<!-- 输入 -->
<script>
  function handleClick() {
    console.log('Button clicked');
    alert('Action completed');
  }
</script>

<!-- 输出 -->
<script>
  function handleClick() {
    console.log('Button clicked');
    alert('Action completed');
  }
</script>
```

#### 1.4 内联样式

**保留** 所有内联样式代码。

**示例**:

```html
<!-- 输入 -->
<div style="color: #333; font-size: 16px; margin: 10px 0;">
  This is a text with inline styles.
</div>

<!-- 输出 -->
<div style="color: #333; font-size: 16px; margin: 10px 0;">
  这是带有内联样式的文本。
</div>
```

#### 1.5 代码块和代码片段

**保留** 技术术语、代码语法、API 名称等。

**示例**:

```html
<!-- 输入 -->
<p>Use the <code>TaskCreate</code> tool to create a new task.</p>
<pre>const result = await fetch('/api/data');</pre>

<!-- 输出 -->
<p>使用 <code>TaskCreate</code> 工具创建新任务。</p>
<pre>const result = await fetch('/api/data');</pre>
```

### 2. 需要翻译的内容

#### 2.1 标题和文本

**翻译** 所有标题和段落文本。

**示例**:

```html
<!-- 输入 -->
<h1>Project Structure</h1>
<p>This project contains multiple modules for handling different tasks.</p>

<!-- 输出 -->
<h1>项目结构</h1>
<p>本项目包含多个用于处理不同任务的模块。</p>
```

#### 2.2 链接

**翻译** 链接文本，但保留 `href` 属性。

**示例**:

```html
<!-- 输入 -->
<a href="https://example.com/docs">Documentation</a>

<!-- 输出 -->
<a href="https://example.com/docs">文档</a>
```

#### 2.3 按钮和表单元素

**翻译** 按钮文本、标签、占位符等。

**示例**:

```html
<!-- 输入 -->
<button type="submit">Save Changes</button>
<label for="email">Email Address</label>
<input type="email" id="email" placeholder="Enter your email">

<!-- 输出 -->
<button type="submit">保存更改</button>
<label for="email">电子邮件地址</label>
<input type="email" id="email" placeholder="请输入您的电子邮件">
```

#### 2.4 表格内容

**翻译** 表头和单元格内容，但保留表格结构。

**示例**:

```html
<!-- 输入 -->
<table>
  <thead>
    <tr>
      <th>File Name</th>
      <th>Size</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>index.html</td>
      <td>2.5 KB</td>
      <td>Active</td>
    </tr>
  </tbody>
</table>

<!-- 输出 -->
<table>
  <thead>
    <tr>
      <th>文件名</th>
      <th>大小</th>
      <th>状态</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>index.html</td>
      <td>2.5 KB</td>
      <td>活跃</td>
    </tr>
  </tbody>
</table>
```

#### 2.5 列表

**翻译** 列表项内容。

**示例**:

```html
<!-- 输入 -->
<ul>
  <li>Execute the command</li>
  <li>Translate the output</li>
  <li>Save the file</li>
</ul>

<!-- 输出 -->
<ul>
  <li>执行命令</li>
  <li>翻译输出</li>
  <li>保存文件</li>
</ul>
```

### 3. 特殊情况处理

#### 3.1 混合内容（标签 + 文本）

**只翻译** 文本部分，保留标签。

**示例**:

```html
<!-- 输入 -->
<p>Welcome to <strong>Insights</strong>, the code analysis tool.</p>

<!-- 输出 -->
<p>欢迎使用 <strong>Insights</strong>，代码分析工具。</p>
```

#### 3.2 HTML 注释

**选项 1**: 保留原文（推荐）
**选项 2**: 翻译注释内容

**示例**:

```html
<!-- 输入 -->
<!-- This section displays the main content -->
<div>Main Content</div>

<!-- 输出（选项 1）-->
<!-- This section displays the main content -->
<div>主要内容</div>

<!-- 输出（选项 2）-->
<!-- 本部分显示主要内容 -->
<div>主要内容</div>
```

#### 3.3 数据属性

**保留** `data-*` 属性值。

**示例**:

```html
<!-- 输入 -->
<div data-section="overview" data-index="1">
  <h2>Overview</h2>
</div>

<!-- 输出 -->
<div data-section="overview" data-index="1">
  <h2>概览</h2>
</div>
```

#### 3.4 ARIA 属性

**翻译** ARIA 标签和描述文本，但保留属性名。

**示例**:

```html
<!-- 输入 -->
<button aria-label="Close dialog">×</button>
<div role="status" aria-live="polite">Loading...</div>

<!-- 输出 -->
<button aria-label="关闭对话框">×</button>
<div role="status" aria-live="polite">加载中...</div>
```

#### 3.5 时间和日期

**翻译** 日期格式，或保留 ISO 格式。

**示例**:

```html
<!-- 输入 -->
<p>Created on January 15, 2025</p>
<time datetime="2025-01-15">2025-01-15</time>

<!-- 输出 -->
<p>创建于 2025 年 1 月 15 日</p>
<time datetime="2025-01-15">2025-01-15</time>
```

### 4. 常见模式示例

#### 4.1 导航栏

```html
<!-- 输入 -->
<nav class="navbar">
  <div class="nav-brand">Insights</div>
  <ul class="nav-menu">
    <li><a href="#overview">Overview</a></li>
    <li><a href="#features">Features</a></li>
    <li><a href="#docs">Documentation</a></li>
  </ul>
</nav>

<!-- 输出 -->
<nav class="navbar">
  <div class="nav-brand">Insights</div>
  <ul class="nav-menu">
    <li><a href="#overview">概览</a></li>
    <li><a href="#features">功能</a></li>
    <li><a href="#docs">文档</a></li>
  </ul>
</nav>
```

#### 4.2 卡片组件

```html
<!-- 输入 -->
<div class="card">
  <h3 class="card-title">Quick Start</h3>
  <p class="card-description">Get started with Insights in 3 simple steps.</p>
  <button class="btn-primary">Get Started</button>
</div>

<!-- 输出 -->
<div class="card">
  <h3 class="card-title">快速开始</h3>
  <p class="card-description">通过 3 个简单步骤开始使用 Insights。</p>
  <button class="btn-primary">开始使用</button>
</div>
```

#### 4.3 状态消息

```html
<!-- 输入 -->
<div class="alert alert-success">
  <strong>Success!</strong> Your changes have been saved.
</div>
<div class="alert alert-error">
  <strong>Error:</strong> Failed to load configuration.
</div>

<!-- 输出 -->
<div class="alert alert-success">
  <strong>成功！</strong> 您的更改已保存。
</div>
<div class="alert alert-error">
  <strong>错误：</strong> 加载配置失败。
</div>
```

### 5. 翻译质量检查清单

翻译完成后，请检查：

- [ ] 所有 HTML 标签完整保留
- [ ] 所有 HTML 属性未修改
- [ ] `<style>` 标签内容未翻译
- [ ] `<script>` 标签内容未翻译
- [ ] CSS 类名和 ID 未翻译
- [ ] 代码块和技术术语保留原文
- [ ] 链接的 `href` 属性保持不变
- [ ] 文本内容准确翻译为中文
- [ ] HTML 缩进和格式保持一致
- [ ] 可以在浏览器中正常打开和显示

### 6. 测试方法

1. **语法检查**: 在浏览器中打开翻译后的 HTML 文件
2. **格式验证**: 检查页面布局是否与原文一致
3. **内容检查**: 确认所有可见文本已翻译
4. **功能检查**: 测试链接、按钮是否正常工作

## 常见错误示例

### 错误 1: 翻译了类名

```html
<!-- 错误 -->
<div class="页眉">Header</div>

<!-- 正确 -->
<div class="header">页眉</div>
```

### 错误 2: 翻译了 CSS 代码

```html
<!-- 错误 -->
<style>
  .容器 {
    最大宽度: 1200px;
  }
</style>

<!-- 正确 -->
<style>
  .container {
    max-width: 1200px;
  }
</style>
```

### 错误 3: 破坏了 HTML 结构

```html
<!-- 错误 -->
<h1>标题</h1
<p>段落</p>

<!-- 正确 -->
<h1>标题</h1>
<p>段落</p>
```

### 错误 4: 翻译了代码块内容

```html
<!-- 错误 -->
<code>任务创建</code>

<!-- 正确 -->
<code>TaskCreate</code>
```

## 总结

记住：**只翻译用户可见的文本内容，保留所有 HTML 结构、样式和代码不变**。
