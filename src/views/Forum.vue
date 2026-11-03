<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import Footer from '../components/Footer.vue'
import { posts, currentUser, publishPost as savePost } from '../game/state.js'
const router=useRouter()
const search=ref(''),showComposer=ref(false),newTitle=ref(''),newContent=ref(''),error=ref('')
const filtered=computed(() => posts.value.filter(p => [p.title,p.author,p.content,...p.comments.map(c=>c.content)].join(' ').includes(search.value.trim())))
function publishPost(){const id=savePost(newTitle.value,newContent.value);if(!id){error.value='请填写标题和正文，并确认已登录';return}newTitle.value='';newContent.value='';showComposer.value=false;router.push('/forum/'+id)}
</script>
<template>
  <div class="page-shell"><NavBar /><main class="container forum-container"><div class="forum-header"><h1 class="section-title">夜市论坛</h1><button v-if="currentUser" class="btn" @click="showComposer=!showComposer">{{ showComposer?'收起':'发帖' }}</button></div><p class="page-desc">摊主和老顾客都在这里聊两句。发帖与评论仅保存在本机。</p>
    <label for="forum-search" class="form-label">搜索帖子与评论</label><input id="forum-search" v-model="search" type="search" class="form-input forum-search" placeholder="输入人物、摊位或关键词">
    <form v-if="showComposer && currentUser" class="card composer" @submit.prevent="publishPost"><label for="post-title">帖子标题</label><input id="post-title" v-model="newTitle" class="form-input" maxlength="80" required><label for="post-body">正文</label><textarea id="post-body" v-model="newContent" class="form-input" rows="4" maxlength="5000" required></textarea><button class="btn">发布到本机论坛</button><p role="alert">{{ error }}</p></form>
    <router-link v-for="post in filtered" :key="post.id" class="card post-card" :to="'/forum/'+post.id"><h2>{{ post.title }}</h2><p class="post-meta">{{ post.author }} · {{ post.date }} · {{ post.comments.length }} 回复</p><p class="post-preview">{{ post.preview }}</p></router-link><p v-if="!filtered.length" class="empty-hint">没有找到相关帖子，试试其他关键词。</p>
  </main><Footer /></div>
</template>
<style scoped>.forum-container{width:100%;max-width:900px}.forum-header{display:flex;align-items:center;justify-content:space-between}.forum-search{margin-bottom:20px}.composer{display:grid;gap:10px;margin-bottom:20px}.post-card{display:block;margin-bottom:10px;transition:border-color .2s}.post-card:hover{border-color:var(--color-accent)}.post-card h2{font-size:var(--font-h3);color:var(--color-primary);margin-bottom:5px}.post-meta{font-size:12px;color:var(--color-text-muted);margin-bottom:5px}.post-preview{font-size:13px;color:var(--color-text-secondary);overflow:hidden;text-overflow:ellipsis;white-space:nowrap}</style>
