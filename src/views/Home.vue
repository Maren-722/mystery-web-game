<template>
  <div class="home-page">
    <NavBar />

    <!-- 首屏：夜市的灯 -->
    <section class="hero">
      <div class="hero-inner">
        <p class="hero-kicker">临岗市 · 江边老街 · 开市五年</p>
        <h1 class="hero-title">南桥夜市</h1>
        <p class="hero-sub">今夜照常营业　17:00 — 23:00</p>
        <div class="hero-rule"></div>
        <p class="hero-line">五周年前的这个秋天，A1 的灶台凉了。</p>
        <div class="hero-links">
          <a @click="$router.push('/stalls')">逛夜市 →</a>
          <a @click="$router.push('/forum')">看论坛 →</a>
        </div>
      </div>
      <span class="hero-date">2026.10.30</span>
      <div class="hero-lanterns" aria-hidden="true"><span>🏮</span><span>🏮</span><span>🏮</span></div>
    </section>

    <div class="container">

      <!-- 置顶：管理处的话（长期说明，特殊样式） -->
      <div v-if="pinnedNotice" class="pinned-card" @click="openNotice(0)">
        <span class="pinned-icon">🏮</span>
        <div class="pinned-body">
          <p class="pinned-tag">置顶 · 管理处</p>
          <p class="pinned-text">{{ pinnedNotice.text }}</p>
        </div>
        <span class="pinned-arrow">›</span>
      </div>

      <!-- 公告栏 -->
      <h2 class="section-title">公告栏</h2>
      <div class="notice-bar">
        <div
          v-for="(n, i) in regularNotices"
          :key="n.id"
          class="notice-item"
          @click="openNotice(i + 1)"
        >
          <span class="notice-tag" :style="{ background: tagColors[n.tag] || 'var(--color-primary)' }">{{ n.tag }}</span>
          <div class="notice-body">
            <p class="notice-text">{{ n.text }}</p>
            <p class="notice-meta">管理处 · {{ n.publishDate }}</p>
          </div>
        </div>
      </div>

      <!-- 公告详情弹窗 -->
      <div v-if="showModal" class="modal-mask" @click.self="closeNotice">
        <div
          class="modal-card"
          @touchstart="onTouchStart"
          @touchend="onTouchEnd"
        >
          <div class="modal-header">
            <span class="notice-tag" :style="{ background: tagColors[activeNotice.tag] || 'var(--color-primary)' }">{{ activeNotice.tag }}</span>
            <h3 class="modal-title">{{ activeNotice.text }}</h3>
            <button class="modal-close" @click="closeNotice">×</button>
          </div>
          <p class="modal-meta">
            南桥夜市管理处<template v-if="activeNotice.publishDate"> · {{ activeNotice.publishDate }}</template><template v-if="activeNotice.dateRange && activeNotice.dateRange !== '长期'"> · {{ activeNotice.dateRange }}</template>
          </p>
          <div class="modal-content">{{ activeNotice.fullText }}</div>

          <!-- 地铁公告：线路示意图直接展示 -->
          <div v-if="activeNotice.metro" class="metro-block">
            <div class="metro-map-wrap">
              <svg class="metro-map" viewBox="0 0 680 320" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="地铁线路示意图">
                <!-- 3号线（横） -->
                <line x1="46" y1="160" x2="648" y2="160" stroke="#3B7DD8" stroke-width="7" stroke-linecap="round" />
                <!-- 1号线（竖，在青石桥换乘） -->
                <line x1="429" y1="38" x2="429" y2="292" stroke="#2FA84F" stroke-width="7" stroke-linecap="round" />
                <!-- 3号线两端方向 -->
                <text x="52" y="140" font-size="13" fill="#3B7DD8" font-weight="600">← 体育中心方向</text>
                <text x="646" y="140" font-size="13" fill="#3B7DD8" font-weight="600" text-anchor="end">城南客运站方向 →</text>
                <!-- 1号线两端方向 -->
                <text x="440" y="52" font-size="13" fill="#2FA84F" font-weight="600">北苑方向 ↑</text>
                <text x="440" y="286" font-size="13" fill="#2FA84F" font-weight="600">↓ 纺织城方向</text>

                <!-- 3号线站点 -->
                <g v-for="(st, i) in line3" :key="'l3-' + i">
                  <circle v-if="!st.here" :cx="st.x" cy="160" r="6" fill="#fff" stroke="#3B7DD8" stroke-width="3" />
                  <text :x="st.x" y="192" font-size="13" :fill="st.key ? '#B3541E' : '#5b5b5b'" :font-weight="st.key ? '700' : '400'" text-anchor="middle">{{ st.name }}</text>
                </g>
                <!-- 1号线站点 -->
                <g v-for="(st, i) in line1" :key="'l1-' + i">
                  <circle :cx="429" :cy="st.y" r="6" fill="#fff" stroke="#2FA84F" stroke-width="3" />
                  <text x="429" :y="st.y - 12" font-size="13" fill="#5b5b5b" text-anchor="middle">{{ st.name }}</text>
                </g>

                <!-- 换乘站：青石桥 -->
                <rect x="420" y="151" width="18" height="18" rx="4" fill="#fff" stroke="#3B7DD8" stroke-width="3" />
                <rect x="420" y="151" width="18" height="18" rx="4" fill="#fff" stroke="#2FA84F" stroke-width="3" transform="rotate(45 429 160)" />
                <text x="429" y="214" font-size="13" fill="#5b5b5b" text-anchor="middle">青石桥（换乘）</text>

                <!-- 当前站：南桥 -->
                <circle cx="324" cy="160" r="13" fill="#FFF3D6" stroke="#B3541E" stroke-width="3" />
                <circle cx="324" cy="160" r="5" fill="#B3541E" />
                <text x="324" y="132" font-size="15" fill="#B3541E" font-weight="700" text-anchor="middle">南桥站（您在这）</text>
                <text x="324" y="214" font-size="13" fill="#B3541E" font-weight="700" text-anchor="middle">南桥</text>

                <!-- 图例 -->
                <g font-size="12" fill="#8a8a8a">
                  <line x1="60" y1="266" x2="92" y2="266" stroke="#3B7DD8" stroke-width="6" stroke-linecap="round" />
                  <text x="100" y="270">3号线</text>
                  <line x1="160" y1="266" x2="192" y2="266" stroke="#2FA84F" stroke-width="6" stroke-linecap="round" />
                  <text x="200" y="270">1号线</text>
                  <rect x="260" y="259" width="14" height="14" rx="3" fill="#fff" stroke="#3B7DD8" stroke-width="2.5" />
                  <text x="282" y="270">换乘站</text>
                  <circle cx="360" cy="266" r="7" fill="#FFF3D6" stroke="#B3541E" stroke-width="3" />
                  <text x="376" y="270">当前站</text>
                </g>
              </svg>
              <p class="metro-note">示意图仅供参考，以车站实际公告为准。</p>
            </div>
          </div>

          <div class="modal-nav" v-if="visibleNotices.length > 1">
            <button class="modal-arrow" @click="prevNotice">‹</button>
            <span class="modal-count">{{ activeIndex + 1 }} / {{ visibleNotices.length }}</span>
            <button class="modal-arrow" @click="nextNotice">›</button>
          </div>
        </div>
      </div>

      <!-- 排班表：2026年10月 日历 -->
      <h2 class="section-title">夜市排班表</h2>
      <p class="table-desc">十月值日安排，每天两位摊主轮流值守收摊巡查，由管理处统一排班。</p>
      <div class="cal-grid">
        <div class="cal-head" v-for="w in weekNames" :key="w">{{ w }}</div>
        <div v-for="pad in leadPads" :key="'pad-' + pad" class="cal-day cal-pad"></div>
        <div
          v-for="day in october"
          :key="day.date"
          class="cal-day"
          :class="{ today: day.date === 30, alert: day.anyStruck }"
        >
          <div class="cal-top">
            <span class="cal-date">{{ day.date }}</span>
            <span v-if="day.date === 30" class="cal-today-tag">今天</span>
          </div>
          <div class="cal-shops">
            <template v-for="(shop, si) in day.shops" :key="si">
              <template v-if="shop.struck">
                <span class="cal-shop struck">{{ shop.name }}</span><span class="cal-replace">→{{ shop.replacedBy }}</span>
              </template>
              <span v-else class="cal-shop">{{ shop.name }}</span>
              <br v-if="si === 0">
            </template>
          </div>
        </div>
      </div>
      <p class="cal-legend"><span class="struck-demo">划线</span> 为请假/停摊，由 <span class="replace-demo">绿色</span> 摊位顶替。</p>

    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import NavBar from '../components/NavBar.vue'
