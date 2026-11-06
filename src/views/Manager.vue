<template>
  <div class="manager-page">
    <NavBar />
    <div class="container">
      <h2 class="section-title">管理处工作台</h2>
      <p class="page-desc">南桥夜市管理处 · 内部系统。公告从这里发布、下架，历史记录长期留存。</p>

      <!-- 通告历史 -->
      <div class="history-head">
        <h3 class="sub-title">通告历史</h3>
        <div class="filter-tabs">
          <button
            v-for="f in filters"
            :key="f"
            class="filter-tab"
            :class="{ active: currentFilter === f }"
            @click="currentFilter = f"
          >{{ f }}（{{ countOf(f) }}）</button>
        </div>
      </div>

      <div class="history-list">
        <div
          v-for="n in filteredNotices"
          :key="n.id"
          class="card history-item"
          :class="{ deleted: n.state === '已删除' }"
          @click="openNotice(n)"
        >
          <div class="history-row">
            <span class="state-badge" :class="stateClass(n.state)">{{ n.state }}</span>
            <span class="notice-tag" :style="{ background: tagColors[n.tag] || 'var(--color-primary)' }">{{ n.tag }}</span>
            <span class="history-text" :class="{ 'text-deleted': n.state === '已删除' }">{{ n.text }}</span>
          </div>
          <p class="history-meta">{{ n.publishDate ? '发布于 ' + n.publishDate : '长期刊登' }}<template v-if="n.dateRange && n.dateRange !== '长期'"> · {{ n.dateRange }}</template></p>
        </div>
      </div>

      <!-- 通告详情 -->
      <div v-if="showDetail" class="modal-mask" @click.self="closeNotice">
        <div class="modal-card">
          <div class="modal-header">
            <span class="state-badge" :class="stateClass(activeNotice.state)">{{ activeNotice.state }}</span>
            <h3 class="modal-title" :class="{ 'text-deleted': activeNotice.state === '已删除' }">{{ activeNotice.text }}</h3>
            <button class="modal-close" @click="closeNotice">×</button>
          </div>
          <p class="modal-meta">南桥夜市管理处 · {{ activeNotice.publishDate ? '发布于 ' + activeNotice.publishDate : '长期刊登' }}<template v-if="activeNotice.dateRange && activeNotice.dateRange !== '长期'"> · {{ activeNotice.dateRange }}</template></p>
          <div class="modal-content">{{ activeNotice.fullText }}</div>
        </div>
      </div>
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

// 通告历史按发布时间新的在前
function parseDate(s) {
  const m = String(s || '').match(/(\d+)月(\d+)日/)
  const y = String(s || '').match(/^(\d{4})年/)
  return (y ? +y[1] : 2026) * 10000 + (m ? (+m[1]) * 100 + (+m[2]) : 0)
}
const allNotices = [...noticesData].sort((a, b) => parseDate(b.publishDate) - parseDate(a.publishDate))

const filters = ['全部', '刊登中', '已过期', '已删除']
const currentFilter = ref('全部')
const filteredNotices = computed(() =>
  currentFilter.value === '全部' ? allNotices : allNotices.filter(n => n.state === currentFilter.value)
)
function countOf(f) {
  return f === '全部' ? allNotices.length : allNotices.filter(n => n.state === f).length
}

const tagColors = {
  '通知': 'var(--color-danger)',
  '开业': 'var(--color-success)',
  '上新': 'var(--color-accent)',
  '活动': 'var(--color-primary)'
}
function stateClass(state) {
  if (state === '刊登中') return 'st-active'
  if (state === '已过期') return 'st-expired'
  return 'st-deleted'
}

const showDetail = ref(false)
const activeNotice = ref(null)

// 点开通告详情才能看到全文（尤其是已删除的），判定挂在点开时
function openNotice(n) {
  activeNotice.value = n
  showDetail.value = true
  if (n.id === 'nt-missing') {
    markNode('notice-missing')
  }
}
function closeNotice() {
  showDetail.value = false
}
</script>

<style scoped>
.page-desc {
  color: var(--color-text-secondary);
  margin-bottom: var(--space-lg);
}
.history-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: var(--space-md);
}
.sub-title {
  font-size: var(--font-h3);
}
.filter-tabs {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
.filter-tab {
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: 20px;
  padding: 4px 14px;
  font-size: var(--font-small);
  color: var(--color-text-secondary);
  cursor: pointer;
  font-family: var(--font-body);
  transition: all 0.15s;
}
.filter-tab:hover {
  border-color: var(--color-accent);
}
.filter-tab.active {
  background: var(--color-primary);
  border-color: var(--color-primary);
  color: #fff;
}

.history-list {
  margin-bottom: var(--space-lg);
}
.history-item {
  cursor: pointer;
  margin-bottom: var(--space-sm);
  padding: 12px 16px;
  transition: border-color 0.2s;
}
.history-item:hover {
  border-color: var(--color-accent);
}
.history-item.deleted {
  opacity: 0.78;
  background: var(--color-bg);
}
.history-row {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.state-badge {
  font-size: 11px;
  padding: 1px 8px;
  border-radius: 4px;
  flex-shrink: 0;
}
.st-active {
  background: #E8F5E9;
  color: #2E7D32;
}
.st-expired {
  background: #F5F5F5;
  color: #9E9E9E;
}
.st-deleted {
  background: #FDECEA;
  color: #C62828;
}
.notice-tag {
  color: #fff;
  padding: 1px 8px;
  border-radius: 4px;
  font-size: 11px;
  flex-shrink: 0;
}
.history-text {
  font-size: var(--font-body-size);
  color: var(--color-text);
}
.text-deleted {
  text-decoration: line-through;
  color: var(--color-text-muted);
}
.history-meta {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
  margin-top: 4px;
  padding-left: 2px;
}

/* 详情弹窗 */
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
  max-width: 540px;
  width: 100%;
  max-height: 86vh;
  overflow-y: auto;
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
</style>
