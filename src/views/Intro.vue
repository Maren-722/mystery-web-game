<template>
  <div class="intro-page">
    <div class="intro-card">
      <span class="intro-tag">游戏开始</span>
      <h1 class="intro-title">你是一名刚到临岗市的大一新生</h1>
      <p class="intro-text">
        开学两周，你还没适应这座江边城市的秋天。今天室友们都出去了，你一个人在宿舍刷手机，搜"临岗必吃夜市"。
      </p>
      <p class="intro-text">
        评论区里有人提到<span class="intro-highlight">南桥夜市</span>——一个数字化转型的新型夜市：每个摊位都上了官网，能看菜单、看评价、逛论坛。里面有凉面、馄饨、炒粉、烧烤、麻辣烫、臭豆腐……等许多美味，尤其是那家<span class="intro-highlight">"陈记糖粥藕"</span>，据说是临岗人从小吃到大的老味道，糖藕软糯、粥底浓稠。
      </p>
      <hr class="intro-divider">
      <p class="intro-text">
        在美味的诱惑下，你点开了南桥夜市的官网：
        <a class="intro-link" @click="$router.push('/home')">http://www.nanqiao-night-market.com</a>
      </p>
      <p class="intro-disclaimer">本游戏为虚构创作，其中人物、地点、事件均为虚构，如有雷同，纯属巧合。</p>
    </div>
  </div>
</template>

<script setup>
// 开场页：前情提要
// 玩家点击按钮后进入夜市官网首页
</script>

<style scoped>
.intro-page {
  min-height: 100vh;
  background: #1a1a2e;
  color: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}
.intro-card {
  max-width: 600px;
  width: 100%;
  background: #16213e;
  border-radius: 12px;
  padding: 48px 40px;
  border: 1px solid #0f3460;
}
.intro-tag {
  display: inline-block;
  background: #e94560;
  color: #fff;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  margin-bottom: 24px;
}
.intro-title {
  font-family: var(--font-title);
  font-size: 28px;
  color: #fff;
  margin-bottom: 24px;
  line-height: 1.4;
}
.intro-text {
  font-size: 15px;
  line-height: 1.9;
  color: #b8b8b8;
  margin-bottom: 16px;
}
.intro-highlight {
  color: #e94560;
  font-weight: 600;
}
.intro-divider {
  border: none;
  border-top: 1px solid #0f3460;
  margin: 32px 0;
}
.intro-link {
  color: #e94560;
  font-weight: 600;
  cursor: pointer;
  text-decoration: underline;
  text-underline-offset: 3px;
  transition: color 0.2s;
}
.intro-link:hover {
  color: #fff;
}
.intro-disclaimer {
  margin-top: 24px;
  font-size: 12px;
  color: #666b85;
  text-align: center;
}

@media (max-width: 720px) {
  .intro-card {
    padding: 32px 24px;
  }
  .intro-title {
    font-size: 24px;
  }
}
</style>
