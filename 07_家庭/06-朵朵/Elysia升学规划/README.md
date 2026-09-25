# Elysia 升学规划项目

Elysia 升学攻略：香港 / 英国 / 日本三地申请策略、雅思备考规划与微信提醒推送。

## 线上部署（腾讯云 CloudBase）

- **前端静态托管 URL**：https://ai-native-d8gox2tz63118e2f3-1334209523.tcloudbaseapp.com/
- **CloudBase 环境**：`ai-native-d8gox2tz63118e2f3`（ap-shanghai）
- **静态托管 COS Bucket**：`646b-static-ai-native-d8gox2tz63118e2f3-1334209523`

### 部署内容

| 文件 | 说明 |
|------|------|
| `index.html` | 升学攻略主页面（PWA） |
| `data.js` | 全部规划数据（雅思 IELTS_PLAN、行动时间线、三地申请策略） |
| `reminders.js` | 三档重点任务提醒数据（KEY_ALERTS，供云函数拉取） |
| `style.css` | 页面样式 |
| `manifest.json` | PWA 清单 |
| `sw.js` | Service Worker（PWA 离线缓存） |

## 云函数

- **函数名**：`elysia-push`（Node.js 18）
- **触发方式**：定时触发器 `every3days`（每 3 天 09:00）+ 手动 invoke
- **逻辑**：读取数据库 `elysia_push_config` → 拉取线上 `reminders.js` → 调用 PushPlus 推送微信
- **手动调用示例**：
  ```
  invokeFunction(name: "elysia-push")
  ```

## 数据库（NoSQL）

集合 `elysia_push_config`，文档 `_id: 'config'`：

| 字段 | 说明 |
|------|------|
| `elysiaToken` | Elysia 的 PushPlus token（已实名认证） |
| `ansonToken` | Anson 的 PushPlus token |
| `elysiaVerified` | Elysia PushPlus 实名认证状态（true） |
| `updatedAt` | 配置更新时间 |

## 本地源文件

- 网页源文件位于 `outputs/webapp_src/`（index.html、data.js、reminders.js、style.css、manifest.json、sw.js）
- 更新后需重新上传到静态托管（CloudBase → 静态托管托管）
- 上传完成后可用 `https://ai-native-d8gox2tz63118e2f3-1334209523.tcloudbaseapp.com/data.js?verify=<日期>` 验证 CDN 是否刷新

## 验证清单（2026-08-22 已通过）

- [x] 静态托管 6 个文件全部上传成功（HTTP 200）
- [x] 线上 `data.js` 已更新为新版雅思规划（firstExam=5.5，IELTS_PLAN 含 3 个阶段小节点 + 单项提分计划）
- [x] 云函数 `elysia-push` 端到端推送成功（Elysia / Anson 均收到，code 200）
- [x] PushPlus 推送通道在 Elysia 实名认证后恢复可用
