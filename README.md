# 南桥夜市 · 网页解谜游戏

一款基于 Vue 3 的网页解谜游戏。玩家以游客身份浏览"南桥夜市"官网，通过公告、论坛、摊位页面中的线索，拼出糖粥藕摊主陈桂生（陈伯）失踪背后的真相，并最终做出选择。

## 技术栈与库用途

| 库/工具 | 用途 | 在项目中的具体作用 |
|---|---|---|
| Vue 3 | 前端框架 | 所有页面的组件化开发与数据渲染 |
| Vite | 构建工具 | 本地开发服务器、打包构建 |
| Vue Router | 前端路由 | 页面跳转、登录路由守卫（未登录拦截私信/手记页） |

数据存储使用 JSON 文件 + localStorage（模拟登录态），无后端、无数据库。

## 项目结构

```
src/
├── assets/          # 图片、字体
├── styles/          # 全局样式（variables.css 为全站设计变量）
├── router/          # 路由配置
├── components/      # NavBar、Footer 公共组件
├── views/           # 各页面组件
├── data/            # 游戏数据（JSON）
│   ├── accounts.json    # 账号密码对照表
│   ├── stalls.json      # 摊位信息
│   ├── posts.json       # 论坛帖
│   └── messages.json    # 私信与手记
└── App.vue          # 根组件
```

## 运行

```bash
npm install
npm run dev      # 本地开发（默认 http://localhost:5173）
npm test         # 游戏数据、凭据、证据依赖及持久数据校验
npm run build    # 打包构建
```

## 分工

- 人A（架构师）：项目骨架、全局样式、路由、NavBar/Footer、Intro/Home/Login
- 人B：Stalls、StallDetail、Forum、PostDetail + stalls.json、posts.json
- 人C：Messages、Notes、Ending + accounts.json、messages.json

## 本次完善

基于队长仓库提交 `bd6804996714d763ec549af1bdd57f8ff7369142`，本地分支为 `improve/account-story-flow`。保留临岗市、张阿姨凉面、夜归人和原有暖棕色设计，接通六个剧情账号、8组61条私信、27篇个人手记、15个论坛帖和两种结局。

- `src/game/state.js`：统一响应式登录状态、本机论坛存储和调查进度。
- `src/game/rules.js`：纯函数形式的凭据、证据、数据规范化及登录回跳规则。
- `src/data/messages.json`：按参与者共享的会话记录，双方读取同一份内容。
- `src/data/notes.json`：按账号归属的手记、草稿和档案。
- `src/data/clues.json`：九条关键证据的稳定标识。
- `src/data/puzzle-clues.json`：开发用密码与前置线索对照，含剧透。
- `src/data/endings.json`：A/B结局文案。

所有正式数据直接维护在 `src/data`。`tools/import-story.py` 仅用于从之前的独立文案包进行一次性迁移，正常开发和部署无需运行。

## 本地验证与部署

建议使用 Node.js 20 或以上，先运行 `npm ci`，然后执行 `npm test` 和 `npm run build`。通过后 `npm run preview -- --host 127.0.0.1` 可检查构建产物。Vite保留 `/nanqiao-night-market/` 作为资源根路径，路由采用hash模式，适配当前GitHub Pages地址。构建产物需经HTTP服务访问，不支持双击dist/index.html。

当前仓库的GitHub Actions在main分支推送后先测试再构建并部署。队长合并修改并推送main后，Pages才会更新。本地修改本身不会更新线上网站。

这是静态解谜游戏，账号、密码和历史聊天均为虚构剧本数据，真实用户数据不应接入此凭据表。论坛发帖和评论仅保存在当前浏览器，重新开始会清除本次调查和本机论坛记录。旧的123456占位密码已移除；不参与谜题的NPC只保留公开摊位资料。
