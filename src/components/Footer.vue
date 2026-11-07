<template>
  <footer v-if="!hideNav" class="footer">
    <p>南桥夜市 · 临岗市江边 · 营业时间 17:00-23:00</p>
    <p class="footer-small">夜市管理处维护 · 有问题请联系管理处王主任</p>
  </footer>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const hideNav = computed(() => route.meta.hideNav === true)
</script>

<style scoped>
.footer {
  background: var(--ink);
  border-top: 1px solid rgba(215, 154, 74, 0.14);
  padding: 30px 24px;
  text-align: center;
  color: #A79C8B;
  font-size: var(--font-tiny);
  letter-spacing: 0.8px;
}
.footer-small {
  margin-top: 6px;
  font-size: 11px;
  color: rgba(167, 156, 139, 0.6);
}
</style>
