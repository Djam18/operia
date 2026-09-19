<template>
  <div class="overflow-x-auto rounded-xl border border-slate-200/80 bg-white">
    <table class="w-full text-left text-xs border-collapse">
      <thead v-if="$slots.header" class="bg-slate-50 border-b border-slate-200/80 text-slate-500 font-semibold uppercase text-[10px] tracking-wider">
        <slot name="header" />
      </thead>
      <tbody class="divide-y divide-slate-100 text-slate-700">
        <slot />
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
// Clean reusable table wrapper
</script>
