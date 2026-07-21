# JavaScript 重复逻辑合并评估报告

## 一、评估背景

根据项目任务计划，需要消除 `floating-buttons.js` 与 `feedback.js` 之间的重复逻辑，解决两个文件对 `feedbackFloat` 按钮的双重控制问题。

---

## 二、重复逻辑分析

### 2.1 重复位置定位

| 文件 | 位置 | 功能描述 |
|------|------|----------|
| `floating-buttons.js` | 第32-44行 | scroll 事件监听，控制三个浮动按钮的显示/隐藏 |
| `feedback.js` | 第282-290行 | scroll 事件监听，控制 feedbackFloat 的显示/隐藏 |

### 2.2 重复代码对比

**floating-buttons.js 中的滚动控制逻辑（第32-44行）：**

```javascript
var ticking = false;
window.addEventListener('scroll', function() {
  if (!ticking) {
    requestAnimationFrame(function() {
      var show = window.scrollY > threshold;
      if (backToTop) backToTop.classList.toggle('show', show);
      if (backToHome) backToHome.classList.toggle('show', show);
      if (feedbackFloat) feedbackFloat.classList.toggle('show', show);
      ticking = false;
    });
    ticking = true;
  }
}, { passive: true });
```

**feedback.js 中的滚动控制逻辑（第282-290行）：**

```javascript
function updateFloatButtons() {
    const isVisible = window.scrollY > 300;
    feedbackFloat?.classList.toggle('show', isVisible);
}

if (feedbackFloat) {
    updateFloatButtons();
    window.addEventListener('scroll', updateFloatButtons);
}
```

### 2.3 重复特征分析

| 特征 | floating-buttons.js | feedback.js | 重复程度 |
|------|---------------------|-------------|----------|
| scroll 事件监听 | ✅ | ✅ | 完全重复 |
| feedbackFloat 显示控制 | ✅ | ✅ | 完全重复 |
| 阈值判断 | threshold 变量 | 硬编码 300 | 逻辑重复，实现差异 |
| 性能优化 | requestAnimationFrame + ticking | 无优化 | 实现差异 |

### 2.4 代码量占比

- `floating-buttons.js` 总代码：61行 → 滚动控制逻辑占 13行（21%）
- `feedback.js` 总代码：291行 → 滚动控制逻辑占 9行（3%）
- `team_ai_maturity_tool.html` 内联JS：约20行（滚动控制 + 点击事件）
- **重复代码总量：约29行（feedback.js 9行 + 内联JS 20行）**

### 2.5 页面引用情况

| 页面 | floating-buttons.css | floating-buttons.js | feedback.js | 内联滚动JS | 状态 |
|------|---------------------|---------------------|-------------|------------|------|
| articles/zh/spinor-taiji-glossary.html | ✅ | ✅ | ✅ | ❌ | 正常 |
| articles/en/spinor-taiji-glossary.html | ✅ | ✅ | ✅ | ❌ | 正常 |
| articles/zh/spinor-taiji-model-statement.html | ✅ | ✅ | ✅ | ❌ | 正常 |
| articles/en/spinor-taiji-model-declaration.html | ✅ | ✅ | ✅ | ❌ | 正常 |
| articles/zh/team_ai_maturity_tool.html | ✅ | ❌ | ✅ | ✅ | 需要迁移 |
| 33-团队AI成熟度/团队AI成熟度自评工具.html | 需检查 | 需检查 | 需检查 | 需检查 | 独立部署 |

---

## 三、潜在合并方式

### 方案A：移除 feedback.js 中的重复逻辑（推荐）

**核心思路**：保留 `floating-buttons.js` 的滚动控制逻辑（已含性能优化），删除 `feedback.js` 中第282-290行的 `updateFloatButtons()` 函数及其调用。

**优势**：
- `floating-buttons.js` 已使用 `requestAnimationFrame` 优化滚动性能
- `floating-buttons.js` 支持可配置的 `threshold`（通过 `data-show-threshold` 属性）
- 符合单一职责原则：`floating-buttons.js` 负责按钮显示控制，`feedback.js` 负责反馈弹窗逻辑

**风险**：
- 需确保所有页面同时引入 `floating-buttons.js` 和 `feedback.js`

### 方案B：将滚动控制逻辑提取为独立模块

**核心思路**：创建新的 `scroll-controller.js`，统一管理所有滚动相关逻辑。

