<template>
  <nav v-if="!hideNav" class="navbar">
    <div class="navbar-logo" @click="go('/home')">南桥夜市</div>
    <div class="navbar-links">
      <a @click="go('/home')">首页</a>
      <a @click="go('/stalls')">夜市导览</a>
      <a @click="go('/forum')">夜市论坛</a>
      <template v-if="currentUser">
        <a @click="go('/messages')">短信</a>
        <a @click="go('/notes')">我的手记</a>
        <span class="navbar-user">{{ currentUser.shopName || currentUser.username }}</span>
      </template>
      <a v-else @click="go('/login')">登录</a>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const hideNav = computed(() => route.meta.hideNav === true)

// 从 localStorage 读取当前登录账号
const currentUser = computed(() => {
  try {
    return JSON.parse(localStorage.getItem('nq_user') || 'null')
  } catch {
    return null
  }
})

function go(path) {
  router.push(path)
}
</script>

<style scoped>
.navbar {
  background: var(--color-primary);
  color: #fff;
  padding: 0 var(--space-lg);
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 56px;
  position: sticky;
  top: 0;
  z-index: 100;
}
.navbar-logo {
  font-family: var(--font-title);
  font-size: 20px;
  font-weight: 700;
  cursor: pointer;
}
.navbar-links {
  display: flex;
  gap: var(--space-lg);
  align-items: center;
}
.navbar-links a {
  color: #fff;
  font-size: var(--font-body-size);
  opacity: 0.9;
  cursor: pointer;
}
.navbar-links a:hover {
  opacity: 1;
}
.navbar-user {
  background: rgba(255, 255, 255, 0.15);
  padding: 4px 12px;
  border-radius: 20px;
  font-size: var(--font-small);
}

@media (max-width: 720px) {
  .navbar {
    padding: 0 var(--space-md);
  }
  .navbar-links {
    gap: var(--space-sm);
  }
  .navbar-links a {
    font-size: var(--font-small);
  }
}
</style>
