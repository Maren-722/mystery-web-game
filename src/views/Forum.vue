<template>
  <div class="forum-page">
    <NavBar />
    <div class="container">
      <div class="forum-header">
        <h2 class="section-title">夜市论坛</h2>
        <!-- 登录后可以发帖 -->
        <button v-if="currentUser" class="btn" @click="showComposer = true">发帖</button>
      </div>
      <p class="page-desc">摊主和老顾客都在这里聊两句。登录后可以发帖、评论。</p>

      <!-- 发帖框（登录后可见） -->
      <div v-if="showComposer" class="card composer">
        <input v-model="newTitle" class="form-input" placeholder="帖子标题" style="margin-bottom:8px">
        <textarea v-model="newContent" class="form-input" rows="4" placeholder="内容…"></textarea>
        <button class="btn" @click="publishPost" style="margin-top:8px">发布</button>
      </div>

      <!-- TODO(队友B)：从 src/data/posts.json 循环渲染帖子列表 -->
      <div
        v-for="post in posts"
        :key="post.id"
        class="card post-card"
        @click="$router.push('/forum/' + post.id)"
      >
        <h3 class="post-title">{{ post.title }}</h3>
        <p class="post-meta">{{ post.author }} · {{ post.date }} · {{ post.replies }} 回复</p>
        <p class="post-preview">{{ post.preview }}</p>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import NavBar from '../components/NavBar.vue'
import Footer from '../components/Footer.vue'
import postsData from '../data/posts.json'

// 帖子列表：数据从 src/data/posts.json 读取（你负责写这个文件）
const posts = ref([])
const showComposer = ref(false)
const newTitle = ref('')
const newContent = ref('')

const currentUser = computed(() => {
  try {
    return JSON.parse(localStorage.getItem('nq_user') || 'null')
  } catch {
    return null
  }
})

onMounted(() => {
  posts.value = postsData
})

// 发帖：存 localStorage，临时渲染（无后端，仅本机可见）
function publishPost() {
  if (!newTitle.value.trim()) return
  posts.value.unshift({
    id: 'local-' + Date.now(),
    title: newTitle.value,
    author: currentUser.value?.shopName || currentUser.value?.username,
    date: '刚刚',
    replies: 0,
    preview: newContent.value
  })
  newTitle.value = ''
  newContent.value = ''
  showComposer.value = false
}
</script>

<style scoped>
.forum-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.page-desc {
  color: var(--color-text-secondary);
  margin-bottom: var(--space-md);
}
.composer {
  margin-bottom: var(--space-md);
}
.post-card {
  cursor: pointer;
  margin-bottom: var(--space-sm);
  transition: border-color 0.2s;
}
.post-card:hover {
  border-color: var(--color-accent);
}
.post-title {
  font-size: var(--font-h3);
  color: var(--color-primary);
  margin-bottom: 4px;
}
.post-meta {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
  margin-bottom: 4px;
}
.post-preview {
  font-size: var(--font-small);
  color: var(--color-text-secondary);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
