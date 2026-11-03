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
          @click="$router.push('/stalls/' + stall.id)"
        >
          <div class="stall-no">摊位 {{ stall.stallNo }}</div>
          <h3 class="stall-name">{{ stall.shopName }}</h3>
          <p class="stall-owner">老板：{{ stall.owner }}</p>
          <p class="stall-main">{{ stall.main }}</p>
          <p class="stall-price">价格：{{ stall.price }}</p>
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
  margin-bottom: var(--space-lg);
}
.stall-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-md);
}
.stall-card {
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.stall-card:hover {
  border-color: var(--color-accent);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.stall-no {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
  margin-bottom: var(--space-xs);
}
.stall-name {
  font-family: var(--font-title);
  font-size: var(--font-h3);
  color: var(--color-primary);
  margin-bottom: 4px;
}
.stall-owner,
.stall-main {
  font-size: var(--font-small);
  color: var(--color-text-secondary);
}
.stall-price {
  font-size: var(--font-small);
  color: var(--color-accent);
  margin-top: var(--space-xs);
}

@media (max-width: 1440px) {
  .stall-grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
@media (max-width: 720px) {
  .stall-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 480px) {
  .stall-grid {
    grid-template-columns: 1fr;
  }
}
</style>
