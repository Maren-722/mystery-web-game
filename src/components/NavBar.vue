<template>
  <nav v-if="!hideNav" class="navbar">
    <div class="navbar-logo" @click="go('/home')">
      <span class="logo-cn">南桥夜市</span>
      <span class="logo-en">NANQIAO NIGHT MARKET</span>
    </div>
    <div class="navbar-links">
      <a :class="{ active: isActive('/home') }" @click="go('/home')">首页</a>
      <a :class="{ active: isActive('/stalls') }" @click="go('/stalls')">夜市导览</a>
      <a :class="{ active: isActive('/forum') }" @click="go('/forum')">夜市论坛</a>
      <template v-if="currentUser && currentUser.role === 'manager'">
        <a :class="{ active: isActive('/manager') }" @click="go('/manager')">管理处</a>
      </template>
      <template v-if="currentUser">
        <a @click="go('/messages')">短信</a>
        <a @click="go('/notes')">我的手记</a>
        <div class="navbar-user-wrap">
          <span class="navbar-user" @click="showMenu = !showMenu">
            {{ currentUser.shopName || currentUser.username }} ▾
          </span>
        </div>
      </template>
      <a v-else @click="go('/login')">登录</a>
      <span
        class="nav-lamp"
        :class="{ lit: progressComplete }"
        @click="goEnding"
      >🏮</span>
    </div>

    <!-- 集齐线索：全屏解锁提示（只弹一次） -->
    <div v-if="showUnlock" class="unlock-mask">
      <div class="unlock-card">
        <span class="unlock-lamp">🏮</span>
        <p class="unlock-text">夜色里，所有的线索都被你串了起来。</p>
        <p class="unlock-text strong">这盏灯，为你亮了。</p>
        <div class="unlock-actions">
          <button class="unlock-btn primary" @click="goEnding">去往结局</button>
          <button class="unlock-btn" @click="stayExploring">继续探索</button>
        </div>
        <p class="unlock-hint">（之后点击导航栏亮起的灯笼，随时可前往结局）</p>
      </div>
    </div>

    <!-- 账号菜单遮罩：点击菜单外关闭 -->
    <div v-if="showMenu" class="menu-mask" @click="closeMenu"></div>

    <!-- 账号下拉菜单 -->
    <div v-if="showMenu" class="user-menu" @click.stop>
      <button class="menu-item" @click="openSwitch">切换账号</button>
      <button class="menu-item menu-danger" @click="logout">退出登录</button>

      <!-- 切换账号表单 -->
      <div v-if="switchMode" class="menu-form">
        <input
          v-model="loginId"
          class="form-input menu-input"
          placeholder="ID"
        >
        <input
          v-model="loginPwd"
          type="password"
          class="form-input menu-input"
          placeholder="密码"
          @keyup.enter="doSwitch"
        >
        <button class="btn btn-block" @click="doSwitch">登录</button>
        <p v-if="loginError" class="menu-error">{{ loginError }}</p>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { matchLogin } from '../utils/auth'
import { isComplete } from '../utils/progress'

const route = useRoute()
const router = useRouter()

const hideNav = ref(route.meta.hideNav === true)

// 当前登录账号：响应式 ref，登录/切换/退出时同步更新
function loadUser() {
  try {
    return JSON.parse(localStorage.getItem('nq_user') || 'null')
  } catch {
    return null
  }
}
const currentUser = ref(loadUser())

// 账号菜单状态
const showMenu = ref(false)
const switchMode = ref(false)
const loginId = ref('')
const loginPwd = ref('')
const loginError = ref('')

// ---------------- 结局灯笼 ----------------
// 灯一直挂在导航栏：未集齐时是暗的，点了没反应；集齐后点亮，可进入结局
const progressComplete = ref(isComplete())
const showUnlock = ref(false)

function onProgressChanged(e) {
  if (e?.detail?.justUnlocked) {
    progressComplete.value = true
    // 集齐后弹一次全屏提示（刷新/重进不再弹）
    if (!localStorage.getItem('nq_ending_prompted')) {
      showUnlock.value = true
    }
  }
}

function goEnding() {
  if (!progressComplete.value) return   // 没集齐：点灯没反应
  localStorage.setItem('nq_ending_prompted', '1')
  showUnlock.value = false
  router.push('/ending')
}

