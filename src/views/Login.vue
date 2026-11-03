<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import NavBar from '../components/NavBar.vue'
import Footer from '../components/Footer.vue'
import BackBar from '../components/BackBar.vue'
import { login } from '../game/state.js'
import { safeRedirect } from '../game/rules.js'
const route=useRoute(), router=useRouter()
const username=ref(''), password=ref(''), errorMsg=ref('')
function handleLogin() {
  if (!username.value.trim() || !password.value.trim()) { errorMsg.value='请输入用户名和密码'; return }
  if (!login(username.value,password.value)) { errorMsg.value='用户名或密码错误，请核对线索中的日期与位数'; return }
  errorMsg.value=''; password.value=''; router.push(safeRedirect(route.query.redirect))
}
</script>
<template>
  <div class="page-shell"><NavBar /><main class="login-container card">
    <BackBar label="返回首页" fallback="/home" /><h1>账号登录</h1><p class="page-desc">输入夜市人物的ID与密码，查看该账号的私信和手记。</p>
    <form @submit.prevent="handleLogin"><label for="login-id" class="form-label">ID / 用户名</label><input id="login-id" v-model="username" class="form-input" autocomplete="off" placeholder="人物姓名、商户名称或账号ID" required>
      <label for="login-pwd" class="form-label">密码</label><input id="login-pwd" v-model="password" class="form-input" type="password" autocomplete="off" placeholder="从网页线索中推理密码" required>
      <button class="btn btn-block" type="submit">登录</button><p class="login-error" role="alert">{{ errorMsg }}</p>
    </form><p class="login-help">账号ID可在商户名片和论坛中找到。日期线索要留意是否包含年份。</p>
  </main><Footer /></div>
</template>
<style scoped>.login-container{width:calc(100% - 32px);max-width:430px;margin:44px auto;padding:32px}.login-container h1{font-family:var(--font-title);font-size:var(--font-h1);margin:12px 0}.form-label{margin-top:20px}.btn{margin-top:24px}.login-error{color:var(--color-danger);font-size:13px;margin-top:12px;min-height:22px}.login-help{font-size:12px;color:var(--color-text-muted);margin-top:18px;line-height:1.8}</style>
