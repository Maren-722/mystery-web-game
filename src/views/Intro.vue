<template>
  <div class="intro-page">
    <div class="intro-card">
      <span class="intro-tag">前情</span>
      <h1 class="intro-title">你是一名刚到临岗市的大一新生</h1>
      <p class="intro-text">
        开学两周，你还没适应这座江边城市的秋天。今天室友们都出去了，你一个人在宿舍刷手机，搜“临岗必吃夜市”。
      </p>
      <p class="intro-text">
        评论区里有人提到<span class="intro-highlight">南桥夜市</span>——一条上了官网的老夜市：摊位、菜单、评价、论坛，全都能在网上看。底下一水儿地夸一家叫<span class="intro-highlight">“陈记糖粥藕”</span>的摊子，说那是临岗人从小吃到大的味道。
      </p>
      <p class="intro-text">
        你按着地址找过去。A1 的卷帘门锁着，门缝里能看见灶台——擦得锃亮，像刚收拾过。隔壁摊主说，陈伯好几天没来了，也没人知道为什么。
      </p>
      <p class="intro-text">
        回宿舍的路上，你刷到夜市论坛最新的一条帖子：<span class="intro-quote">“陈伯是不是不出摊了？以后还喝得到糖粥藕吗呜呜呜”</span>
        底下十几条回复，没有一个人答得上来。
      </p>
      <p class="intro-text">
        一个在一条街上卖了二十年糖粥藕的老人，不会无缘无故地消失。
        <br>你也不知道自己为什么，把那条帖子来来回回看了三遍。
      </p>
      <hr class="intro-divider">
      <p class="intro-text intro-go">
        你点开了南桥夜市的官网：
        <a class="intro-link" @click="$router.push('/home')">www.nanqiao-night-market.com</a>
      </p>
      <p class="intro-disclaimer">本游戏为虚构创作，其中人物、地点、事件均为虚构，如有雷同，纯属巧合。</p>
    </div>
  </div>
</template>

<script setup>
// 开场页：前情提要
// 玩家点击链接后进入夜市官网首页
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
.intro-quote {
  color: #d8cfc2;
  font-style: italic;
}
.intro-go {
  color: #d8cfc2;
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
