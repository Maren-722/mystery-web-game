<template>
  <router-view />
  <p v-if="!storageAvailable" class="storage-notice" role="status">浏览器未允许保存数据，本次仍可游玩，关闭页面后进度可能丢失。</p>
</template>

<script setup>
import { watch } from 'vue'
import { useRouter } from 'vue-router'
import { currentUser, storageAvailable } from './game/state.js'
const router = useRouter()
watch(currentUser, user => {
  const route = router.currentRoute.value
  if (!user && route.meta.requiresAuth) router.replace({ name: 'login', query: { redirect: route.fullPath } })
}, { flush: 'sync' })
// 根组件：只做路由出口
// 开场页（Intro）不需要导航栏，其他页面由各自视图决定布局
</script>
