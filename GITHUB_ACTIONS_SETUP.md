# GitHub Actions 配置指南

## 概述

本指南将帮助您配置 GitHub Actions 以实现夸克网盘的自动签到功能，并支持企业微信通知。

## 前置条件

1. 一个 GitHub 账号
2. 夸克网盘账号
3. 企业微信账号（用于接收通知）

## 配置步骤

### 步骤 1：获取夸克网盘 Cookie

1. 在浏览器中登录夸克网盘网页版
2. 打开浏览器开发者工具（F12）
3. 切换到 Network 标签
4. 刷新页面，找到任意请求
5. 在请求头中找到 Cookie
6. 复制完整的 Cookie 值

### 步骤 2：获取企业微信 Webhook URL

1. 登录企业微信管理后台
2. 进入"应用管理" > "创建应用"
3. 创建一个机器人应用
4. 在应用详情中找到"Webhook 地址"
5. 复制完整的 Webhook URL

### 步骤 3：在 GitHub 中配置 Secrets

1. 打开您的 GitHub 仓库
2. 进入 Settings > Secrets and variables > Actions
3. 点击 "New repository secret" 添加以下 secrets：

#### 必需的 Secrets

- **COOKIE_QUARK**
  - 值：步骤 1 中获取的夸克网盘 Cookie
  - 说明：如果有多个账号，用 `\n` 或 `&&` 分隔

- **WEBHOOK_URL**
  - 值：步骤 2 中获取的企业微信 Webhook URL
  - 说明：用于发送签到结果通知

### 步骤 4：配置 GitHub Actions 权限

1. 进入仓库的 Settings > Actions > General
2. 在 "Workflow permissions" 部分
3. 选择 "Read and write permissions"
4. 勾选 "Allow GitHub Actions to create and approve pull requests"
5. 点击 "Save" 保存

### 步骤 5：创建 Personal Access Token（如需手动触发）

1. 进入 GitHub Settings > Developer settings > Personal access tokens
2. 点击 "Generate new token (classic)"
3. 设置 token 名称和过期时间
4. 勾选以下权限：
   - `repo`（完整仓库访问权限）
   - `workflow`（用于创建和更新 workflow 文件）
5. 点击 "Generate token"
6. 复制生成的 token（注意：token 只显示一次）

### 步骤 6：验证 Workflow 文件

确保仓库中存在以下文件：

**文件路径**：`.github/workflows/quark_sign.yml`

**文件内容**：
```yaml
name: Quark Auto Sign-in

on:
  schedule:
    - cron: '0 10 * * *'
  workflow_dispatch:

permissions:
  contents: read
  actions: write

jobs:
  quark-sign:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      actions: write
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: |
          python -m pip install requests

      - name: Run Quark Sign-in
        env:
          COOKIE_QUARK: ${{ secrets.COOKIE_QUARK }}
          WEBHOOK_URL: ${{ secrets.WEBHOOK_URL }}
        run: |
          python quark_sign.py
```

## Workflow 说明

### 定时执行

- 默认配置：每天北京时间 18:00 执行（UTC 时间 10:00）
- Cron 表达式：`0 10 * * *`
- 时区：UTC（协调世界时）

### 手动触发

- 支持通过 GitHub Actions 页面手动触发
- 进入 Actions > Quark Auto Sign-in > Run workflow

### 执行权限

- `contents: read` - 读取仓库内容
- `actions: write` - 写入 Actions 相关信息

## 配置企业微信通知

### 在个人微信中接收企业微信通知

1. **下载企业微信**
   - 在应用商店搜索"企业微信"并下载安装
   - 使用手机号注册或使用微信登录

2. **加入企业**
   - 联系企业管理员获取邀请链接或二维码
   - 通过邀请加入企业

3. **关注应用**
   - 进入企业微信应用
   - 找到"应用"或"工作台"
   - 搜索并关注"夸克自动签到"应用
   - 开启消息通知

4. **接收通知**
   - 确保企业微信应用有通知权限
   - 在手机设置中允许企业微信发送通知
   - 签到成功后，您将收到签到结果通知

## 测试配置

### 方法 1：手动触发 Workflow

