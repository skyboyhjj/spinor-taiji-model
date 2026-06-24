# GitHub Issue 创建功能验证报告

> 验证日期：2026-06-24
> 验证范围：反馈系统端到端代码审查

---

## 一、验证矩阵

| 验证项 | 结果 | 详情 |
|--------|:----:|------|
| 前后端接口契约 | ✅ 通过 | 请求体字段 `{type, source, content, contact}` 完全匹配 |
| HTTP 方法与路由 | ✅ 通过 | 前端 POST `/api/feedback` → Function `onRequestPost` |
| 客户端输入验证 | ✅ 通过 | 三页面均校验 content ≥ 5 字符 |
| 服务端输入验证 | ✅ 通过 | 校验 JSON 格式 + content 长度 |
| GitHub API 端点 | ✅ 已修复 | 原使用不存在标签导致 422，已移除 labels 参数 |
| CORS 处理 | ✅ 通过 | OPTIONS 预检 + Access-Control-Allow-Origin |
| 错误处理 | ✅ 通过 | 分层错误码（400/500/502），含 detail 字段 |
| 环境变量读取 | ✅ 通过 | `env.GITHUB_TOKEN` 标准 Cloudflare 方式 |
| 词汇表重复代码 | ✅ 已修复 | 移除第 789-826 行重复的 related-link 事件处理 |

---

## 二、发现的问题与修复

### 问题 1：自定义标签不存在（严重）

**发现**：GitHub 仓库只有 9 个默认标签，没有 `status:triage`、`source:statement`、`type:suggestion` 等自定义标签。

**影响**：GitHub API 在创建 Issue 时遇到不存在的标签名会返回 `422 Unprocessable Entity`，导致所有反馈提交失败。

**修复**：从 API 请求体中移除 `labels` 参数，将标签信息改为写入 Issue body 的引用块中：

```markdown
> 标签: `status:triage` `source:statement` `type:suggestion`
```

**修复文件**：[functions/api/feedback.js](file:///E:/Trac%20Project/spinor-taiji-model/functions/api/feedback.js) 第 51-54 行

### 问题 2：错误信息未回传（中等）

**发现**：`errorText` 变量被读取但未包含在响应中，排查问题时无法获取 GitHub 返回的具体错误原因。

**修复**：在 502 错误响应中添加 `detail` 字段，包含 GitHub API 的原始错误信息。

### 问题 3：词汇表页面重复代码（低）

**发现**：[spinor-taiji-glossary.html](file:///E:/Trac%20Project/spinor-taiji-model/articles/zh/spinor-taiji-glossary.html) 第 789-826 行与第 751-788 行的 `related-link` 事件处理代码完全重复，导致每个相关词条被绑定两次事件。

**修复**：移除重复代码块。

---

## 三、数据流端到端验证

```
用户点击「提交反馈」
    │
    ▼
前端: fetch POST /api/feedback
    │  body: { type: "suggestion", source: "statement", content: "...", contact: "..." }
    │
    ▼
Function: onRequestPost()
    ├─ 解析 JSON ──失败──→ 400 "请求格式无效"
    ├─ 校验 content ≥ 5 ──失败──→ 400 "反馈内容不能为空或过短"
    ├─ 构建 Issue 标题和正文
    └─ fetch POST https://api.github.com/repos/skyboyhjj/spinor-taiji-model/issues
           │
           ├─ 成功 (201) ──→ 返回 { success: true, url: "https://..." }
           ├─ 失败 (4xx/5xx) ──→ 返回 502 + detail
           └─ 网络异常 ──→ 返回 500
```

---

## 四、预期 Issue 格式

提交后将生成如下 Issue：

**标题**：`[反馈] 建议 - 声明`

**正文**：
```markdown
## 反馈详情

- **类型**: 建议
- **来源**: 声明

[用户提交的反馈内容]

- **联系方式**: user@example.com

---
> 标签: `status:triage` `source:statement` `type:suggestion`

*此 Issue 由用户通过页面反馈表单自动提交*
```

---

## 五、部署前检查清单

| 序号 | 检查项 | 状态 |
|:----:|--------|:----:|
| 1 | `GITHUB_TOKEN` 环境变量已配置 | ⬜ 待部署时完成 |
| 2 | Token 具备 `repo` 权限 | ⬜ 待确认 |
| 3 | `functions/api/feedback.js` 已部署 | ⬜ 待部署 |
| 4 | 三个页面均已包含浮动按钮 + 弹窗 | ✅ |
| 5 | 各页面 `source` 参数正确（statement/glossary） | ✅ |
| 6 | 部署后提交一条测试反馈验证 | ⬜ 待执行 |

---

## 六、手动测试步骤

部署完成后，按以下步骤验证：

1. 打开 `https://spinortaiji.com/articles/zh/spinor-taiji-model-statement.html`
2. 滚动页面，点击右下角 **📬 反馈** 按钮
3. 填写表单：
   - 类型：改进建议
   - 内容：`这是一条自动化验证测试反馈，请忽略。`
   - 联系方式：留空
4. 点击「提交反馈」
5. **预期结果**：弹窗显示 🎉 感谢页面
6. 打开 https://github.com/skyboyhjj/spinor-taiji-model/issues 确认新 Issue 已创建
7. 关闭测试 Issue（通过 GitHub 界面 Close issue）