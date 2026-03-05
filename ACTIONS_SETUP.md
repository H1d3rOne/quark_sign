# Quark Sign - GitHub Actions Setup Guide

## GitHub Actions 自动签到配置

本项目已配置GitHub Actions自动执行夸克网盘签到功能。

## 配置步骤

### 1. 添加Repository Secret

1. 进入GitHub仓库页面：https://github.com/H1d3rOne/quark_sign/settings/secrets/actions
2. 点击 "New repository secret" 按钮
3. 添加以下Secret：
   - Name: `COOKIE_QUARK`
   - Value: 你的夸克网盘Cookie信息（支持多个账号，用换行符或&&分隔）

### 2. Cookie格式

单个账号格式：
```
user=用户名; kps=加密的kps值; sign=加密的sign值; vcode=vcode值
```

多个账号格式（用换行符或&&分隔）：
```
user=账号1; kps=xxx; sign=xxx; vcode=xxx
user=账号2; kps=xxx; sign=xxx; vcode=xxx
```

### 3. 手动触发

如果需要立即执行签到：
1. 进入GitHub仓库的Actions页面
2. 选择 "Quark Auto Sign-in" workflow
3. 点击 "Run workflow" 按钮

### 4. 自动执行

GitHub Actions已配置为每天北京时间上午10:00自动执行签到。

## 功能说明

- 自动签到获取每日奖励
- 支持多账号批量签到
- 企业微信通知签到结果
- 显示签到进度和奖励信息

## 注意事项

1. 确保Cookie信息正确且有效
2. 企业微信webhook地址可在代码中修改
3. 签到结果会自动发送到企业微信