**优势**：
- 更高的模块化程度
- 便于未来扩展其他滚动行为

**风险**：
- 增加文件数量和复杂度
- 需要更新所有页面的脚本引用

### 方案C：将滚动控制逻辑移入 feedback.js

**核心思路**：删除 `floating-buttons.js` 中的滚动控制，统一由 `feedback.js` 管理。

**优势**：
- 减少文件间依赖

**风险**：
- `floating-buttons.js` 失去核心功能
- 需重构 `floating-buttons.js` 的职责定位
- 丢失 `requestAnimationFrame` 性能优化

---

## 四、推荐方案：方案A

### 4.1 实施步骤

**步骤1：删除 feedback.js 中的重复代码**
- 删除第282-285行的 `updateFloatButtons()` 函数定义
- 删除第287-290行的函数调用和事件监听

**步骤2：迁移团队AI成熟度工具页面**
- 在 `team_ai_maturity_tool.html` 中引入 `floating-buttons.js`
- 将 `backToHomeBtn` 的 `onclick` 改为 `data-home-url` 属性
- 删除内联的滚动控制JS（第391-413行）

**步骤3：验证页面功能**
- 确认所有页面同时引入 `floating-buttons.js` 和 `feedback.js`
- 验证滚动时反馈按钮的显示/隐藏行为正常
- 验证返回顶部、返回首页按钮行为正常

**步骤4：运行验证脚本**
- 执行 `python scripts/validate_before_commit.py` 确保代码质量

### 4.2 预期收益

| 指标 | 合并前 | 合并后 | 改进 |
|------|--------|--------|------|
| scroll 事件监听器数量 | 2个 | 1个 | -50% |
| 重复代码行数 | 9行 | 0行 | -100% |
| 性能优化 | 部分优化 | 统一优化 | ✅ |
| 阈值可配置性 | 部分可配 | 完全可配 | ✅ |
| 维护成本 | 双文件维护 | 单文件维护 | 降低 |

### 4.3 风险评估

| 风险 | 概率 | 影响 | 应对措施 |
|------|------|------|----------|
| 页面未引入 floating-buttons.js | 低 | 高 | 检查所有页面的脚本引用 |
| 滚动性能下降 | 无风险 | - | floating-buttons.js 已有 requestAnimationFrame 优化 |
| 功能回归 | 低 | 中 | 执行完整测试用例 |

---

## 五、确认文档

### 5.1 合并方案确认

```
确认项：删除 feedback.js 中第282-290行的重复滚动控制逻辑
合并方式：方案A（移除 feedback.js 中的重复逻辑）
保留逻辑：floating-buttons.js 中的滚动控制（含 requestAnimationFrame 优化）
```

### 5.2 实施步骤确认

```
步骤1：删除 feedback.js 第282-290行代码 ✅ 已完成
步骤2：迁移 team_ai_maturity_tool.html（引入 floating-buttons.js，删除内联JS） ✅ 已完成
步骤3：验证所有页面同时引入 floating-buttons.js 和 feedback.js ✅ 已完成
步骤4：运行本地验证脚本 ✅ 已完成
步骤5：提交代码并推送 ⬜ 待执行
```

### 5.4 实施结果

| 操作 | 文件 | 修改内容 | 结果 |
|------|------|----------|------|
| 删除重复代码 | feedback.js | 删除第282-290行 updateFloatButtons() 函数及事件监听 | ✅ |
| 属性修改 | team_ai_maturity_tool.html | onclick → data-home-url 属性 | ✅ |
| 删除内联JS | team_ai_maturity_tool.html | 删除第391-413行滚动控制和点击事件代码 | ✅ |
| 添加引用 | team_ai_maturity_tool.html | 添加 `<script src="/assets/floating-buttons.js">` | ✅ |
| 验证 | validate_before_commit.py | 所有检查通过 | ✅ |

### 5.3 验证标准

```
1. 滚动 >300px 时，三个浮动按钮（返回顶部、返回首页、反馈建议）均显示
2. 滚动 <300px 时，三个浮动按钮均隐藏
3. 点击反馈按钮可打开反馈弹窗
4. 点击返回顶部按钮可平滑滚动到页面顶部
5. 点击返回首页按钮可跳转到首页
6. validate_before_commit.py 所有检查通过
```

---

**评估完成日期**：2026-07-21  
**评估人**：系统自动生成  
**文档版本**：V1.0