function stayExploring() {
  localStorage.setItem('nq_ending_prompted', '1')
  showUnlock.value = false
}

onMounted(() => {
  window.addEventListener('nq-progress-changed', onProgressChanged)
})
onBeforeUnmount(() => {
  window.removeEventListener('nq-progress-changed', onProgressChanged)
})

function go(path) {
  router.push(path)
}

// 当前页面高亮：首页精确匹配，导览/论坛匹配其详情页
function isActive(path) {
  if (path === '/home') return route.path === '/home'
  return route.path.startsWith(path)
}

function closeMenu() {
  showMenu.value = false
  switchMode.value = false
  loginError.value = ''
}

function openSwitch() {
  switchMode.value = true
  loginError.value = ''
}

// 退出登录：清除登录态，恢复游客模式
function logout() {
  localStorage.removeItem('nq_user')
  currentUser.value = null
  closeMenu()
  loginId.value = ''
  loginPwd.value = ''
  window.dispatchEvent(new CustomEvent('nq-user-changed'))
  // 若在私密页面（短信/手记），跳回首页
  if (route.meta.requiresAuth) {
    router.push('/home')
  }
}

// 切换账号：统一走 matchLogin（剧情账号ID/账号名、玩家用户名/数字ID均可）
function doSwitch() {
  const id = loginId.value.trim()
  const pwd = loginPwd.value.trim()
  if (!id || !pwd) {
    loginError.value = '请输入ID和密码'
    return
  }
  const result = matchLogin(id, pwd)
  if (result && result.ok) {
    localStorage.setItem('nq_user', JSON.stringify({
      username: result.username,
      shopName: result.shopName,
      role: result.role
    }))
    currentUser.value = { username: result.username, shopName: result.shopName, role: result.role }
    closeMenu()
    loginId.value = ''
    loginPwd.value = ''
    window.dispatchEvent(new CustomEvent('nq-user-changed'))
  } else {
    loginError.value = 'ID或密码错误，请重试'
  }
}
</script>

<style scoped>
.navbar {
  background: var(--ink);
  color: #EFE6D6;
  padding: 0 28px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 24px;
  height: 64px;
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid rgba(215, 154, 74, 0.18);
}
.navbar-logo {
  display: flex;
  flex-direction: column;
  gap: 3px;
  cursor: pointer;
  user-select: none;
  flex-shrink: 0;
}
.logo-cn {
  font-family: var(--font-title);
  font-size: 20px;
  font-weight: 600;
  letter-spacing: 4px;
  line-height: 1;
  color: #F6EEDF;
}
.logo-en {
  font-size: 8px;
  letter-spacing: 2.6px;
  line-height: 1;
  color: rgba(215, 154, 74, 0.85);
}
.navbar-links {
  display: flex;
  gap: 22px;
  align-items: center;
  overflow-x: auto;
  scrollbar-width: none;
}
.navbar-links::-webkit-scrollbar {
  display: none;
}
.navbar-links a {
  position: relative;
  color: #CBC2B3;
  font-size: 13px;
  letter-spacing: 0.8px;
  cursor: pointer;
  padding: 8px 1px;
  white-space: nowrap;
  transition: color 0.2s;
}
.navbar-links a:hover {
  color: #F3E7D2;
}
/* 当前所在页面：暖色字 + 下划线 */
.navbar-links a.active {
  color: var(--amber-soft);
}
.navbar-links a.active::after {
  content: '';
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  height: 1.5px;
  background: var(--amber);
}
.navbar-user-wrap {
  position: relative;
}
.navbar-user {
  border: 1px solid rgba(215, 154, 74, 0.42);
  color: #EADFCB;
  padding: 5px 12px;
  border-radius: 2px;
  font-size: var(--font-tiny);
  letter-spacing: 0.5px;
  cursor: pointer;
  user-select: none;
  white-space: nowrap;
  transition: background 0.2s, border-color 0.2s;
}
.navbar-user:hover {
  background: rgba(215, 154, 74, 0.12);
  border-color: rgba(215, 154, 74, 0.7);
}

