<template>
  <div class="home-page">
    <NavBar />
    <div class="container">

      <!-- 公告栏 -->
      <h2 class="section-title">公告栏</h2>
      <p class="page-desc">网站资料截至 2026 年 10 月 28 日</p>
      <div class="notice-bar">
        <div
          v-for="(n, i) in notices"
          :key="i"
          class="notice-item"
          role="button"
          tabindex="0"
          :class="{ important: n.important }"
          @click="openNotice(n)"
          @keydown.enter="openNotice(n)"
          @keydown.space.prevent="openNotice(n)"
        >
          <span class="notice-tag" :style="{ background: tagColors[n.tag] }">{{ n.tag }}</span>
          <div class="notice-body">
            <p class="notice-text">{{ n.text }}</p>
            <p class="notice-meta">{{ n.meta }}</p>
          </div>
        </div>
      </div>

      <!-- 公告详情弹窗 -->
      <div v-if="showModal" class="modal-mask" @click.self="closeNotice">
        <div
          class="modal-card"
          role="dialog"
          aria-modal="true"
          aria-labelledby="notice-title"
          @keydown="handleModalKeys"
          @touchstart="onTouchStart"
          @touchend="onTouchEnd"
        >
          <div class="modal-header">
            <span class="notice-tag" :style="{ background: tagColors[activeNotice.tag] }">{{ activeNotice.tag }}</span>
            <h3 id="notice-title" class="modal-title">{{ activeNotice.text }}</h3>
            <button ref="closeButton" class="modal-close" aria-label="关闭公告" @click="closeNotice">×</button>
          </div>
          <p class="modal-meta">{{ activeNotice.meta }}</p>
          <div class="modal-content">{{ activeNotice.fullText }}</div>
          <div class="modal-nav">
            <button class="modal-arrow" aria-label="上一条公告" @click="prevNotice">‹</button>
            <span class="modal-count">{{ activeIndex + 1 }} / {{ notices.length }}</span>
            <button class="modal-arrow" aria-label="下一条公告" @click="nextNotice">›</button>
          </div>
        </div>
      </div>

      <!-- 值日表（固屏） -->
      <h2 class="section-title">夜市值日表</h2>
      <p class="table-desc">10月26日至11月1日，每天三家店铺轮流打扫。陈记暂停营业期间由邻摊代班。</p>
      <div class="schedule-grid">
        <div
          v-for="day in schedule"
          :key="day.name"
          class="schedule-day"
          :class="{ today: day.today }"
        >
          <div class="schedule-day-name">{{ day.name }}</div>
          <div class="schedule-day-date">{{ day.date }}</div>
          <div class="schedule-day-shops">
            <template v-for="shop in day.shops" :key="shop.name">
              <span
                v-if="shop.closed"
                class="schedule-shop-closed"
              >{{ shop.name }}</span>
              <span v-else>{{ shop.name }}</span>
              <span v-if="shop.replacedBy" class="schedule-replaced">（由{{ shop.replacedBy }}顶替）</span>
              <br>
            </template>
          </div>
        </div>
      </div>

    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, nextTick } from 'vue'
import NavBar from '../components/NavBar.vue'
import Footer from '../components/Footer.vue'

// 公告标签配色：通知/开业/上新/活动
const tagColors = {
  '通知': 'var(--color-danger)',
  '开业': 'var(--color-success)',
  '上新': 'var(--color-accent)',
  '活动': 'var(--color-primary)'
}

