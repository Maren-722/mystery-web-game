<template>
  <div class="messages-page">
    <NavBar />
    <div class="container">
      <h2 class="section-title">短信</h2>
      <p class="page-desc">{{ currentUser ? '你和夜市里其他人的聊天记录。' : '' }}</p>

      <div v-if="currentUser">
        <div v-if="messageList.length">
          <div
            v-for="conv in messageList"
            :key="conv.with"
            class="card conv-card"
          >
            <div class="conv-header" @click="toggleConv(conv)">
              <div class="conv-avatar">{{ conv.with.slice(0, 1) }}</div>
              <div class="conv-info">
                <p class="conv-name">{{ conv.with }}</p>
                <p class="conv-preview">{{ conv.messages.length ? lastOf(conv.messages).content : '（记录已清空）' }}</p>
              </div>
              <span class="conv-count" v-if="conv.messages.length">{{ conv.messages.length }} 条</span>
              <span class="conv-chevron" :class="{ open: openConvs.has(conv.with) }">›</span>
            </div>
            <div v-if="openConvs.has(conv.with)" class="conv-body">
              <template v-if="conv.messages.length">
                <div
                  v-for="(msg, i) in conv.messages"
                  :key="i"
                  class="msg-item"
                  :class="{ mine: msg.from === currentUser.username }"
                >
                  <p class="msg-meta">{{ msg.from }} · {{ msg.time }}</p>
                  <p class="msg-content">{{ msg.content }}</p>
                </div>
              </template>
              <p v-else class="conv-empty">此会话的记录已被清空。</p>
            </div>
          </div>
        </div>
        <p v-else class="empty-hint">暂时没有私信记录。</p>
      </div>
      <p v-else class="empty-hint"><router-link to="/login">登录</router-link>后查看私信。</p>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount } from 'vue'
import NavBar from '../components/NavBar.vue'
import Footer from '../components/Footer.vue'
import messagesData from '../data/messages.json'
import { markNode } from '../utils/progress'

const messageList = ref([])
const openConvs = ref(new Set())

const currentUser = computed(() => {
  try {
    return JSON.parse(localStorage.getItem('nq_user') || 'null')
  } catch {
    return null
  }
})

// 展开某个会话才判定进度（内容点开后才可见，判定同样在点开时）
const PROGRESS_KEYS = {
  '小李|刘姐': 'chat-xl-lj',
  '刘姐|陈伯': 'chat-lj-cb',
  '老张|陈伯': 'chat-lz-cb'
}

function toggleConv(conv) {
  const s = new Set(openConvs.value)
  if (s.has(conv.with)) {
    s.delete(conv.with)
  } else {
    s.add(conv.with)
    const key = PROGRESS_KEYS[currentUser.value?.username + '|' + conv.with]
    if (key) markNode(key)
  }
  openConvs.value = s
}

function lastOf(messages) {
  return messages[messages.length - 1]
}

function loadData() {
  if (currentUser.value) {
    messageList.value = messagesData[currentUser.value.username] || []
  } else {
    messageList.value = []
  }
  openConvs.value = new Set()
}

onMounted(() => {
  loadData()
  // 切换账号后自动刷新为本账号的私信
  window.addEventListener('nq-user-changed', loadData)
})

onBeforeUnmount(() => {
  window.removeEventListener('nq-user-changed', loadData)
})
</script>

<style scoped>
.page-desc {
  color: var(--color-text-secondary);
  margin-bottom: var(--space-md);
}
.conv-card {
  margin-bottom: var(--space-md);
  padding: 0;
  overflow: hidden;
}
.conv-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  cursor: pointer;
  transition: background 0.15s;
}
.conv-header:hover {
  background: var(--color-bg);
}
.conv-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-primary);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 600;
  flex-shrink: 0;
}
.conv-info {
  flex: 1;
  min-width: 0;
}
.conv-name {
  font-size: var(--font-body-size);
  font-weight: 600;
  color: var(--color-text);
  margin-bottom: 2px;
}
.conv-preview {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.conv-preview.cleared {
  font-style: italic;
}
.conv-count {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
  flex-shrink: 0;
}
.conv-chevron {
  color: var(--color-text-muted);
  font-size: 18px;
  transform: rotate(0deg);
  transition: transform 0.2s;
  flex-shrink: 0;
}
.conv-chevron.open {
  transform: rotate(90deg);
}
.conv-body {
  border-top: 1px dashed var(--color-border);
  padding: 12px 16px;
  background: var(--color-bg);
}
.msg-item {
  padding: 8px 0;
}
.msg-item.mine {
  text-align: right;
}
.msg-meta {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
}
.msg-content {
  background: var(--color-card);
  display: inline-block;
  padding: 8px 12px;
  border-radius: var(--radius);
  max-width: 85%;
  line-height: 1.7;
  text-align: left;
}
.msg-item.mine .msg-content {
  background: #FFFBEB;
}
.conv-empty {
  color: var(--color-text-muted);
  font-size: var(--font-small);
  font-style: italic;
  text-align: center;
  padding: 12px 0;
}
.empty-hint {
  color: var(--color-text-secondary);
}
</style>
