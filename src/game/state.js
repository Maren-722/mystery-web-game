import { computed, ref } from 'vue'
import accounts from '../data/accounts.json'
import threads from '../data/messages.json'
import notes from '../data/notes.json'
import clues from '../data/clues.json'
import seedPosts from '../data/posts.json'
import { authenticate, normalizeUser, normalizeProgress, normalizeForum, canConclude } from './rules.js'

export const storageAvailable = ref(true)
function read(key) {
  try { return JSON.parse(localStorage.getItem(key) || 'null') } catch { return null }
}
function write(key, value) {
  try { if (value === null) localStorage.removeItem(key); else localStorage.setItem(key, JSON.stringify(value)) }
  catch { storageAvailable.value = false }
}
export const currentUser = ref(normalizeUser(read('nq_user'), accounts))
export const progress = ref(normalizeProgress(read('nq_progress_v1'), clues))
const forum = ref(normalizeForum(read('nq_forum_v1'), seedPosts.map(p => p.id)))
export const readyForEnding = computed(() => canConclude(progress.value.evidence))

export function login(username, password) {
  const id = authenticate(accounts, username, password)
  if (!id) return false
  currentUser.value = normalizeUser({ username: id }, accounts)
  write('nq_user', currentUser.value)
  return true
}
export function logout() { currentUser.value = null; write('nq_user', null) }

export function recordEvidence(id) {
  if (!clues.some(c => c.id === id) || progress.value.evidence.includes(id)) return
  progress.value.evidence.push(id)
  write('nq_progress_v1', progress.value)
}
export function markConversationRead(id) {
  const t = threads.find(t => t.id === id && t.participants.includes(currentUser.value?.username))
  t?.messages.forEach(m => recordEvidence(m.evidenceId))
}
export function markNoteRead(id) {
  const n = notes.find(n => n.id === id && n.accountId === currentUser.value?.username)
  if (n) recordEvidence(n.evidenceId)
}
export function chooseEnding(choice) {
  if (!readyForEnding.value || currentUser.value?.username !== 'chennian' || !['A', 'B'].includes(choice)) return false
  progress.value.ending = choice
  write('nq_progress_v1', progress.value)
  return true
}
export function resetGame() {
  logout()
  progress.value = { evidence: [], ending: null }
  forum.value = { posts: [], comments: {} }
  write('nq_progress_v1', null); write('nq_forum_v1', null); write('nq_ending', null)
}

export const posts = computed(() => [...forum.value.posts, ...seedPosts].map(p => ({
  ...p, comments: [...(p.comments || []), ...(forum.value.comments[p.id] || [])]
})))
export function publishPost(title, content) {
  if (!currentUser.value || !title.trim() || !content.trim()) return null
  const p = { id: `local-${crypto.randomUUID()}`, title: title.trim().slice(0,80), content: content.trim().slice(0,5000), author: currentUser.value.displayName, authorId: currentUser.value.username, date: '刚刚', preview: content.trim().slice(0,70), comments: [] }
  forum.value.posts.unshift(p)
  write('nq_forum_v1', forum.value)
  return p.id
}
export function addComment(postId, content) {
  if (!currentUser.value || !content.trim() || !posts.value.some(p => p.id === postId)) return false
  ;(forum.value.comments[postId] ||= []).push({ id: crypto.randomUUID(), user: currentUser.value.displayName, date: '刚刚', content: content.trim().slice(0,2000) })
  write('nq_forum_v1', forum.value)
  return true
}

window.addEventListener('storage', event => {
  if (event.key === 'nq_user' || event.key === null) currentUser.value = normalizeUser(read('nq_user'), accounts)
  if (event.key === 'nq_progress_v1' || event.key === null) progress.value = normalizeProgress(read('nq_progress_v1'), clues)
  if (event.key === 'nq_forum_v1' || event.key === null) forum.value = normalizeForum(read('nq_forum_v1'), seedPosts.map(p => p.id))
})

export { accounts, threads, notes, clues }
