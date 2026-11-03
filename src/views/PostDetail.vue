<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import Footer from '../components/Footer.vue'
import BackBar from '../components/BackBar.vue'
import { posts, currentUser, addComment as saveComment } from '../game/state.js'
const route=useRoute()
const post=computed(() => posts.value.find(p => p.id === route.params.id))
const newComment=ref('')
watch(() => route.params.id, () => {newComment.value=''})
function addComment(){if(saveComment(route.params.id,newComment.value))newComment.value=''}
</script>
<template><div class="page-shell"><NavBar /><main class="container post-container"><BackBar label="返回论坛" fallback="/forum" /><article v-if="post" class="card detail-card"><h1>{{ post.title }}</h1><p class="post-meta">{{ post.author }} <span v-if="post.authorId" class="author-id">账号ID {{ post.authorId === 'chennian' ? '夜归人' : post.authorId }}</span> · {{ post.date }}</p><p class="post-content">{{ post.content }}</p><h2>评论（{{ post.comments.length }}）</h2><div v-for="(c,i) in post.comments" :key="c.id || i" class="comment-item"><p class="post-meta">{{ c.user }} · {{ c.date }}</p><p>{{ c.content }}</p></div><form v-if="currentUser" class="comment-composer" @submit.prevent="addComment"><label for="comment-body" class="form-label">写下你的评论</label><textarea id="comment-body" v-model="newComment" class="form-input" rows="3" maxlength="2000" required></textarea><button class="btn">评论 · 仅本机保存</button></form><p v-else class="login-hint"><router-link :to="{path:'/login',query:{redirect:route.fullPath}}">登录后参与评论</router-link></p></article><div v-else class="card"><p>没有找到这个帖子。</p><router-link to="/forum">返回论坛</router-link></div></main><Footer /></div></template>
<style scoped>.post-container{max-width:800px;width:100%}.detail-card{padding:28px}.detail-card h1{font-family:var(--font-title);font-size:var(--font-h1);line-height:1.5}.post-meta{font-size:12px;color:var(--color-text-muted);margin:8px 0}.author-id{display:inline-block;margin-left:8px}.post-content{white-space:pre-line;line-height:1.9;padding:18px 0 26px;border-bottom:1px solid var(--color-border)}.detail-card h2{font-size:16px;margin:22px 0 10px}.comment-item{padding:12px 0;border-bottom:1px dashed var(--color-border);overflow-wrap:anywhere}.comment-composer{margin-top:24px}.comment-composer button{margin-top:10px}.login-hint{margin-top:20px;color:var(--color-primary)}</style>
