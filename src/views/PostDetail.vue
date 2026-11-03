<template>
  <div class="post-detail-page">
    <NavBar />
    <div class="container">
      <BackBar label="返回论坛" fallback="/forum" />
      <!-- TODO(队友B)：根据路由参数 :id 从 src/data/posts.json 读取帖子详情和评论 -->
      <div v-if="post" class="detail-card">
        <h2 class="post-title">{{ post.title }}</h2>
        <p class="post-meta">{{ post.author }} · {{ post.date }}</p>
        <div class="post-content">{{ post.content }}</div>

        <h3 class="sub-title">评论（{{ post.comments.length }}）</h3>
        <div v-for="(c, i) in post.comments" :key="i" class="comment-item">
          <p class="comment-user">{{ c.user }} · {{ c.date }}</p>
          <p>{{ c.content }}</p>
        </div>

        <!-- 登录后可以评论 -->
        <div v-if="currentUser" class="comment-composer">
          <textarea v-model="newComment" class="form-input" rows="3" placeholder="写下你的评论…"></textarea>
          <button class="btn" @click="addComment" style="margin-top:8px">评论</button>
        </div>
        <p v-else class="login-hint">
          <router-link to="/login">登录</router-link>后可参与评论
        </p>
      </div>
      <p v-else>没有找到这个帖子。</p>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import Footer from '../components/Footer.vue'
import BackBar from '../components/BackBar.vue'
import postsData from '../data/posts.json'

const route = useRoute()
const post = ref(null)
const newComment = ref('')

const currentUser = computed(() => {
  try {
    return JSON.parse(localStorage.getItem('nq_user') || 'null')
  } catch {
    return null
  }
})

onMounted(() => {
  post.value = postsData.find(p => p.id === route.params.id) || null
})

function addComment() {
  if (!newComment.value.trim()) return
  post.value.comments.push({
    user: currentUser.value?.shopName || '游客',
    date: '刚刚',
    content: newComment.value
  })
  newComment.value = ''
}
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
.post-title {
  font-family: var(--font-title);
  font-size: var(--font-h1);
  color: var(--color-primary);
}
.post-meta {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
  margin: 4px 0 var(--space-md);
}
.post-content {
  line-height: 1.9;
  padding-bottom: var(--space-md);
  border-bottom: 1px solid var(--color-border);
}
.sub-title {
  font-size: var(--font-h3);
  margin: var(--space-md) 0 var(--space-sm);
}
.comment-item {
  padding: 10px 0;
  border-bottom: 1px dashed var(--color-border);
}
.comment-user {
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
  margin-bottom: 4px;
}
.comment-composer {
  margin-top: var(--space-md);
}
.login-hint {
  margin-top: var(--space-md);
  color: var(--color-text-secondary);
}
</style>
