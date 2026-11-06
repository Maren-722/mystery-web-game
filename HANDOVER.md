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

### （模板，复制这段往下加）

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
