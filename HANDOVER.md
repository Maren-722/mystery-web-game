# 交接说明（HANDOVER）

> 用法：每次做完一批改动，先更新本文件，再和代码一起 commit + push。
> 原则：队友只看这一页，就能接手你的工作，不用来问你。

---

## 项目速览（只需维护一次，改了才更新）

- **游戏是什么**：《南桥夜市》网页解谜游戏——玩家以游客身份浏览夜市官网，从公告、论坛、摊位、私信线索中拼出糖粥藕摊主陈伯失踪的真相
- **启动方式**：`npm install` → `npm run dev` → 浏览器打开 `http://localhost:5173/nanqiao-night-market/`（注意：项目设了 base 路径，不是根路径 5173）
- **技术栈**：Vue 3 + Vite + Vue Router（hash 路由）；无后端，数据全在 `src/data/*.json` + localStorage 模拟登录态
- **目录约定**：
  - `src/views/` —— 各页面（Intro 前情 / Home 首页 / Login·Register 登录注册 / Stalls·StallDetail 摊位 / Forum·PostDetail 论坛 / Messages 私信 / Notes 手记 / Ending 结局）
  - `src/components/` —— NavBar、Footer、BackBar 公共组件
  - `src/data/` —— 游戏数据（accounts 账号 / stalls 摊位 / posts 论坛帖 / messages 私信手记）
  - `src/styles/` —— 全局样式，`variables.css` 是全站设计变量，改配色去这里
  - `src/router/index.js` —— 路由与登录守卫（`requiresAuth` 的页面未登录会被踢到登录页）
- **分支约定**：`main` 只由架构负责人（人A）合并，且 **push 到 main 会自动部署到 GitHub Pages**（`.github/workflows/deploy.yml`），所以干活前先开自己的分支 `feature/名字-功能`；队友还有一个进行中的远程分支 `improve/account-story-flow`
- **分工**（照 README）：人A 架构/样式/路由/Intro·Home·Login；人B Stalls·StallDetail·Forum·PostDetail + stalls·posts 数据；人C Messages·Notes·Ending + accounts·messages 数据

---

## 更新日志（每次改完就往下加一段，最新的放最上面）

### 2026-11-06 · 2x1y3z · 分支 feature/2x1y3z-main-storyline

**本次做了什么**

1. 解谜主线数据层重写：剧情账号 6 个、主线帖 3 篇、私信与手记全量、摊位与评论全量
2. 新增 notices.json 作为首页公告与"通告历史"的统一数据源
3. 张阿姨改为纯 NPC（张姐凉面，不可登录）；全站文案按"生活化、有情感"标准重写

**涉及文件**

- `src/data/accounts.json` —— 重写为 6 个剧情账号（NPC 账号全部移除）
- `src/data/posts.json` —— 旧帖全部删除，替换为 3 篇主线帖（评论支持回复某人）
- `src/data/messages.json` —— 全量重写：6 个账号的私信 + 手记
- `src/data/stalls.json` —— NPC 摊位改名、评论全部重写、摊主私密手记字段清空
- `src/data/notices.json` —— 新增（含刊登中/已过期/已删除三种状态）

**怎么验证**

`npm run dev` 后：论坛应只剩 3 篇新帖；摊位导览各摊是新评论；用主线账号登录可看到新私信与手记（账号与谜底见本地《主线改造方案.md》，该文档刻意不入库）

**已知问题 / 没做完的**

- Home 公告栏尚未接入 notices.json，值日表还是旧的 7 天卡片
- PostDetail/StallDetail 的"回复 @xx"前缀、Notes 的加粗、Messages 的管理员面板、Ending 进度追踪均未实现（下一阶段）
- 结局解锁提示的形态待讨论

**下一步建议**

- Phase 2：Home（公告接入 + 10 月整月日历排班 + 地铁线路图）

---

### 日期 · 你的名字 · 分支 xxx

**本次做了什么**

1.

**涉及文件**

- `路径/文件名` —— 改了什么

**怎么验证**

1.

**已知问题 / 没做完的**

-

**下一步建议**

-
