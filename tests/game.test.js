import test from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { authenticate, normalizeUser, normalizeProgress, normalizeForum, getConversations, getNotes, canConclude, safeRedirect } from '../src/game/rules.js'
const load = name => JSON.parse(readFileSync(new URL(`../src/data/${name}.json`, import.meta.url), 'utf8'))
const accounts=load('accounts'),threads=load('messages'),notes=load('notes'),clues=load('clues'),posts=load('posts'),stalls=load('stalls'),manifest=load('puzzle-clues')

test('six real puzzle credentials replace placeholders and accept display aliases',()=>{
  assert.equal(Object.keys(accounts).length,6)
  for(const [id,a] of Object.entries(accounts)){
    assert.notEqual(a.password,'123456')
    assert.equal(authenticate(accounts,id,a.password),id)
    a.aliases.forEach(name=>assert.equal(authenticate(accounts,name,a.password),id))
    assert.equal(authenticate(accounts,id,'wrong'),null)
  }
  assert.equal(authenticate(accounts,'toString','123456'),null)
})
test('malformed and unknown stored users become guests, valid metadata is canonical',()=>{
  for(const value of [null,[],{},'chenguisheng',{username:'not-a-user'},{username:'__proto__'}]) assert.equal(normalizeUser(value,accounts),null)
  assert.equal(normalizeUser({username:'chennian',shopName:'spoofed'},accounts).displayName,'夜归人')
})
test('shared conversation records show the same ordered history to both participants',()=>{
  const ids=[]
  for(const t of threads){
    assert.equal(new Set(t.participants).size,2)
    const [a,b]=t.participants.map(id=>getConversations(threads,id).find(x=>x.id===t.id))
    assert.deepEqual(a.messages,b.messages)
    assert.deepEqual(a.messages.map(m=>m.at),a.messages.map(m=>m.at).sort())
    t.messages.forEach(m=>{assert.ok(t.participants.includes(m.fromId));ids.push(m.id)})
  }
  assert.equal(ids.length,new Set(ids).size)
  assert.equal(ids.length,61)
})
test('every account has private notes and each clue has exactly one reading source',()=>{
  assert.equal(notes.length,27)
  Object.keys(accounts).forEach(id=>assert.ok(getNotes(notes,id).length>=3))
  notes.forEach(n=>assert.ok(Object.hasOwn(accounts,n.accountId)))
  const evidence=[...notes,...threads.flatMap(t=>t.messages)].map(x=>x.evidenceId).filter(Boolean)
  assert.deepEqual([...evidence].sort(),clues.map(c=>c.id).sort())
  assert.equal(evidence.length,new Set(evidence).size)
})
test('ending is unavailable without all three independent discoveries and explicit choice',()=>{
  assert.equal(canConclude([]),false)
  assert.equal(canConclude(['EV_HOSPITAL','EV_IDENTITY']),false)
  const evidence=['EV_HOSPITAL','EV_LOST_DATE','EV_IDENTITY']
  assert.equal(canConclude(evidence),true)
  assert.deepEqual(normalizeProgress({evidence:['junk','EV_HOSPITAL','EV_HOSPITAL'],ending:'A'},clues),{evidence:['EV_HOSPITAL'],ending:null})
  assert.equal(normalizeProgress({evidence,ending:'B'},clues).ending,'B')
  assert.equal(normalizeProgress({evidence},clues).ending,null)
})
test('each account password has a visible reachable clue and there are no dependency cycles',()=>{
  const reachable=new Set()
  for(let pass=0;pass<6;pass++) for(const c of manifest){
    assert.equal(accounts[c.accountId].password,c.password)
    if(c.sourceType==='stall'){
      const stall=stalls.find(s=>s.id===c.sourceId)
      assert.equal(stall.accountId,c.accountId)
      assert.ok(stall.reviews.length>=2)
      reachable.add(c.accountId)
    } else if(c.sourceType==='notice'){
      const home=readFileSync(new URL('../src/views/Home.vue',import.meta.url),'utf8')
      assert.ok(home.includes('2018年9月1日')&&home.includes('YYYYMMDD'))
      reachable.add(c.accountId)
    } else {
      const n=notes.find(n=>n.id===c.sourceId)
      assert.ok(n.content.includes(c.password))
      if(c.postId)assert.ok(posts.find(p=>p.id===c.postId).comments.some(c=>c.content.includes('纸条背面')))
      if(reachable.has(n.accountId))reachable.add(c.accountId)
    }
  }
  assert.equal(reachable.size,6)
})
test('forum content is complete, NPCs have reviews and public pages do not disclose the son identity',()=>{
  assert.equal(posts.length,15)
  posts.forEach(p=>{assert.ok(p.content&&p.comments);assert.equal(typeof p.preview,'string')})
  stalls.forEach(s=>{assert.ok(s.reviews.length);assert.equal(s.price,`${Math.min(...s.dishes.map(d=>d.price))}元起`);assert.equal('notes' in s,false)})
  assert.ok(!JSON.stringify(posts).includes('夜归人（陈念）'))
})
test('persisted local posts retain detail and comments, while broken records are discarded',()=>{
  const saved={posts:[{id:'local-test',title:'测试',content:'完整正文',author:'李明'},{id:'p1',title:'override',content:'bad',author:'bad'}],comments:{'local-test':[{user:'李明',content:'回复'}],p1:[{user:'李明',content:'线索'},{content:5}],unknown:[{user:'a',content:'b'}]}}
  const result=normalizeForum(saved,posts.map(p=>p.id))
  assert.equal(result.posts.length,1)
  assert.equal(result.posts[0].content,'完整正文')
  assert.equal(result.comments['local-test'].length,1)
  assert.equal(result.comments.p1.length,1)
  assert.equal(result.comments.unknown,undefined)
})
test('login return paths stay within supported game pages',()=>{
  for(const bad of ['https://example.com','//example.com','/ending','/login',['/notes'],null])assert.equal(safeRedirect(bad),'/messages')
  assert.equal(safeRedirect('/forum/p9'),'/forum/p9')
  assert.equal(safeRedirect('/notes'),'/notes')
})
