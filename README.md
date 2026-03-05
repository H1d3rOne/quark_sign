# Quark Sign - GitHub Actions Setup Guide

## GitHub Actions 自动签到配置

本项目已配置GitHub Actions自动执行夸克网盘签到及企业微信通知。

## 配置步骤

### 1. 添加Repository Secret
1. 进入GitHub仓库页面：https://github.com/H1d3rOne/quark_sign/settings/secrets/actions
2. 点击 "New repository secret" 按钮
3. 添加以下Secret：
   - Name: `COOKIE_QUARK`
   - Value: 你的夸克网盘Cookie信息（支持多个账号，用换行符或&&分隔）
   - Name: `WEBHOOK_URL`
   - Value: 你的企业微信Webhook地址（在quark_sign.py中的send_to_wxwork函数中配置）

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

## 企业微信消息通知配置

### 步骤1：创建企业微信群
1. 登录企业微信管理后台：https://work.weixin.qq.com/
2. 进入"应用管理" → "自建" → "创建应用"
3. 填写应用名称（如"夸克签到通知"）
4. 上传应用图标
5. 点击"创建"按钮

### 步骤2：获取Webhook地址
1. 在应用详情页面，找到"机器人"部分
2. 点击"添加机器人"
3. 填写机器人名称（如"夸克签到机器人"）
4. 点击"创建"
5. 复制生成的Webhook地址

### 步骤3：修改代码中的Webhook地址
1. 在quark_sign.py文件中，找到send_to_wxwork函数
2. 将webhook变量的值修改为你刚才复制的Webhook地址

### 步骤4：测试通知
1. 手动触发一次workflow
2. 检查企业微信群是否收到签到通知

## 注意事项

1. 确保Cookie信息正确且有效
2. 企业微信webhook地址可在代码中修改
3. 签到结果会自动发送到企业微信
4. 确保企业微信应用已正确配置并启用