// 当前打开的公告（弹窗）：支持左右切换邻近公告
const showModal = ref(false)
const activeIndex = ref(0)
const activeNotice = computed(() => notices.value[activeIndex.value])
const closeButton = ref(null)
let noticeTrigger = null
function openNotice(n) {
  noticeTrigger = document.activeElement
  activeIndex.value = notices.value.findIndex(item => item === n)
  showModal.value = true
  nextTick(() => closeButton.value?.focus())
}
function closeNotice() {
  showModal.value = false
  noticeTrigger?.focus()
}
function handleModalKeys(event) {
  if (event.key === 'Escape') { closeNotice(); return }
  if (event.key !== 'Tab') return
  const buttons = [...event.currentTarget.querySelectorAll('button')]
  const first = buttons[0], last = buttons.at(-1)
  if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus() }
  else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus() }
}
function prevNotice() {
  activeIndex.value = (activeIndex.value - 1 + notices.value.length) % notices.value.length
}
function nextNotice() {
  activeIndex.value = (activeIndex.value + 1) % notices.value.length
}
// 移动端左右滑动切换
let touchStartX = 0
function onTouchStart(e) {
  touchStartX = e.touches[0].clientX
}
function onTouchEnd(e) {
  const dx = e.changedTouches[0].clientX - touchStartX
  if (dx > 50) prevNotice()
  else if (dx < -50) nextNotice()
}

// 公告列表：第一条为核心公告（暂停营业），其余营造夜市氛围
const notices = ref([
  {
    tag: '通知',
    important: true,
    text: '陈记糖粥藕暂停营业，恢复时间另行通知。',
    meta: '发布：南桥夜市管理处 · 王志强 ｜ 10月13日',
    fullText: '陈记糖粥藕（A1号摊位）因个人原因暂停营业，恢复时间另行通知。\n\n管理处已与陈师傅取得联系。请勿传播未经证实的说法，具体营业安排以本栏后续公告为准。\n\n—— 南桥夜市管理处 王志强\n2026年10月13日'
  },
  {
    tag: '开业',
    text: '王记烧烤全新开业，全场8折！',
    meta: '开业时间：10月14日',
    fullText: '王记烧烤（B3号摊位）于10月14日正式开业！\n\n主营：烤羊肉串、烤生蚝、烤茄子、烤韭菜。\n开业期间（10月14日-10月20日）全场8折，欢迎各位街坊捧场！'
  },
  {
    tag: '上新',
    text: '刘姐麻辣烫推出新品「秘制香辣藕片」，买一送一。',
    meta: '活动时间：10月15日-10月17日',
    fullText: '刘姐麻辣烫（B4号摊位）新品「秘制香辣藕片」10月15日上市！\n\n精选洪湖莲藕，香辣入味，脆嫩爽口，前三天买一送一，数量有限，售完即止。\n\n（藕是托老伙计进的货，那批藕品质不错，大家尝尝就知道。）'
  },
  {
    tag: '活动',
    text: '张阿姨凉面新品酸梅汤上市，第二杯半价。',
    meta: '活动时间：10月13日起',
    fullText: '张阿姨凉面（A2号摊位）自酿酸梅汤10月13日起上市！\n\n乌梅、山楂、陈皮慢火熬制，解腻消暑，配凉面一绝。活动期间第二杯半价。'
  },
  {
    tag: '活动',
    text: '小李炒粉开业一周年，全场满20减5。',
    meta: '活动时间：10月10日-10月20日',
    fullText: '小李炒粉（B2号摊位）开业一周年啦！\n\n10月10日-10月20日，全场满20减5，感谢各位街坊一年来的照顾。招牌炒粉加个蛋，老客都知道！'
  },
  {
    tag: '通知',
    text: '管理处值班资料与旧账号迁移说明',
    meta: '管理处公开资料 · 10月20日',
    fullText: '管理处负责人：王志强。账号ID：wangzhiqiang。到岗日期：2018年9月1日。\n\n旧系统迁移说明：管理处账号沿用负责人到岗日期，按YYYYMMDD八位年月日输入。商户账号按各摊主原先登记的日期保留。\n\n江边老摊区于2008年集中挂牌为南桥夜市，早年纸档随摊位迁入本系统。历史排班与公告不代表今天的营业状态。'
  }
])

