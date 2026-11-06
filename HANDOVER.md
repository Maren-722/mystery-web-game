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

### 2026-11-06（二）· 2x1y3z · 分支 feature/2x1y3z-main-storyline

**本次做了什么**

1. **结局解锁机制落地**：导航栏常驻一盏暗灯笼🏮，10 个关键线索节点集齐后点亮，并弹一次全屏提示（去往结局 / 继续探索）；没集齐点灯无反应，直接访问 /ending 会被"灯还没亮"挡板拦住。进度存 localStorage（nq_progress）
2. **Home 重写**：公告栏接入 notices.json（只显示"刊登中"，置顶优先）；排班表改为 2026 年 10 月整月日历（每天 2 人值班；陈伯每周二/周日值班，住院那一周 10.6、10.11 与失踪后 10.27 的班被划掉并由他摊顶替，10.30 标"今天"）；地铁公告里可展开 SVG 线路示意图（3 号线 + 1 号线换乘，南桥→城南方向第五站梧桐苑）
3. **Messages 重写**：会话改为折叠卡片（点开才见内容），空会话显示"记录已清空"（陈伯账号的既视感）
4. **Manager 新增**：王主任登录后导航栏出现"管理处"，工作台含通告历史（全部/刊登中/已过期/已删除筛选，点开看全文，已删除的标题划线）；登录管理员账号后自动跳转工作台
5. **细节**：陈伯手记 5 篇精简为 3 篇；帖子与摊位评论支持"回复 @xx"显示；手记正文 **xx** 渲染为加粗（陈伯日记里的"念"字）

**涉及文件**

- `src/utils/progress.js` —— 新增：10 节点进度追踪（节点清单见文件头注释，含判定粒度原则）
- `src/views/Home.vue` —— 重写（公告 + 日历排班 + 地铁图）
- `src/views/Messages.vue` —— 重写（折叠会话）
- `src/views/Manager.vue` —— 新增（管理员工作台）
- `src/views/Ending.vue` —— 重写（挡板 + 新结局文案"第五站，梧桐苑"）
- `src/views/Notes.vue` / `PostDetail.vue` / `StallDetail.vue` —— 小改（进度判定、回复显示、加粗渲染）
- `src/components/NavBar.vue` —— 灯笼 + 解锁提示 + 管理员入口，登录态增加 role 字段
- `src/views/Login.vue` —— 登录态写入 role，管理员登录直跳工作台
- `src/router/index.js` —— 新增 /manager 路由（requiresManager 守卫）
- `src/data/messages.json` —— 陈伯手记 5→3 篇

**怎么验证**

`npm run dev` 后：首页看到日历排班与可展开的地铁图；登录王主任（见本地《主线改造方案.md》）出现"管理处"；按方案里的线索链走完 10 个节点后灯笼点亮、弹提示、可进结局

**已知问题 / 没做完的**

- 结局为单一版本占位，分支结局/彩蛋后续再商讨
- 谜底文档《主线改造方案.md》刻意不入库（防止玩家在仓库里翻到答案）

**下一步建议**

- 人物塑造与合理化细节补充（陈伯走后摊主们的关心互动等，剧本作者持续补充）
- 移动端实测一遍日历与线路图

---

### 2026-11-07 · 2x1y3z · 分支 feature/2x1y3z-main-storyline

**本次做了什么**

1. **ID 登录体系**：登录改为按 ID 匹配——商户 ID=人名（导览可见），游客 ID=长数字（论坛发言旁显示）。账号数据结构见 `src/data/accounts.json` 的 `uid` 字段
2. **私信/手记按剧作家 11-07 反馈重写**：刘姐×陈伯改隐晦版；删三组会话（老张-小李/刘姐-王主任/小李-儿子）；陈伯失踪后小李/刘姐/老张的追问全部无回复；王主任手记改为事务口吻两篇；儿子手记重写（身世更苦、主动寻亲）；陈伯手记第三篇移到 10.25（交王主任、不声不响离开）
3. **短信页仿微信改版**：电脑=左侧会话列表+右侧聊天窗；手机=列表↔聊天切换。按最新消息倒序、可发消息（本机保存）、绿色气泡
4. **功能修复**：帖子评论即时显示（不用退出重进）；评论/帖子/评价/消息长文换行；切换账号后短信/手记/评论框无需刷新即时更新；论坛评论按时间倒序；手记按时间倒序
5. **摊位详情页新增顾客评价发布功能**（本机保存）
6. 文案：地铁公告去掉"示意图见下方"；帖子1去掉落款、感谢织进正文；帖子2评论顺序调整（儿子的评论倒序第二）

**涉及文件**

- `src/data/accounts.json / posts.json / messages.json / notices.json` —— 数据更新
- `src/utils/auth.js` —— 新增：登录态响应式共享 + 按 ID 查账号
- `src/views/Messages.vue` —— 重写（仿微信）
- `src/views/PostDetail.vue / Forum.vue / Notes.vue / StallDetail.vue / Login.vue` —— 功能与修复
- `src/components/NavBar.vue` —— 切换账号改 ID 登录

**怎么验证**

`npm run dev` 后：登录页用 ID 登录（商户填人名，儿子账号 ID 在帖子2他的评论旁）；短信页为微信式双栏、可发消息；发帖评论后立即出现；切换账号后短信手记立即变化

**已知问题 / 没做完的**

- 结局为单一版本占位，分支结局后续再商讨
- 地铁线路图待美化

---

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
