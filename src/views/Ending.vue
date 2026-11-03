<template>
  <div class="ending-page">
    <div class="ending-card">
      <span class="ending-tag">结 局</span>
      <h1 class="ending-title">{{ ending.title }}</h1>
      <p class="ending-text">{{ ending.content }}</p>
      <hr class="ending-divider">
      <button class="ending-btn" @click="$router.push('/')">重新开始</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

// TODO(队友C)：结局文案写在 src/data/endings.json（或直接写在这里）
// A结局：告诉夜归人真相 → 父子最后三个月在一起
// B结局：继续保密 → 陈伯一个人离开
const endings = {
  A: {
    title: '他等到了',
    content: '第二年春天，陈记糖粥藕的摊位又支起来了。摊主是个年轻人，右手食指关节微微变形。'
  },
  B: {
    title: '有些人，你以为还能再见',
    content: '等你终于敢开口的时候，摊位已经锁了。'
  }
}

const ending = ref(endings.A)

onMounted(() => {
  const choice = localStorage.getItem('nq_ending')
  ending.value = endings[choice] || endings.A
})
</script>

<style scoped>
.ending-page {
  min-height: 100vh;
  background: #1a1a2e;
  color: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}
.ending-card {
  max-width: 560px;
  width: 100%;
  background: #16213e;
  border-radius: 12px;
  padding: 48px 40px;
  border: 1px solid #0f3460;
}
.ending-tag {
  display: inline-block;
  background: #e94560;
  color: #fff;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  margin-bottom: 24px;
}
.ending-title {
  font-family: var(--font-title);
  font-size: 28px;
  color: #fff;
  margin-bottom: 20px;
  line-height: 1.4;
}
.ending-text {
  font-size: 15px;
  line-height: 2;
  color: #b8b8b8;
}
.ending-divider {
  border: none;
  border-top: 1px solid #0f3460;
  margin: 32px 0;
}
.ending-btn {
  display: block;
  width: 100%;
  padding: 14px;
  background: transparent;
  color: #e94560;
  border: 1px solid #e94560;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  font-family: var(--font-body);
  transition: background 0.2s;
}
.ending-btn:hover {
  background: rgba(233, 69, 96, 0.15);
}
</style>
