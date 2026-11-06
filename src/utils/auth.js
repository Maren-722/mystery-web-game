// 当前登录态的响应式共享（解决"切换账号后必须刷新页面"的问题）
// ------------------------------------------------------------
// localStorage 不是响应式数据源，直接在 computed 里读会在切换账号后拿到缓存的旧值。
// 这里统一用 ref + 'nq-user-changed' 事件（NavBar 登录/切换/退出时派发）来同步。
// 用法：const { currentUser, readUser, syncUser } = useCurrentUser()
// ------------------------------------------------------------
import { ref, onMounted, onBeforeUnmount } from 'vue'
import accounts from '../data/accounts.json'

export function readUser() {
  try {
    return JSON.parse(localStorage.getItem('nq_user') || 'null')
  } catch {
    return null
  }
}

export function useCurrentUser() {
  const currentUser = ref(readUser())

  function syncUser() {
    currentUser.value = readUser()
  }

  onMounted(() => {
    window.addEventListener('nq-user-changed', syncUser)
  })
  onBeforeUnmount(() => {
    window.removeEventListener('nq-user-changed', syncUser)
  })

  return { currentUser, readUser, syncUser }
}

// 按 ID 查找剧情账号：商户 ID 是人名（导览里可见），游客 ID 是长数字（论坛发言旁可见）
// 兼容直接用账号名（玩家注册的自定义账号仍以用户名登录）
export function findAccountById(id) {
  const byUid = Object.keys(accounts).find(k => accounts[k].uid === id)
  if (byUid) return { username: byUid, ...accounts[byUid] }
  if (accounts[id]) return { username: id, ...accounts[id] }
  return null
}