1. 进入仓库的 Actions 页面
2. 选择 "Quark Auto Sign-in" workflow
3. 点击 "Run workflow"
4. 选择分支（通常是 main）
5. 点击 "Run workflow" 按钮
6. 等待执行完成，查看运行日志

### 方法 2：查看执行日志

1. 进入 Actions 页面
2. 点击最近一次的 workflow 运行记录
3. 展开各个步骤查看详细日志
4. 检查是否有错误信息

## 常见问题

### 1. Workflow 执行失败

**问题**：Workflow 执行时出现错误

**解决方案**：
- 检查 Secrets 是否正确配置
- 查看 Actions 日志获取详细错误信息
- 确认 Cookie 是否有效（可能需要重新获取）

### 2. 未收到企业微信通知

**问题**：签到成功但未收到通知

**解决方案**：
- 检查 WEBHOOK_URL 是否正确
- 确认企业微信应用配置正确
- 检查个人微信是否已关注应用
- 查看 Actions 日志确认通知是否发送

### 3. Cookie 失效

**问题**：签到失败，提示 Cookie 无效

**解决方案**：
- 重新获取夸克网盘 Cookie
- 更新 GitHub Secrets 中的 COOKIE_QUARK
- 确保在浏览器中已登录夸克网盘

### 4. 定时任务未执行

**问题**：定时任务没有按预期执行

**解决方案**：
- 检查 Cron 表达式是否正确
- 确认 Workflow 文件在正确的分支上
- 查看 Actions 页面确认是否有执行记录

## 安全建议

1. **保护敏感信息**
   - 不要将 Cookie 和 Webhook URL 提交到代码仓库
   - 定期更新 Personal Access Token
   - 使用最小权限原则配置 Secrets

2. **定期检查**
   - 定期查看 Actions 执行日志
   - 监控异常活动
   - 及时更新依赖库

3. **备份配置**
   - 记录重要的配置信息
   - 保存 Workflow 文件的备份
   - 定期测试配置的有效性

## 高级配置

### 修改执行时间

编辑 `.github/workflows/quark_sign.yml` 文件中的 cron 表达式：

```yaml
schedule:
  - cron: '0 10 * * *'  # 每天 UTC 10:00 执行
```

Cron 表达式格式：`分 时 日 月 周`

示例：
- `0 2 * * *` - 每天 UTC 2:00（北京时间 10:00）
- `0 */6 * * *` - 每 6 小时执行一次
- `0 10 * * 1-5` - 工作日每天 UTC 10:00 执行

### 多账号配置

如果有多个夸克账号，用 `\n` 或 `&&` 分隔 Cookie：

```
cookie1=value1;cookie2=value2
cookie1=value1;cookie2=value2
```

### 自定义通知内容

修改 `quark_sign.py` 中的 `send_to_wxwork` 函数来自定义通知格式。

## 维护和更新

### 更新代码

1. 在本地修改代码
2. 提交到 GitHub
3. Workflow 会自动使用最新代码执行

### 更新 Secrets

1. 进入 Settings > Secrets and variables > Actions
2. 找到需要更新的 secret
3. 点击 "Update" 更新值
4. 保存更改

### 监控执行状态

1. 定期查看 Actions 页面
2. 设置 GitHub 通知（可选）
3. 关注企业微信通知

## 联系支持

如遇到问题，请：
1. 查看本文档的常见问题部分
2. 检查 GitHub Actions 日志
3. 提交 Issue 到仓库

## 附录

### Cron 表达式参考

| 表达式 | 说明 |
|--------|------|
| `0 10 * * *` | 每天 10:00 |
| `0 */6 * * *` | 每 6 小时 |
| `0 10 * * 1-5` | 工作日 10:00 |
| `0 10 1 * *` | 每月 1 日 10:00 |
| `0 10,18 * * *` | 每天 10:00 和 18:00 |

### GitHub Actions 权限说明

| 权限 | 说明 |
|------|------|
| `contents: read` | 读取仓库内容 |
| `contents: write` | 写入仓库内容 |
| `actions: read` | 读取 Actions 信息 |
| `actions: write` | 写入 Actions 信息 |

---

**最后更新**：2026-03-05
**版本**：1.0.0