export const REQUIRED_EVIDENCE = ['EV_HOSPITAL', 'EV_LOST_DATE', 'EV_IDENTITY']

export function authenticate(accounts, username, password) {
  const name = String(username ?? '').trim()
  const pwd = String(password ?? '').trim()
  return Object.entries(accounts).find(([id, a]) =>
    [id, ...(a.aliases || [])].includes(name) && a.password === pwd
  )?.[0] ?? null
}

export function normalizeUser(value, accounts) {
  if (!value || typeof value !== 'object' || !Object.hasOwn(accounts, value.username)) return null
  const a = accounts[value.username]
  return { username: value.username, displayName: a.displayName, shopName: a.shopName, role: a.role }
}

export function normalizeProgress(value, clues) {
  const known = new Set(clues.map(c => c.id))
  const evidence = Array.isArray(value?.evidence) ? [...new Set(value.evidence.filter(id => known.has(id)))] : []
  const ready = REQUIRED_EVIDENCE.every(id => evidence.includes(id))
  return { evidence, ending: ready && ['A', 'B'].includes(value?.ending) ? value.ending : null }
}

export function canConclude(evidence) {
  return REQUIRED_EVIDENCE.every(id => evidence.includes(id))
}

export function getConversations(threads, accountId) {
  return threads.filter(t => t.participants.includes(accountId)).map(t => ({
    ...t, messages: [...t.messages].sort((a, b) => a.at.localeCompare(b.at))
  }))
}

export function getNotes(notes, accountId) {
  return notes.filter(n => n.accountId === accountId).sort((a, b) => a.at.localeCompare(b.at))
}

export function safeRedirect(value) {
  if (typeof value !== 'string' || !/^\/(messages|notes|forum|stalls)(\/[^?#]*)?(\?[^#]*)?$/.test(value)) return '/messages'
  return value
}

export function normalizeForum(value, seedIds) {
  const posts = Array.isArray(value?.posts) ? value.posts.filter(p =>
    p && typeof p.id === 'string' && p.id.startsWith('local-') && !seedIds.includes(p.id) &&
    typeof p.title === 'string' && typeof p.content === 'string' && typeof p.author === 'string'
  ).map(p => ({ ...p, title: p.title.slice(0, 80), content: p.content.slice(0, 5000), comments: [] })) : []
  const comments = {}
  if (value?.comments && typeof value.comments === 'object') {
    for (const [id, list] of Object.entries(value.comments)) {
      if (!seedIds.includes(id) && !posts.some(p => p.id === id)) continue
      comments[id] = Array.isArray(list) ? list.filter(c => c && typeof c.content === 'string' && typeof c.user === 'string').map(c => ({ ...c, content: c.content.slice(0, 2000) })) : []
    }
  }
  return { posts, comments }
}
