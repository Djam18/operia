<template>
  <div v-if="$route.path === '/console'" class="min-h-screen bg-[#0B0F17] text-slate-100 font-sans">
    <router-view />
  </div>
  <div v-else-if="$route.path === '/login'" class="min-h-screen bg-[#F8FAFC]">
    <router-view />
  </div>
  <div v-else class="flex min-h-screen bg-[#F8FAFC]">
    <Sidebar />
    <main class="flex-1 overflow-y-auto">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import Sidebar from './components/Sidebar.vue'
</script>
