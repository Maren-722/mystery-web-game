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
  border-top: 1px solid var(--color-border);
  padding: var(--space-lg);
  text-align: center;
  color: var(--color-text-secondary);
  font-size: var(--font-small);
}
.footer-small {
  margin-top: var(--space-xs);
  font-size: var(--font-tiny);
  color: var(--color-text-muted);
}
</style>
