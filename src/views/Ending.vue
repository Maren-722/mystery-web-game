<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import endings from '../data/endings.json'
import { progress, resetGame } from '../game/state.js'
const router=useRouter()
const ending=computed(() => endings[progress.value.ending])
function restart() { resetGame(); router.replace('/') }
</script>
<template><main class="ending-page"><article v-if="ending" class="ending-card"><span class="ending-tag">结局 {{ progress.ending }}</span><h1>{{ ending.title }}</h1><p class="ending-text">{{ ending.content }}</p><p class="ending-after">你在南桥夜市读到的故事，到这里暂告一段落。</p><button class="btn btn-block" @click="router.push('/notes')">回看人物手记</button><button class="restart" @click="restart">重新开始 · 清除本次调查及本机论坛记录</button></article></main></template>
<style scoped>.ending-page{min-height:100vh;background:var(--color-primary-dark);padding:48px 20px;display:grid;place-items:center}.ending-card{max-width:620px;background:var(--color-bg);padding:44px;border-radius:var(--radius-lg)}.ending-tag{color:var(--color-accent);font-size:12px;letter-spacing:3px}.ending-card h1{font-family:var(--font-title);font-size:28px;margin:20px 0}.ending-text{white-space:pre-line;line-height:2.1}.ending-after{font-size:12px;color:var(--color-text-muted);margin:30px 0}.restart{width:100%;border:0;background:none;color:var(--color-text-secondary);font:inherit;font-size:12px;margin-top:18px;cursor:pointer}@media(max-width:600px){.ending-card{padding:28px 24px}}</style>
