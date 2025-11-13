# LangBot 配置向导

## 📋 需要收集的信息

在继续部署之前，请准备以下信息：

### 1️⃣ Dify API Key
**获取方式**:
1. 访问 https://qmsai.transsion.com
2. 登录到Dify管理后台
3. 进入 "设置" → "API密钥"
4. 复制API Key

**示例**: `sk-xxx-xxx-xxx`

---

### 2️⃣ 飞书机器人配置

#### 创建飞书机器人应用
1. 访问 https://open.feishu.cn/
2. 登录飞书开发者后台
3. 创建新应用 → 选择 "机器人"
4. 填写应用信息

#### 获取应用凭证
1. 在应用详情页面找到 "凭证与基础信息"
2. 复制以下信息:
   - **App ID**: 应用ID
   - **App Secret**: 应用Secret

**示例**:
```
App ID: cli_a1b2c3d4e5f6g7h8
App Secret: xxx-xxx-xxx-xxx
```

#### 配置事件订阅
1. 在应用设置中找到 "事件订阅"
2. 配置Webhook URL: `http://47.108.152.16/webhook/feishu`
3. 配置事件类型:
   - 消息事件
   - 应用事件

---

### 3️⃣ Webhook Token (自定义)

这是一个自定义的安全令牌，用于验证来自飞书的消息。

**建议**: 使用强密码，例如:
```
langbot_webhook_token_2025_secure_key_12345
```

---

## 🔧 配置步骤

### 步骤1: 编辑.env文件

```bash
ssh root@47.108.152.16
nano /opt/langbot/.env
```

### 步骤2: 填入以下信息

```bash
# Dify配置
DIFY_API_KEY=<从Dify获取的API Key>
DIFY_API_URL=https://qmsai.transsion.com

# 飞书配置
FEISHU_APP_ID=<飞书应用ID>
FEISHU_APP_SECRET=<飞书应用Secret>
WEBHOOK_TOKEN=<自定义的Webhook Token>

# LangBot配置
LANGBOT_PORT=8080
LANGBOT_HOST=0.0.0.0
LANGBOT_DEBUG=false
LOG_LEVEL=INFO
```

### 步骤3: 保存文件

按 `Ctrl + X` → `Y` → `Enter` 保存

### 步骤4: 验证配置

```bash
cat /opt/langbot/.env
```

---

## ✅ 配置检查清单

- [ ] Dify API Key 已获取
- [ ] 飞书应用已创建
- [ ] 飞书应用ID已获取
- [ ] 飞书应用Secret已获取
- [ ] Webhook Token已准备
- [ ] .env文件已编辑
- [ ] 配置已验证

---

## 📞 需要帮助？

如果遇到问题，请检查:

1. **Dify连接问题**
   ```bash
   curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://qmsai.transsion.com/api/apps
   ```

2. **飞书连接问题**
   ```bash
   curl -X POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal \
     -H "Content-Type: application/json" \
     -d '{"app_id":"YOUR_APP_ID","app_secret":"YOUR_APP_SECRET"}'
   ```

3. **查看日志**
   ```bash
   tail -f /var/log/langbot/langbot.log
   ```

---

**准备好信息后，继续执行部署！** 🚀

