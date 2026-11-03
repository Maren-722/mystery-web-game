<template>
  <div class="intro-page">
    <div class="intro-card">
      <span class="intro-tag">游戏开始</span>
      <h1 class="intro-title">你是一名刚到临岗市的大一新生</h1>
      <p class="intro-text">
        开学两周，你还没适应这座江边城市的秋天。今晚室友出去约会了，你一个人在宿舍刷手机，搜"临岗必吃夜市"。
      </p>
      <p class="intro-text">
        评论区里有人提到<span class="intro-highlight">南桥夜市</span>——江边摆了18年的老夜市，其中有一家<span class="intro-highlight">"陈记糖粥藕"</span>，据说是很多临岗人从小吃到大的味道。
      </p>
      <p class="intro-text">
        你点进了南桥夜市的官网，想看看陈记今晚出不出摊。
      </p>
      <hr class="intro-divider">
      <button class="intro-btn" @click="$router.push('/home')">进入南桥夜市官网 →</button>
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
.intro-btn {
  display: block;
  width: 100%;
  padding: 16px;
  background: #e94560;
  color: #fff;
  text-align: center;
  border-radius: 8px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  font-family: var(--font-body);
  transition: background 0.2s;
}
.intro-btn:hover {
  background: #c73650;
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
