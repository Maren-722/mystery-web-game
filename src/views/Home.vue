<template>
  <div class="home-page">
    <NavBar />
    <div class="container">

      <!-- 公告栏 -->
      <div class="notice-bar">
        <span class="notice-tag">公告</span>
        <span class="notice-text">{{ notice }}</span>
      </div>

      <!-- 排班表（固屏） -->
      <h2 class="section-title">本周排班表</h2>
      <div class="schedule-grid">
        <div
          v-for="day in schedule"
          :key="day.name"
          class="schedule-day"
          :class="{ today: day.today }"
        >
          <div class="schedule-day-name">{{ day.name }}</div>
          <div class="schedule-day-shops">
            <template v-for="shop in day.shops" :key="shop.name">
              <span
                v-if="shop.closed"
                class="schedule-shop-closed"
              >{{ shop.name }}</span>
              <span v-else>{{ shop.name }}</span>
              <br>
            </template>
          </div>
        </div>
      </div>

      <!-- 登录后：排班表下方多出两个入口 -->
      <template v-if="currentUser">
        <h2 class="section-title">我的空间</h2>
        <div class="dashboard-grid">
          <div class="card dashboard-card" @click="$router.push('/notes')">
            <h3>我的手记</h3>
            <p class="card-desc">查看你发过的私密手记</p>
          </div>
          <div class="card dashboard-card" @click="$router.push('/messages')">
            <h3>短信</h3>
            <p class="card-desc">查看你和其他人的聊天记录</p>
          </div>
        </div>
      </template>

    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import NavBar from '../components/NavBar.vue'
import Footer from '../components/Footer.vue'

// 公告内容（队友可调整措辞，核心信息：陈记暂停营业）
const notice = ref('陈记糖粥藕自10月12日起暂停营业，恢复时间另行通知。——南桥夜市管理处')

// 排班表数据（暂定，可移到 data/stalls.json）
const schedule = ref([
  { name: '周一', shops: [{ name: '卤味老张' }, { name: '凉面张阿姨' }, { name: '炒粉小李' }] },
  { name: '周二', shops: [{ name: '卤味老张' }, { name: '凉面张阿姨' }, { name: '炒粉小李' }] },
  { name: '周三', today: true, shops: [{ name: '陈记糖粥藕', closed: true }, { name: '卤味老张' }, { name: '凉面张阿姨' }] },
  { name: '周四', shops: [{ name: '卤味老张' }, { name: '凉面张阿姨' }, { name: '炒粉小李' }] },
  { name: '周五', shops: [{ name: '卤味老张' }, { name: '凉面张阿姨' }, { name: '炒粉小李' }] },
  { name: '周六', shops: [{ name: '卤味老张' }, { name: '凉面张阿姨' }, { name: '炒粉小李' }] },
  { name: '周日', shops: [{ name: '卤味老张' }, { name: '凉面张阿姨' }, { name: '炒粉小李' }] }
])

const currentUser = computed(() => {
  try {
    return JSON.parse(localStorage.getItem('nq_user') || 'null')
  } catch {
    return null
  }
})
</script>

<style scoped>
.notice-bar {
  background: #FFFBEB;
  border: 1px solid var(--color-accent-light);
  border-radius: var(--radius);
  padding: 12px 16px;
  margin-bottom: var(--space-lg);
  display: flex;
  align-items: center;
  gap: 12px;
}
.notice-tag {
  background: var(--color-accent);
  color: #fff;
  padding: 2px 10px;
  border-radius: 4px;
  font-size: var(--font-tiny);
  flex-shrink: 0;
}
.notice-text {
  font-size: var(--font-body-size);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.schedule-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
  margin-bottom: var(--space-lg);
}
.schedule-day {
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 12px;
  text-align: center;
}
.schedule-day.today {
  border-color: var(--color-accent);
  background: #FFFBEB;
}
.schedule-day-name {
  font-size: var(--font-small);
  color: var(--color-text-secondary);
  margin-bottom: 8px;
}
.schedule-day-shops {
  font-size: var(--font-tiny);
  line-height: 1.8;
}
.schedule-shop-closed {
  color: var(--color-danger);
  text-decoration: line-through;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-md);
}
.dashboard-card {
  cursor: pointer;
  transition: border-color 0.2s, box-shadow 0.2s;
}
.dashboard-card:hover {
  border-color: var(--color-accent);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.dashboard-card h3 {
  font-size: var(--font-h3);
  color: var(--color-primary);
  margin-bottom: 8px;
}
.card-desc {
  font-size: var(--font-small);
  color: var(--color-text-secondary);
}

@media (max-width: 720px) {
  .schedule-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}
</style>
