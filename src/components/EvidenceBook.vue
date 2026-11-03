<script setup>
import { computed } from 'vue'
import { progress, clues, readyForEnding, currentUser } from '../game/state.js'
const found = computed(() => clues.filter(c => progress.value.evidence.includes(c.id)))
</script>
<template>
  <details class="evidence-book">
    <summary>调查笔记 · 已找到 {{ found.length }} 条线索</summary>
    <ul v-if="found.length"><li v-for="clue in found" :key="clue.id">{{ clue.label }}</li></ul>
    <p v-else>打开人物的会话或手记后，关键发现会记在这里。</p>
    <p v-if="readyForEnding && currentUser?.username !== 'chennian'">线索已经能够拼起来了。回到夜归人的账号，看看他还在等什么。</p>
  </details>
</template>
<style scoped>
.evidence-book{border:1px solid var(--color-border);background:var(--color-card);padding:14px 18px;margin-bottom:20px;border-radius:var(--radius);font-size:var(--font-small);color:var(--color-text-secondary)}summary{cursor:pointer;color:var(--color-primary)}ul{margin-top:12px;display:grid;gap:6px}li::before{content:'· ';color:var(--color-accent)}p{margin-top:12px}
</style>
