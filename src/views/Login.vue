<template>
  <div class="login-page">
    <NavBar />
    <div class="login-container">
      <BackBar label="返回首页" fallback="/home" />
      <h1 class="login-title">账号登录</h1>
      <p class="login-subtitle">登录后可查看私信、手记和管理店铺信息</p>

      <div class="form-group">
        <label class="form-label">ID / 用户名</label>
        <input
          type="text"
          class="form-input"
          v-model="username"
          placeholder="请输入用户名"
          @keyup.enter="handleLogin"
        >
      </div>
      <div class="form-group">
        <label class="form-label">密码</label>
        <input
          type="password"
          class="form-input"
          v-model="password"
          placeholder="请输入密码"
          @keyup.enter="handleLogin"
        >
      </div>

      <button class="btn btn-primary btn-block" @click="handleLogin">登 录</button>
      <div class="login-error" v-if="errorMsg">{{ errorMsg }}</div>
    </div>
    <Footer />
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import Footer from '../components/Footer.vue'
import BackBar from '../components/BackBar.vue'
import accounts from '../data/accounts.json'

const router = useRouter()
const route = useRoute()

const username = ref('')
const password = ref('')
const errorMsg = ref('')

// 登录逻辑：账号密码对照表在 src/data/accounts.json（队友C维护）
// 登录成功：写入 localStorage，跳转到私信页
function handleLogin() {
  const uname = username.value.trim()
  const pwd = password.value.trim()

  if (!uname || !pwd) {
    errorMsg.value = '请输入用户名和密码'
    return
  }

  const account = accounts[uname]
  if (account && account.password === pwd) {
    errorMsg.value = ''
    localStorage.setItem('nq_user', JSON.stringify({
      username: uname,
      shopName: account.shopName || uname
    }))
    router.push(route.query.redirect || '/messages')
  } else {
    errorMsg.value = '用户名或密码错误，请重试'
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
.login-container {
  max-width: 400px;
  width: 100%;
  margin: 60px auto;
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  padding: var(--space-xl);
  flex: 1;
}
.login-title {
  font-family: var(--font-title);
  font-size: var(--font-h1);
  text-align: center;
  margin-bottom: var(--space-sm);
}
.login-subtitle {
  font-size: var(--font-small);
  color: var(--color-text-secondary);
  text-align: center;
  margin-bottom: var(--space-xl);
}
.form-group {
  margin-bottom: var(--space-md);
}
.login-error {
  color: var(--color-danger);
  font-size: var(--font-small);
  margin-top: var(--space-md);
  text-align: center;
}

@media (max-width: 720px) {
  .login-container {
    margin: 24px auto;
    padding: var(--space-lg);
  }
}
</style>
