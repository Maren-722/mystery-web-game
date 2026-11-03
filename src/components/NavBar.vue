<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { currentUser, login, logout as clearUser } from '../game/state.js'
const route=useRoute(),router=useRouter()
const hideNav=computed(() => route.meta.hideNav === true)
const showMenu=ref(false),switchMode=ref(false),loginId=ref(''),loginPwd=ref(''),loginError=ref('')
function closeMenu(){showMenu.value=false;switchMode.value=false;loginError.value='';loginPwd.value=''}
watch(() => route.fullPath,closeMenu)
function logout(){clearUser();closeMenu();if(route.meta.requiresAuth)router.replace('/home')}
function doSwitch(){if(!login(loginId.value,loginPwd.value)){loginError.value='账号或密码错误，请核对网页线索';return}loginId.value='';closeMenu()}
</script>
<template>
  <nav v-if="!hideNav" class="navbar" aria-label="主导航" @keydown.esc="closeMenu">
    <router-link class="navbar-logo" to="/home">南桥夜市</router-link><div class="navbar-links"><router-link to="/home">首页</router-link><router-link to="/stalls">夜市导览</router-link><router-link to="/forum">夜市论坛</router-link><template v-if="currentUser"><router-link to="/messages">私信</router-link><router-link to="/notes">手记</router-link><button class="navbar-user" :aria-expanded="showMenu" aria-controls="account-menu" @click="showMenu=!showMenu">{{ currentUser.displayName }} ▾</button></template><router-link v-else to="/login">登录</router-link></div>
    <div v-if="showMenu" class="menu-mask" @click="closeMenu"></div><section v-if="showMenu" id="account-menu" class="user-menu"><button class="menu-item" @click="switchMode=true">切换账号</button><button class="menu-item menu-danger" @click="logout">退出登录</button><form v-if="switchMode" class="menu-form" @submit.prevent="doSwitch"><label for="switch-id">ID / 用户名</label><input id="switch-id" v-model="loginId" class="form-input" autocomplete="off" required><label for="switch-password">密码</label><input id="switch-password" v-model="loginPwd" type="password" class="form-input" autocomplete="off" required><button class="btn btn-block">登录并切换</button><p v-if="loginError" class="menu-error" role="alert">{{ loginError }}</p></form></section>
  </nav>
</template>
<style scoped>.navbar{background:var(--color-primary);color:#fff;padding:12px 24px;display:flex;align-items:center;justify-content:space-between;gap:16px;position:sticky;top:0;z-index:100;min-height:56px}.navbar-logo{font-family:var(--font-title);font-size:20px;font-weight:700;white-space:nowrap}.navbar-links{display:flex;align-items:center;gap:24px;flex-wrap:wrap}.navbar-links a{font-size:14px}.navbar-links .router-link-active{text-decoration:underline;text-underline-offset:5px}.navbar-user{max-width:180px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;background:#ffffff26;border:0;border-radius:20px;padding:5px 12px;color:white;font:inherit;font-size:13px;cursor:pointer}.menu-mask{position:fixed;inset:0;z-index:150}.user-menu{position:absolute;right:16px;top:calc(100% + 8px);width:270px;max-width:calc(100vw - 32px);background:var(--color-card);border:1px solid var(--color-border);border-radius:var(--radius);padding:10px;box-shadow:0 4px 18px #0002;z-index:200;color:var(--color-text)}.menu-item{width:100%;padding:10px;background:none;border:0;text-align:left;color:var(--color-text);font:inherit;cursor:pointer}.menu-item:hover{background:var(--color-bg)}.menu-danger,.menu-error{color:var(--color-danger)}.menu-form{border-top:1px dashed var(--color-border);padding-top:14px;display:grid;gap:8px}.menu-form label,.menu-error{font-size:12px}@media(max-width:720px){.navbar{align-items:flex-start;flex-direction:column;padding:12px 16px;gap:10px}.navbar-links{gap:14px;width:100%;row-gap:10px}.navbar-links a{font-size:13px}.navbar-user{margin-left:auto}}
</style>