import Footer from '../components/Footer.vue'
import noticesData from '../data/notices.json'
import { markNode } from '../utils/progress'

// 公告标签配色
const tagColors = {
  '通知': 'var(--color-danger)',
  '开业': 'var(--color-success)',
  '上新': 'var(--color-accent)',
  '活动': 'var(--color-primary)'
}

// 首页只展示「刊登中」：置顶的单独渲染，其余按发布日期新的在前
function parseDate(s) {
  const m = String(s || '').match(/(\d+)月(\d+)日/)
  return m ? (+m[1]) * 100 + (+m[2]) : 0
}
const visibleNotices = computed(() => {
  const active = noticesData.filter(n => n.state === '刊登中')
  const pinned = active.filter(n => n.pinned)
  const regular = active
    .filter(n => !n.pinned)
    .sort((a, b) => parseDate(b.publishDate) - parseDate(a.publishDate))
  return [...pinned, ...regular]
})
const pinnedNotice = computed(() => visibleNotices.value.find(n => n.pinned) || null)
const regularNotices = computed(() => visibleNotices.value.filter(n => !n.pinned))

// 公告弹窗
const showModal = ref(false)
const activeIndex = ref(0)
const activeNotice = computed(() => visibleNotices.value[activeIndex.value])

function openNotice(i) {
  activeIndex.value = i
  showModal.value = true
  // 地铁公告：弹窗打开即能看到线路图，打开时就记录进度
  if (activeNotice.value?.metro) {
    markNode('metro-map')
  }
}
function closeNotice() {
  showModal.value = false
}
function prevNotice() {
  const len = visibleNotices.value.length
  activeIndex.value = (activeIndex.value - 1 + len) % len
  if (activeNotice.value?.metro) markNode('metro-map')
}
function nextNotice() {
  const len = visibleNotices.value.length
  activeIndex.value = (activeIndex.value + 1) % len
  if (activeNotice.value?.metro) markNode('metro-map')
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

// ---------------- 排班表：2026年10月 ----------------
const weekNames = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
// 2026年10月1日是周四 → 周一开头的日历前面空3格
const leadPads = 3

// 每周值班模板（摊位按此轮值，老摊位每周两次）
const weekPlan = {
  1: ['老街凉面', '巷尾臭豆腐'],      // 周一
  2: ['陈记糖粥藕', '小李炒粉'],      // 周二
  3: ['鲜果小铺', '炭火烧烤'],        // 周三
  4: ['巷口馄饨', '刘姐麻辣烫'],      // 周四
  5: ['张记卤味', '街角烤冷面'],      // 周五
  6: ['巷口馄饨', '巷尾臭豆腐'],      // 周六
  0: ['陈记糖粥藕', '老街凉面']       // 周日
}

// 陈伯的班被划掉的日期：10.6/10.11 住院那一周，10.27 失踪之后
const struckMap = {
  6: { '陈记糖粥藕': '炭火烧烤' },
  11: { '陈记糖粥藕': '刘姐麻辣烫' },
  27: { '陈记糖粥藕': '鲜果小铺' }
}

const october = []
for (let d = 1; d <= 31; d++) {
  const weekday = new Date(2026, 9, d).getDay()
  const struck = struckMap[d] || {}
  const shops = weekPlan[weekday].map(name => ({
    name,
    struck: !!struck[name],
    replacedBy: struck[name] || ''
  }))
  october.push({
    date: d,
    shops,
    anyStruck: shops.some(s => s.struck)
  })
}

// ---------------- 地铁线路图数据 ----------------
const line3 = [
  { name: '体育中心', x: 72 },
  { name: '半山公园', x: 122 },
  { name: '东湖', x: 172 },
  { name: '市政府', x: 224 },
  { name: '工业大学', x: 274 },
  { name: '', x: 324 },            // 南桥站单独绘制
  { name: '柳浪湾', x: 376 },
  { name: '', x: 429 },            // 青石桥换乘站单独绘制
  { name: '南湖公园', x: 480 },
  { name: '双井街', x: 532 },
  { name: '梧桐苑', x: 584, key: true },
  { name: '城南客运站', x: 644 }
].filter(s => s.name !== '')
const line1 = [
  { name: '北苑', y: 74 },
  { name: '市图书馆', y: 116 },
  { name: '', y: 160 },            // 青石桥（换乘）单独绘制
  { name: '梅林', y: 208 },
  { name: '纺织城', y: 252 }
].filter(s => s.name !== '')
</script>

<style scoped>
/* 首屏：墨色夜空 + 几盏远处的灯 */
.hero {
  position: relative;
  background: var(--ink);
  overflow: hidden;
}
.hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(420px 230px at 78% 20%, rgba(215, 154, 74, 0.22), transparent 70%),
    radial-gradient(300px 190px at 64% 74%, rgba(180, 70, 47, 0.16), transparent 72%),
    radial-gradient(520px 260px at 10% 8%, rgba(215, 154, 74, 0.10), transparent 70%);
}
.hero::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 110px;
  background: linear-gradient(to bottom, rgba(20, 23, 29, 0), var(--color-bg));
}
.hero-inner {
  position: relative;
  z-index: 2;
  max-width: var(--container-max);
  margin: 0 auto;
  padding: 82px 28px 78px;
}
.hero-kicker {
  font-size: 11px;
  letter-spacing: 3.2px;
  color: rgba(215, 154, 74, 0.92);
}
.hero-title {
  font-family: var(--font-title);
  font-size: 62px;
  font-weight: 600;
  letter-spacing: 12px;
  line-height: 1.15;
  color: #FAF3E5;
  margin: 20px 0 12px;
}
.hero-sub {
  font-size: 13px;
  letter-spacing: 2px;
  color: #B9AE9C;
}
.hero-rule {
  width: 46px;
  height: 1px;
  background: var(--amber);
  margin: 24px 0;
}
.hero-line {
  font-family: var(--font-title);
  font-size: 17px;
  letter-spacing: 1.2px;
  color: #E4D8C4;
}
.hero-links {
  display: flex;
  gap: 24px;
  margin-top: 28px;
  font-size: 13px;
  letter-spacing: 1px;
}
.hero-links a {
  color: var(--amber-soft);
  border-bottom: 1px solid rgba(215, 154, 74, 0.38);
  padding-bottom: 2px;
  cursor: pointer;
  transition: color 0.2s, border-color 0.2s;
}
.hero-links a:hover {
  color: #fff;
  border-color: #fff;
}
.hero-date {
  position: absolute;
  right: 30px;
  bottom: 26px;
  font-size: 11px;
  letter-spacing: 3px;
  color: rgba(239, 230, 214, 0.35);
  z-index: 2;
}
.hero-lanterns {
  position: absolute;
  top: 48px;
  right: 64px;
  display: flex;
  gap: 18px;
  z-index: 2;
  opacity: 0.92;
}
.hero-lanterns span {
  font-size: 24px;
  filter: drop-shadow(0 0 12px rgba(255, 190, 92, 0.5));
  animation: sway 5s ease-in-out infinite;
}
.hero-lanterns span:nth-child(2) {
  font-size: 30px;
  margin-top: -6px;
  animation-delay: -1.6s;
}
.hero-lanterns span:nth-child(3) {
  font-size: 20px;
  margin-top: 4px;
  animation-delay: -3.2s;
}
@keyframes sway {
  0%, 100% { transform: rotate(-3deg) translateY(0); }
  50% { transform: rotate(3deg) translateY(2px); }
}