// 故事固定在2026年10月28日，本周10月26日至11月1日
// 陈叔暂停营业后，原值日由其他店铺顶替
const schedule = ref([
  {
    name: '周一', date: '10月26日',
    shops: [{ name: '张记卤味' }, { name: '张阿姨凉面' }, { name: '小李炒粉' }]
  },
  {
    name: '周二', date: '10月27日',
    shops: [
      { name: '陈记糖粥藕', closed: true, replacedBy: '张阿姨凉面' },
      { name: '赵记馄饨' },
      { name: '王记烧烤' }
    ]
  },
  {
    name: '周三', date: '10月28日', today: true,
    shops: [{ name: '陈记糖粥藕', closed: true, replacedBy: '张阿姨凉面' }, { name: '珍姐水果捞' }, { name: '刘姐麻辣烫' }]
  },
  {
    name: '周四', date: '10月29日',
    shops: [
      { name: '陈记糖粥藕', closed: true, replacedBy: '王记烧烤' },
      { name: '小李炒粉' },
      { name: '阿强臭豆腐' }
    ]
  },
  {
    name: '周五', date: '10月30日',
    shops: [{ name: '张记卤味' }, { name: '赵记馄饨' }, { name: '珍姐水果捞' }]
  },
  {
    name: '周六', date: '10月31日',
    shops: [{ name: '阿伟烤冷面' }, { name: '张阿姨凉面' }, { name: '刘姐麻辣烫' }]
  },
  {
    name: '周日', date: '11月1日',
    shops: [{ name: '阿强臭豆腐' }, { name: '王记烧烤' }, { name: '小李炒粉' }]
  }
])

</script>

<style scoped>
.notice-bar {
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 4px 16px;
  margin-bottom: var(--space-lg);
}
.notice-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px dashed var(--color-border);
  cursor: pointer;
  transition: background 0.15s;
}
.notice-item:hover {
  background: #FFFDF8;
}
.notice-item:last-child {
  border-bottom: none;
}
.notice-item.important {
  background: #FFFBEB;
  margin: 0 -16px;
  padding: 12px 16px;
  border-bottom: 1px solid var(--color-accent-light);
  border-radius: var(--radius) var(--radius) 0 0;
}
.notice-item.important:hover {
  background: #FFF6DC;
}
.notice-tag {
  background: var(--color-primary);
  color: #fff;
  padding: 2px 10px;
  border-radius: 4px;
  font-size: var(--font-tiny);
  flex-shrink: 0;
  margin-top: 2px;
}

/* 公告详情弹窗 */
.modal-mask {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 20px;
}
.modal-card {
  max-height: calc(100dvh - 40px);
  overflow: auto;
  max-width: 520px;
  width: 100%;
  background: var(--color-card);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.25);
}
.modal-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: var(--space-sm);
}
.modal-title {
  flex: 1;
  font-family: var(--font-title);
  font-size: var(--font-h3);
  color: var(--color-primary);
  line-height: 1.4;
}
.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  line-height: 1;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 0 4px;
}
.modal-close:hover {
  color: var(--color-text);
}
.modal-meta {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
  padding-bottom: var(--space-sm);
  border-bottom: 1px solid var(--color-border);
  margin-bottom: var(--space-md);
}
.modal-content {
  font-size: var(--font-body-size);
  line-height: 1.9;
  white-space: pre-line;
  color: var(--color-text);
}
.modal-nav {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: var(--space-md);
  padding-top: var(--space-sm);
  border-top: 1px solid var(--color-border);
}
.modal-arrow {
  background: var(--color-bg);
  border: 1px solid var(--color-border);
  width: 32px;
  height: 32px;
  border-radius: 50%;
  font-size: 18px;
  color: var(--color-primary);
  cursor: pointer;
  line-height: 1;
  transition: border-color 0.2s, color 0.2s;
}
.modal-arrow:hover {
  border-color: var(--color-accent);
  color: var(--color-accent);
}
.modal-count {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
}
.notice-text {
  font-size: var(--font-body-size);
}
.notice-item.important .notice-text {
  font-weight: 600;
}
.notice-meta {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
  margin-top: 2px;
}

.table-desc {
  font-size: var(--font-small);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-md);
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
  font-weight: 600;
  color: var(--color-text);
}
.schedule-day-date {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
  margin-bottom: 8px;
}
.schedule-day-shops {
  font-size: var(--font-tiny);
  line-height: 1.9;
}
.schedule-shop-closed {
  color: var(--color-danger);
  text-decoration: line-through;
}
.schedule-replaced {
  color: var(--color-success);
  font-size: 11px;
}

@media (max-width: 720px) {
  .schedule-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
