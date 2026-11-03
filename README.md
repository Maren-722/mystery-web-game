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
npm run build    # 打包构建
```

## 分工

- 人A（架构师）：项目骨架、全局样式、路由、NavBar/Footer、Intro/Home/Login
- 人B：Stalls、StallDetail、Forum、PostDetail + stalls.json、posts.json
- 人C：Messages、Notes、Ending + accounts.json、messages.json
