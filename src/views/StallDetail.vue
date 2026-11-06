<template>
  <div class="stall-detail-page">
    <NavBar />
    <div class="container">
      <BackBar label="返回夜市导览" fallback="/stalls" />
      <!-- TODO(队友B)：根据路由参数 :id 从 src/data/stalls.json 读取对应摊位详情 -->
      <div v-if="stall" class="detail-card">
        <div class="detail-header">
          <span class="stall-no">摊位 {{ stall.stallNo }}</span>
          <h2 class="stall-name">{{ stall.shopName }}</h2>
          <p class="stall-owner">老板：{{ stall.owner }}</p>
        </div>

        <!-- 菜品与价格 -->
        <h3 class="sub-title">菜品</h3>
        <div v-for="item in stall.dishes" :key="item.name" class="dish-row">
          <span>{{ item.name }}</span>
          <span class="dish-price">{{ item.price }}元</span>
        </div>

        <!-- 注意：摊主手记属于私密内容，只有摊主登录后在"我的手记"页可见，
             游客在摊位详情页不显示。手记数据在 src/data/stalls.json 的 notes 字段。 -->

        <!-- 顾客评价 -->
        <h3 class="sub-title">顾客评价</h3>
        <div v-for="(review, i) in stall.reviews" :key="i" class="review-item">
          <p class="review-user">
            {{ review.user }}<template v-if="review.replyTo"> 回复 {{ review.replyTo }}</template> · {{ review.date }}
          </p>
          <p>{{ review.content }}</p>
        </div>
      </div>
      <p v-else>没有找到这个摊位。</p>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import Footer from '../components/Footer.vue'
import BackBar from '../components/BackBar.vue'
import stallsData from '../data/stalls.json'

const route = useRoute()
const stall = ref(null)

// 摊位详情：按 :id 匹配数据
onMounted(() => {
  stall.value = stallsData.find(s => s.id === route.params.id) || null
})
</script>

<style scoped>
.detail-card {
  max-width: 720px;
  margin: 0 auto;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
}
.detail-header {
  border-bottom: 1px solid var(--color-border);
  padding-bottom: var(--space-md);
  margin-bottom: var(--space-md);
}
.stall-no {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
}
.stall-name {
  font-family: var(--font-title);
  font-size: var(--font-h1);
  color: var(--color-primary);
  margin: 4px 0;
}
.stall-owner {
  color: var(--color-text-secondary);
}
.sub-title {
  font-size: var(--font-h3);
  margin: var(--space-md) 0 var(--space-sm);
  padding-bottom: 4px;
  border-bottom: 1px solid var(--color-border);
}
.dish-row {
  display: flex;
  justify-content: space-between;
  padding: 6px 0;
  border-bottom: 1px dashed var(--color-border);
}
.dish-price {
  color: var(--color-accent);
}
.review-item {
  padding: 10px 0;
  border-bottom: 1px dashed var(--color-border);
}
.review-user {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
  margin-bottom: 4px;
}
</style>
