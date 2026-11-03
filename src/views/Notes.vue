<script setup>
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import Footer from '../components/Footer.vue'
import EvidenceBook from '../components/EvidenceBook.vue'
import { notes, currentUser, markNoteRead, readyForEnding, chooseEnding } from '../game/state.js'
import { getNotes } from '../game/rules.js'
const router = useRouter()
const selectedId = ref(null)
const list = computed(() => getNotes(notes, currentUser.value?.username))
const active = computed(() => list.value.find(n => n.id === selectedId.value))
watch(() => currentUser.value?.username, () => { selectedId.value = null })
function open(n) { selectedId.value = n.id; markNoteRead(n.id) }
function decide(choice) { if (chooseEnding(choice)) router.push('/ending') }
</script>
<template>
  <div class="page-shell"><NavBar /><div class="container private-container">
    <h1 class="section-title">我的手记</h1><p class="page-desc">{{ currentUser?.displayName }}留下的备忘、草稿与没说出口的话。</p>
    <EvidenceBook />
    <div class="account-layout">
      <aside class="account-list" aria-label="手记列表"><button v-for="n in list" :key="n.id" @click="open(n)" :aria-current="n.id === selectedId"><strong>{{ n.title }}</strong><small>{{ n.at }} · {{ n.kind }}</small></button></aside>
      <section class="account-reader" aria-live="polite"><article v-if="active" class="private-note"><p class="note-kind">{{ active.kind }}</p><h2>{{ active.title }}</h2><time>{{ active.at }}</time><p class="note-body">{{ active.content }}</p></article><div v-else class="account-empty"><h2>翻开一篇手记</h2><p>这里记下的，往往没有告诉别人。</p></div></section>
    </div>
    <section v-if="readyForEnding && currentUser?.username === 'chennian'" class="decision card">
      <h2>这一次，你知道他在哪</h2><p>住院地址、二十八年前的日期、那封没发出的私信，已经能够拼在一起。夜归人还在等一条回复。</p>
      <button class="btn" @click="decide('A')">把住院地址告诉他</button><button class="btn btn-secondary" @click="decide('B')">暂时不发出这条消息</button>
    </section>
  </div><Footer /></div>
</template>
<style scoped>.decision{margin-top:24px}.decision h2{font-family:var(--font-title);font-size:var(--font-h2)}.decision p{margin:16px 0;line-height:1.9}.decision button{margin:0 10px 10px 0}.btn-secondary{background:var(--color-card);color:var(--color-primary);border:1px solid var(--color-border)}</style>
