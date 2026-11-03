<template>
  <div class="messages-page">
    <NavBar />
    <div class="container">
      <h2 class="section-title">短信</h2>
      <p class="page-desc">你和夜市里其他人的聊天记录。</p>

      <!-- TODO(队友C)：根据当前登录账号（localStorage 的 nq_user）从 src/data/messages.json 读取对应私信 -->
      <div v-if="currentUser">
        <div v-if="messageList.length">
          <div
            v-for="conv in messageList"
            :key="conv.with"
            class="card conv-card"
          >
            <h3 class="conv-title">与 {{ conv.with }} 的对话</h3>
            <div
              v-for="(msg, i) in conv.messages"
              :key="i"
              class="msg-item"
              :class="{ mine: msg.from === currentUser.username }"
            >
              <p class="msg-meta">{{ msg.from }} · {{ msg.time }}</p>
              <p class="msg-content">{{ msg.content }}</p>
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
import { ref, computed, onMounted } from 'vue'
import NavBar from '../components/NavBar.vue'
import Footer from '../components/Footer.vue'
import messagesData from '../data/messages.json'

// 私信数据：src/data/messages.json（你负责写这个文件）
// 结构建议：{ "chenjigui": [{ with: "老张", messages: [{from, time, content}] }] }
const messageList = ref([])

const currentUser = computed(() => {
  try {
    return JSON.parse(localStorage.getItem('nq_user') || 'null')
  } catch {
    return null
  }
})

onMounted(() => {
  if (currentUser.value) {
    messageList.value = messagesData[currentUser.value.username] || []
  }
})
</script>

<style scoped>
.page-desc {
  color: var(--color-text-secondary);
  margin-bottom: var(--space-md);
}
.conv-card {
  margin-bottom: var(--space-md);
}
.conv-title {
  font-size: var(--font-h3);
  color: var(--color-primary);
  margin-bottom: var(--space-sm);
  border-bottom: 1px solid var(--color-border);
  padding-bottom: var(--space-xs);
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
  background: var(--color-bg);
  display: inline-block;
  padding: 8px 12px;
  border-radius: var(--radius);
  max-width: 80%;
}
.msg-item.mine .msg-content {
  background: #FFFBEB;
}
.empty-hint {
  color: var(--color-text-secondary);
}
</style>
