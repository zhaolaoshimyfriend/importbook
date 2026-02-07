# GitHub 认证配置指南

## 方案一：使用 SSH 密钥（推荐，一次配置长期使用）

### 步骤 1：复制你的 SSH 公钥

你的 SSH 公钥内容：
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIK67g+Imdke5BbzXge49XoqrafMQyHlF6ZAFbH67/fcQ zhaolaoshimyfriend@github.com
```

### 步骤 2：添加到 GitHub

1. 访问：https://github.com/settings/keys
2. 点击 "New SSH key"
3. Title: `MacBook - 导账项目`
4. Key: 粘贴上面的公钥（整行）
5. 点击 "Add SSH key"

### 步骤 3：测试并推送

```bash
# 测试连接
ssh -T git@github.com

# 如果成功，推送代码
git push -u origin main
```

---

## 方案二：使用 Personal Access Token（快速方案）

### 步骤 1：生成 Token

1. 访问：https://github.com/settings/tokens/new
2. Note（备注）：`导账项目推送`
3. Expiration（过期时间）：选择合适的时间（如 90 天）
4. 勾选权限：**repo**（全部勾选）
5. 点击 "Generate token"
6. **重要**：立即复制 token（只显示一次）

### 步骤 2：配置 Git 使用 Token

```bash
# 使用 token 作为密码
git push -u origin main
# 用户名：zhaolaoshimyfriend
# 密码：粘贴刚才复制的 token
```

### 步骤 3：保存凭证（可选，避免每次输入）

```bash
# macOS 使用 Keychain 保存
git config --global credential.helper osxkeychain

# 然后再次推送，输入一次后会自动保存
git push -u origin main
```

---

## 当前状态

- ✅ SSH 密钥已生成：`~/.ssh/id_ed25519_github`
- ✅ SSH 配置已完成
- ✅ Git 远程仓库已配置：`git@github.com:zhaolaoshimyfriend/importbook.git`
- ⏳ 等待：将 SSH 公钥添加到 GitHub 或使用 Token 推送

## 推荐

建议使用**方案一（SSH）**，配置一次后可以长期使用，无需每次输入密码。
