<template>
  <div class="post-detail-page">
    <NavBar />
    <div class="container">
      <BackBar label="返回论坛" fallback="/forum" />
      <!-- 帖子详情：内置帖子 + 玩家发布的帖子（玩家评论存 localStorage，退出登录仍可见） -->
      <div v-if="post" class="detail-card">
        <h2 class="post-title">{{ post.title }}</h2>
        <p class="post-meta">{{ post.author }} · {{ post.date }}</p>
        <div class="post-content">{{ post.content }}</div>

        <h3 class="sub-title">评论（{{ mergedComments.length }}）</h3>
        <div v-for="(c, i) in mergedComments" :key="i" class="comment-item">
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

// 读取玩家发布的帖子（与 Forum 同一份数据）
function readLocalPosts() {
  try {
    return JSON.parse(localStorage.getItem('nq_posts') || '[]')
  } catch {
    return []
  }
}

// 玩家补充的评论：{ postId: [ {user,date,content} ] }
function readLocalComments() {
  try {
    return JSON.parse(localStorage.getItem('nq_comments') || '{}')
  } catch {
    return {}
  }
}

// 合并展示：帖子自带评论 + 玩家后续补充的评论
const mergedComments = computed(() => {
  if (!post.value) return []
  const extra = readLocalComments()[post.value.id] || []
  return [...(post.value.comments || []), ...extra]
})

onMounted(() => {
  const id = route.params.id
  const localPosts = readLocalPosts()
  const found = localPosts.find(p => p.id === id) || postsData.find(p => p.id === id) || null
  post.value = found
})

function addComment() {
  if (!newComment.value.trim() || !post.value) return
  const comment = {
    user: currentUser.value?.shopName || currentUser.value?.username || '游客',
    date: new Date().toLocaleDateString('zh-CN', { month: 'long', day: 'numeric' }),
    content: newComment.value.trim()
  }
  // 持久化到 localStorage：退出登录/切换账号后依然存在，退出游戏(清浏览器数据)后不再保留
  const localComments = readLocalComments()
  localComments[post.value.id] = [...(localComments[post.value.id] || []), comment]
  localStorage.setItem('nq_comments', JSON.stringify(localComments))
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
