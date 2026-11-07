<template>
  <div class="stalls-page">
    <NavBar />
    <div class="container">
      <h2 class="section-title">夜市导览</h2>
      <p class="page-desc">在这里查看每个摊位的名片：摊位号、老板、主营商品、价格和顾客评价。</p>

      <div class="stall-grid">
        <!-- TODO(队友B)：从 src/data/stalls.json 循环渲染摊位卡片 -->
        <div
          v-for="stall in stalls"
          :key="stall.id"
          class="card stall-card"
          :class="{ 'stall-closed': stall.closed }"
          @click="$router.push('/stalls/' + stall.id)"
        >
          <div class="stall-no">摊位 {{ stall.stallNo }}</div>
          <h3 class="stall-name">{{ stall.shopName }}</h3>
          <p class="stall-owner">老板：{{ stall.owner }} <span v-if="stall.uid" class="stall-uid">ID:{{ stall.uid }}</span></p>
          <p class="stall-main">{{ stall.main }}</p>
          <p class="stall-price">价格：{{ stall.price }}</p>
          <span v-if="stall.closed" class="stall-status">暂停营业</span>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import NavBar from '../components/NavBar.vue'
import Footer from '../components/Footer.vue'
import stallsData from '../data/stalls.json'

// 摊位列表：数据从 src/data/stalls.json 读取（你负责写这个文件）
const stalls = ref([])

onMounted(() => {
  stalls.value = stallsData
})
</script>

<style scoped>
.page-desc {
  color: var(--color-text-secondary);
  margin-bottom: 28px;
  max-width: 620px;
}
.stall-grid {
  display: grid;
  /* 全设备固定两列：左列 A1-A5，右列 B1-B5（列优先填充） */
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(5, auto);
  grid-auto-flow: column;
  gap: 14px;
}
.stall-card {
  cursor: pointer;
  padding: 18px 20px 16px;
  transition: border-color 0.2s, box-shadow 0.2s, transform 0.2s;
  position: relative;
}
.stall-card:hover {
  border-color: var(--color-accent);
  box-shadow: var(--shadow-soft);
  transform: translateY(-1px);
}
.stall-no {
  display: inline-block;
  font-size: 10px;
  letter-spacing: 1.6px;
  color: var(--color-accent);
  border: 1px solid rgba(184, 121, 44, 0.35);
  padding: 1px 7px;
  border-radius: 2px;
  margin-bottom: 10px;
}
.stall-name {
  font-family: var(--font-title);
  font-size: 19px;
  letter-spacing: 1px;
  color: var(--color-text);
  margin-bottom: 6px;
}
.stall-owner,
.stall-main {
  font-size: var(--font-tiny);
  color: var(--color-text-secondary);
  line-height: 1.75;
}
.stall-uid {
  color: var(--color-text-muted);
  margin-left: 4px;
}
.stall-price {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px dashed var(--color-border);
}
.stall-status {
  position: absolute;
  top: 16px;
  right: 16px;
  background: rgba(166, 64, 42, 0.1);
  color: var(--color-danger);
  border: 1px solid rgba(166, 64, 42, 0.3);
  padding: 1px 7px;
  border-radius: 2px;
  font-size: 10px;
  letter-spacing: 1px;
}

/* 暂停营业摊位：整体压暗（保持暖调，不用冷灰） */
.stall-closed {
  background: #F3EEE2;
  border-color: #E2D8C5;
}
.stall-closed .stall-name {
  color: #857E70;
}
.stall-closed .stall-owner,
.stall-closed .stall-main,
.stall-closed .stall-price {
  color: #A39B8B;
}

/* 手机端同样保持两列（A 列 / B 列），卡片内容自动紧凑换行 */
@media (max-width: 720px) {
  .stall-card {
    padding: 14px 14px 12px;
  }
  .stall-name {
    font-size: 16px;
  }
  .stall-main {
    display: none;
  }
}
</style>
