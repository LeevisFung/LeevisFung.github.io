# dw/ · 知识蒸馏工作台的线上配套文件

这个目录只放两样东西，供**已售出的工作台**在启动时读取。
不要删、不要改文件名。

| 文件 | 地址 | 作用 |
|---|---|---|
| `revoked.json` | https://leevisfung.github.io/dw/revoked.json | **撤销授权** |
| `version.json` | https://leevisfung.github.io/dw/version.json | **版本检查 / 更新提示** |

---

## 一、撤销某个买家的授权（退款 / 违规转卖）

1. 打开 `revoked.json`
2. 把他的**授权码 id** 加进 `revoked` 数组：

```json
{
  "revoked": ["a1b2c3d4", "e5f6g7h8"]
}
```

3. 保存 → 提交 → 推送。**约 1 分钟后生效。**

效果：该买家**下次联网打开工作台时会被拒绝**，并提示"授权已失效，请联系卖家"。

> **只放随机 id，不要放买家姓名或昵称**——这个文件是公开的。

---

## 二、发新版

1. 打开 `version.json`
2. 改这几行：

```json
{
  "latest": "6.1.0",           ← 新版本号
  "minSupported": "6.0.0",     ← 低于这个版本强制提示升级
  "title": "本次改了什么",       ← 一句话
  "changes": ["修复了 XX", "新增了 YY"]   ← 变更清单，会显示给用户
}
```

3. 保存 → 提交 → 推送

效果：老用户下次打开会看到"有新版本 v6.1.0"，并显示变更清单和获取方式。

> **新版文件不要传到这个公开仓库** —— 传了就没了付费墙。
> 新版仍然通过闲鱼私发给正版买家。**盗版拿不到更新，这正是"持续更新"作为护城河的作用。**

---

## 三、怎么改（不用 git 命令也行）

在 GitHub 网页上直接打开文件 → 点铅笔图标 → 改 → Commit changes。
**改完等 1 分钟**再让对方重开工作台。

---

## ⚠️ 安全提醒

- 这个仓库是**公开**的，任何人都能看到这两个文件——**这是设计如此，没问题**（里面没有买家信息）
- **但 GitHub Token 绝不能写进 git remote URL**。如果你之前这么干过，去
  Settings → Developer settings → Personal access tokens **吊销重发**，然后：
  ```bash
  git remote set-url origin https://github.com/LeevisFung/LeevisFung.github.io.git
  ```
