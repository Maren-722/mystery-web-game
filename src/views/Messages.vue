<script setup>
import { computed, ref, watch } from 'vue'
import NavBar from '../components/NavBar.vue'
import Footer from '../components/Footer.vue'
import EvidenceBook from '../components/EvidenceBook.vue'
import { accounts, threads, currentUser, markConversationRead } from '../game/state.js'
import { getConversations } from '../game/rules.js'
const selectedId = ref(null)
const conversations = computed(() => getConversations(threads, currentUser.value?.username))
const active = computed(() => conversations.value.find(t => t.id === selectedId.value))
const otherName = t => accounts[t.participants.find(id => id !== currentUser.value?.username)]?.displayName
watch(() => currentUser.value?.username, () => { selectedId.value = null })
function open(t) { selectedId.value = t.id; markConversationRead(t.id) }
</script>
<template>
  <div class="page-shell"><NavBar /><div class="container private-container">
    <h1 class="section-title">私信记录</h1>
    <p class="page-desc">{{ currentUser?.displayName }}的历史会话。收摊以后，有些话只留在这里。</p>
    <EvidenceBook />
    <div class="account-layout">
      <aside class="account-list" aria-label="会话列表">
        <button v-for="t in conversations" :key="t.id" @click="open(t)" :aria-current="t.id === selectedId">
          <strong>{{ otherName(t) }}</strong><small>{{ t.messages.at(-1).at }}</small><span>{{ t.messages.at(-1).content }}</span>
        </button>
      </aside>
      <section class="account-reader" aria-live="polite">
        <template v-if="active"><header class="reader-header"><h2>与{{ otherName(active) }}的对话</h2><p>历史记录 · 按发送时间排列</p></header>
          <div class="chat-history"><article v-for="m in active.messages" :key="m.id" class="chat-message" :class="{mine:m.fromId === currentUser?.username}">
            <p class="chat-meta">{{ accounts[m.fromId].displayName }} · <time>{{ m.at }}</time></p><p class="chat-bubble">{{ m.content }}</p>
          </article></div>
        </template>
        <div v-else class="account-empty"><h2>选择一段会话</h2><p>关于那一晚，每个人都记得一部分。</p></div>
      </section>
    </div>
  </div><Footer /></div>
</template>
