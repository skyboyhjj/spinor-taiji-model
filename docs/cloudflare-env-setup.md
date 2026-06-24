# Cloudflare Pages 环境变量配置指南

## 概述

反馈系统依赖 Cloudflare Pages Function 将用户提交的反馈自动创建为 GitHub Issue。这需要配置 `GITHUB_TOKEN` 环境变量，使后端服务能够调用 GitHub API。

整个过程分为两步：
1. 在 GitHub 生成 Personal Access Token
2. 在 Cloudflare Pages 仪表板中配置环境变量

---

## 第一步：生成 GitHub Personal Access Token

### 1.1 进入 GitHub Token 设置页面

打开 https://github.com/settings/tokens

> 也可通过以下路径进入：GitHub 右上角头像 → **Settings** → 左侧菜单 **Developer settings** → **Personal access tokens** → **Tokens (classic)**

### 1.2 创建新 Token

点击 **「Generate new token」** → 选择 **「Generate new token (classic)」**

| 字段 | 填写内容 |
|------|---------|
| **Note** | `spinor-taiji-feedback`（用于标识此 Token 的用途） |
| **Expiration** | 建议选择 `No expiration` 或 `90 days` 后记得续期 |

### 1.3 勾选权限范围

在 **Select scopes** 区域，勾选以下权限：

```
repo
  ☑ repo:status
  ☑ repo_deployment
  ☑ public_repo
  ☑ repo:invite
```

> 实际上只需勾选最顶层的 **「repo」** 复选框，它会自动包含所有子权限。

完整权限清单如下：

| 权限 | 说明 |
|------|------|
| `repo` | 允许读写仓库（包括创建 Issues） |

### 1.4 生成并复制 Token

点击页面底部的 **「Generate token」** 按钮。

> ⚠️ **重要**：生成后页面会显示 Token 值（格式为 `ghp_xxxxxxxxxxxxxxxxxxxx`）。**请立即复制并保存**，离开此页面后将无法再次查看。如果丢失，需要重新生成。

---

## 第二步：在 Cloudflare Pages 配置环境变量

### 2.1 进入项目仪表板

打开 Cloudflare Dashboard：https://dash.cloudflare.com/

选择你的项目 **「spinor-taiji-model」**。

### 2.2 进入环境变量设置

点击顶部导航栏的 **「Settings」** 标签页 → 左侧菜单选择 **「Environment variables」**

### 2.3 添加环境变量

点击 **「Add variable」** 按钮，填写：

| 字段 | 填写内容 |
|------|---------|
| **Variable name** | `GITHUB_TOKEN` |
| **Value** | 粘贴第一步生成的 Token（如 `ghp_xxxxxxxxxxxxxxxxxxxx`） |

> 确保 Production 和 Preview 环境都选中（默认即是）。

### 2.4 保存并部署

点击页面底部的 **「Save」** 按钮。

保存后，Cloudflare Pages 会自动触发一次重新部署，使新的环境变量生效。你可以在 **「Deployments」** 标签页查看部署进度。

---

## 第三步：验证配置是否生效

### 3.1 等待部署完成

在 **「Deployments」** 标签页中，确认最新一次部署状态为 **「Active」**（绿色标记）。

### 3.2 测试反馈提交

1. 打开你的网站页面（如 `https://spinortaiji.com/articles/zh/spinor-taiji-model-statement.html`）
2. 滚动页面，右下角出现 **📬 反馈** 浮动按钮
3. 点击按钮，填写反馈表单并提交
4. 如果看到 **🎉 感谢你的反馈！**，说明配置成功
5. 检查 GitHub 仓库 [skyboyhjj/spinor-taiji-model](https://github.com/skyboyhjj/spinor-taiji-model/issues) 的 Issues 页面，确认新 Issue 已自动创建

### 3.3 故障排查

| 错误信息 | 可能原因 | 解决方法 |
|---------|---------|---------|
| 提交失败（GitHub API 错误） | Token 权限不足或已过期 | 检查 Token 是否勾选了 `repo` 权限，是否过期 |
| 提交失败，请稍后重试 | 网络超时或 Token 未配置 | 检查环境变量名称是否为 `GITHUB_TOKEN`，确认已保存并重新部署 |
| 网络错误 | 客户端网络问题 | 检查网络连接，或通过微信公众号「TS爱心联盟」提交 |

---

## 安全提示

- **不要**将 `GITHUB_TOKEN` 写入代码或提交到 Git 仓库
- 如果 Token 泄露，立即在 GitHub Token 设置页面点击 **「Regenerate token」** 使其失效，然后更新 Cloudflare 环境变量
- 建议定期检查 Token 有效期，在到期前续期