<template>
  <div class="notes-page">
    <NavBar />
    <div class="container">
      <h2 class="section-title">我的手记</h2>
      <p class="page-desc">只有你自己能看到的私密手记。</p>

      <!-- TODO(队友C)：根据当前登录账号从 src/data/notes.json（或 messages.json 内）读取手记 -->
      <!-- 关键：陈伯账号登录后，这里显示《给念儿的》等隐藏手记 -->
      <div v-if="currentUser">
        <div v-if="notes.length">
          <div v-for="(note, i) in notes" :key="i" class="card note-card">
            <p class="note-date">{{ note.date }}</p>
            <p class="note-content">{{ note.content }}</p>
          </div>
        </div>
        <p v-else class="empty-hint">还没有手记。</p>
      </div>
      <p v-else class="empty-hint"><router-link to="/login">登录</router-link>后查看手记。</p>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import NavBar from '../components/NavBar.vue'
import Footer from '../components/Footer.vue'
import messagesData from '../data/messages.json'

// 手记数据：可以放在 src/data/messages.json 的 notes 字段，或单独建 notes.json
const notes = ref([])

const currentUser = computed(() => {
  try {
    return JSON.parse(localStorage.getItem('nq_user') || 'null')
  } catch {
    return null
  }
})

onMounted(() => {
  if (currentUser.value) {
    notes.value = messagesData[currentUser.value.username]?.notes || []
  }
})
</script>

<style scoped>
.page-desc {
  color: var(--color-text-secondary);
  margin-bottom: var(--space-md);
}
.note-card {
  margin-bottom: var(--space-md);
  border-left: 3px solid var(--color-accent);
}
.note-date {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
  margin-bottom: var(--space-xs);
}
.note-content {
  white-space: pre-line;
  line-height: 1.9;
}
.empty-hint {
  color: var(--color-text-secondary);
}
</style>