/* 菜单遮罩：点击任意外部区域关闭 */
.menu-mask {
  position: fixed;
  inset: 0;
  z-index: 150;
}
/* 账号下拉菜单 */
.user-menu {
  position: absolute;
  right: 0;
  top: calc(100% + 10px);
  background: var(--color-card);
  border: 1px solid var(--color-border);
  border-radius: var(--radius);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
  min-width: 220px;
  padding: 8px;
  z-index: 200;
}
.menu-item {
  display: block;
  width: 100%;
  text-align: left;
  background: none;
  border: none;
  padding: 8px 10px;
  font-size: var(--font-body-size);
  color: var(--color-text);
  font-family: var(--font-body);
  border-radius: var(--radius);
  cursor: pointer;
  transition: background 0.15s;
}
.menu-item:hover {
  background: var(--color-bg);
}
.menu-danger {
  color: var(--color-danger);
}
.menu-form {
  border-top: 1px dashed var(--color-border);
  margin-top: 8px;
  padding-top: 10px;
  display: grid;
  gap: 8px;
}
.menu-input {
  font-size: 14px;
  padding: 8px 10px;
}
.menu-error {
  color: var(--color-danger);
  font-size: var(--font-tiny);
  text-align: center;
}

/* 结局灯笼：一直是暗的，集齐后点亮 */
.nav-lamp {
  font-size: 20px;
  cursor: pointer;
  user-select: none;
  line-height: 1;
  filter: grayscale(1) brightness(0.75);
  opacity: 0.45;
  transition: filter 0.6s, opacity 0.6s, text-shadow 0.6s;
}
.nav-lamp.lit {
  filter: none;
  opacity: 1;
  animation: lampGlow 2.4s ease-in-out infinite;
}
@keyframes lampGlow {
  0%, 100% { text-shadow: 0 0 4px rgba(255, 190, 92, 0.6); }
  50% { text-shadow: 0 0 14px rgba(255, 190, 92, 1); }
}

/* 集齐线索的全屏解锁提示 */
.unlock-mask {
  position: fixed;
  inset: 0;
  background: radial-gradient(ellipse at center, rgba(30, 24, 16, 0.92), rgba(10, 8, 5, 0.97));
  z-index: 2000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}
.unlock-card {
  max-width: 440px;
  width: 100%;
  text-align: center;
}
.unlock-lamp {
  display: block;
  font-size: 56px;
  margin-bottom: 20px;
  animation: lampGlow 2.4s ease-in-out infinite;
}
.unlock-text {
  color: #d8cfc2;
  font-size: 16px;
  line-height: 2;
  margin-bottom: 6px;
}
.unlock-text.strong {
  color: #ffcf8a;
  font-size: 19px;
  font-weight: 600;
  font-family: var(--font-title);
  margin-bottom: 26px;
}
.unlock-actions {
  display: flex;
  gap: 14px;
  justify-content: center;
  margin-bottom: 18px;
}
.unlock-btn {
  flex: 1;
  max-width: 160px;
  padding: 12px;
  border-radius: 8px;
  border: 1px solid rgba(255, 207, 138, 0.5);
  background: transparent;
  color: #ffcf8a;
  font-size: 15px;
  font-family: var(--font-body);
  cursor: pointer;
  transition: background 0.2s;
}
.unlock-btn:hover {
  background: rgba(255, 207, 138, 0.12);
}
.unlock-btn.primary {
  background: rgba(255, 190, 92, 0.9);
  color: #241a0e;
  border: none;
  font-weight: 600;
}
.unlock-btn.primary:hover {
  background: rgba(255, 190, 92, 1);
}
.unlock-hint {
  color: #8a7f6f;
  font-size: 12px;
}

@media (max-width: 720px) {
  .navbar {
    padding: 0 14px;
    height: 58px;
    gap: 12px;
  }
  .logo-cn {
    font-size: 17px;
    letter-spacing: 2px;
  }
  .logo-en {
    display: none;
  }
  .navbar-links {
    gap: 14px;
    justify-content: flex-end;
  }
  .navbar-links a {
    font-size: var(--font-tiny);
    letter-spacing: 0;
  }
  .navbar-user {
    padding: 4px 8px;
  }
  .user-menu {
    position: fixed;
    right: var(--space-md);
    top: 64px;
  }
}
</style>
