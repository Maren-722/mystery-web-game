<template>
  <div class="ending-page">
    <!-- 未集齐：灯还没亮，故事没到说再见的时候 -->
    <div v-if="!unlocked" class="ending-card">
      <span class="ending-lamp dim">🏮</span>
      <p class="blocked-text">灯还没亮。</p>
      <p class="blocked-sub">夜市的故事，还没到说再见的时候。</p>
      <hr class="ending-divider">
      <button class="ending-btn" @click="$router.push('/home')">回到夜市</button>
    </div>

    <!-- 已集齐：结局 -->
    <div v-else class="ending-card">
      <span class="ending-tag">结 局</span>
      <h1 class="ending-title">第五站，梧桐苑</h1>
      <p class="ending-text">
        你把所有的碎片拼在了一起。
      </p>
      <p class="ending-text">
        2006年8月16日，城南老街，四岁的陈念走失，手腕上系着一根绣着「念」字的红绳。之后的二十年，父亲陈桂生守着同一个夜市、同一口锅，住在同一间老屋里——他不敢搬家，怕儿子回来找不到家门。
      </p>
      <p class="ending-text">
        今年秋天，儿子回来了。他就在离父亲三米远的地方，喝了一碗觉得"特别亲切"的糖粥藕。他把红绳递过去，父亲低头搅着粥，说：不认得。
      </p>
      <p class="ending-text">
        十月，陈伯查出了病。他在手记里写：认了，让他守着我走吗？他丢了二十年，回来就为了送我？——他不肯。
      </p>
      <p class="ending-text">
        10月26日傍晚，他把最后一锅粥分给了街坊，把灶台擦得锃亮，给王主任留了张纸条。然后他拎着那口大锅，走进了南桥站的夜风里。<br>往城南方向，第五站，梧桐苑。
      </p>
      <p class="ending-text">
        那栋小楼的灯，还亮着。
      </p>
      <p class="ending-text">
        ——而此刻，屏幕前有个年轻人，手腕上系着一根褪色的红绳，正在论坛里一遍遍刷新同一个问题：<br>"陈伯去哪了？"
      </p>
      <p class="ending-text ending-last">
        也许明天，会有人去敲那扇门。
      </p>
      <hr class="ending-divider">
      <button class="ending-btn" @click="$router.push('/home')">再回夜市看看</button>
      <button class="ending-btn ghost" @click="restart">重新开始</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { isComplete } from '../utils/progress'

// 结局页守卫：线索没有集齐时，直接访问只会看到"灯还没亮"
const unlocked = ref(isComplete())

function restart() {
  localStorage.removeItem('nq_progress')
  localStorage.removeItem('nq_ending_prompted')
  localStorage.removeItem('nq_user')
  localStorage.removeItem('nq_notes')
  localStorage.removeItem('nq_posts')
  localStorage.removeItem('nq_comments')
  window.dispatchEvent(new CustomEvent('nq-user-changed'))
  window.location.href = `${window.location.pathname}#/`
  window.location.reload()
}
</script>

<style scoped>
.ending-page {
  min-height: 100vh;
  background: #1a1a2e;
  color: #e0e0e0;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 20px;
}
.ending-card {
  max-width: 600px;
  width: 100%;
  background: #16213e;
  border-radius: 12px;
  padding: 48px 40px;
  border: 1px solid #0f3460;
}
.ending-tag {
  display: inline-block;
  background: #e94560;
  color: #fff;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  margin-bottom: 24px;
}
.ending-title {
  font-family: var(--font-title);
  font-size: 28px;
  color: #fff;
  margin-bottom: 20px;
  line-height: 1.4;
}
.ending-text {
  font-size: 15px;
  line-height: 2;
  color: #b8b8b8;
  margin-bottom: 14px;
}
.ending-last {
  color: #ffcf8a;
  font-weight: 600;
}
.ending-divider {
  border: none;
  border-top: 1px solid #0f3460;
  margin: 32px 0;
}
.ending-btn {
  display: block;
  width: 100%;
  padding: 14px;
  background: transparent;
  color: #e94560;
  border: 1px solid #e94560;
  border-radius: 8px;
  font-size: 14px;
  cursor: pointer;
  font-family: var(--font-body);
  transition: background 0.2s;
  margin-bottom: 10px;
}
.ending-btn:hover {
  background: rgba(233, 69, 96, 0.15);
}
.ending-btn.ghost {
  color: #7a8bb8;
  border-color: #2a3f6f;
}
.ending-btn.ghost:hover {
  background: rgba(122, 139, 184, 0.12);
}

/* 未解锁的挡板页 */
.ending-lamp {
  display: block;
  text-align: center;
  font-size: 44px;
  margin-bottom: 20px;
}
.ending-lamp.dim {
  filter: grayscale(1) brightness(0.75);
  opacity: 0.45;
}
.blocked-text {
  text-align: center;
  font-family: var(--font-title);
  font-size: 22px;
  color: #d8cfc2;
  margin-bottom: 8px;
}
.blocked-sub {
  text-align: center;
  font-size: 14px;
  color: #8a8a8a;
}
</style>