/* 置顶：管理处的话（与普通公告不同的特殊样式） */
.pinned-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: var(--ink-2);
  border-left: 3px solid var(--amber);
  border-radius: var(--radius-lg);
  padding: 18px 22px;
  margin-bottom: 30px;
  cursor: pointer;
  box-shadow: 0 10px 28px rgba(20, 23, 29, 0.16);
  transition: transform 0.2s, box-shadow 0.2s;
}
.pinned-card:hover {
  transform: translateY(-1px);
  box-shadow: 0 14px 34px rgba(20, 23, 29, 0.22);
}
.pinned-icon {
  font-size: 26px;
  line-height: 1;
  filter: drop-shadow(0 0 8px rgba(255, 200, 120, 0.55));
}
.pinned-body {
  flex: 1;
  min-width: 0;
}
.pinned-tag {
  font-size: 10px;
  letter-spacing: 2px;
  color: var(--amber-soft);
  margin-bottom: 4px;
}
.pinned-text {
  font-family: var(--font-title);
  font-size: 16px;
  letter-spacing: 0.8px;
  color: #F6EEDF;
  font-weight: 600;
}
.pinned-arrow {
  color: var(--amber-soft);
  font-size: 20px;
}

.notice-bar {
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 4px 22px;
  margin-bottom: var(--space-lg);
}
.notice-item {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 15px 0;
  border-bottom: 1px solid var(--color-border);
  cursor: pointer;
  transition: background 0.15s;
}
.notice-item:hover {
  background: #FBF6EA;
}
.notice-item:last-child {
  border-bottom: none;
}
.notice-tag {
  background: var(--color-primary);
  color: #F7F1E4;
  padding: 2px 9px;
  border-radius: 2px;
  font-size: 11px;
  letter-spacing: 1px;
  flex-shrink: 0;
  margin-top: 3px;
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
  max-width: 560px;
  width: 100%;
  max-height: 86vh;
  overflow-y: auto;
  background: var(--color-card);
  border-radius: var(--radius-lg);
  padding: 28px 26px;
  box-shadow: 0 20px 60px rgba(20, 23, 29, 0.35);
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
  font-size: 19px;
  letter-spacing: 0.8px;
  color: var(--color-text);
  line-height: 1.5;
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
.notice-meta {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
  margin-top: 2px;
}

/* 地铁线路图 */
.metro-block {
  margin-top: var(--space-md);
}
.metro-map-wrap {
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  background: #FDFCF9;
  padding: 8px;
}
.metro-map {
  width: 100%;
  height: auto;
  display: block;
}
.metro-note {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
  text-align: center;
  margin-top: 6px;
}

/* 排班日历 */
.table-desc {
  font-size: var(--font-small);
  color: var(--color-text-secondary);
  margin-bottom: var(--space-md);
}
.cal-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 5px;
  margin-bottom: var(--space-xs);
}
.cal-head {
  text-align: center;
  font-size: 11px;
  letter-spacing: 1.6px;
  font-weight: 500;
  color: var(--color-text-muted);
  padding: 4px 0 10px;
}
.cal-day {
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: 9px 8px;
  min-height: 96px;
}
.cal-pad {
  background: transparent;
  border-color: transparent;
}
.cal-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 7px;
}
.cal-date {
  font-family: var(--font-title);
  font-size: 15px;
  font-weight: 600;
  color: var(--color-text);
}
.cal-today-tag {
  font-size: 9px;
  letter-spacing: 1px;
  background: var(--color-accent);
  color: #fff;
  padding: 1px 6px;
  border-radius: 2px;
}
.cal-day.today {
  border-color: var(--color-accent);
  background: #FFFAEE;
}
.cal-day.alert {
  border-color: #E7C9BC;
  background: #FDF6F1;
}
.cal-day.today.alert {
  border-color: var(--color-accent);
}
.cal-shops {
  font-size: 10.5px;
  line-height: 1.9;
}
.cal-shop {
  color: var(--color-text-secondary);
  display: inline-block;
}
.cal-shop.struck {
  color: var(--color-danger);
  text-decoration: line-through;
  font-weight: 600;
}
.cal-replace {
  color: var(--color-success);
  font-size: 10px;
  margin-left: 2px;
}
.cal-legend {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
  margin-bottom: var(--space-lg);
}
.struck-demo {
  color: var(--color-danger);
  text-decoration: line-through;
}
.replace-demo {
  color: var(--color-success);
}

@media (max-width: 720px) {
  .hero-inner {
    padding: 54px 18px 52px;
  }
  .hero-title {
    font-size: 40px;
    letter-spacing: 8px;
    margin: 16px 0 10px;
  }
  .hero-line {
    font-size: 15px;
  }
  .hero-date {
    display: none;
  }
  .pinned-text {
    font-size: var(--font-body-size);
  }
  .cal-grid {
    grid-template-columns: repeat(7, 1fr);
    gap: 3px;
  }
  .cal-day {
    padding: 5px 3px;
    min-height: 72px;
  }
  .cal-shops {
    font-size: 9px;
    line-height: 1.55;
  }
  .cal-date {
    font-size: var(--font-small);
  }
  .cal-head {
    font-size: 10px;
    letter-spacing: 0;
  }
}
</style>
