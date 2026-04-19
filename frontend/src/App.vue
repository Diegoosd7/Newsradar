<template>
	<AppHeader />
	<div class="user-view">
		<AppNavbar v-if="auth.isAuthenticated" :role="auth.role" @logout="handleLogout" />
		<RouterView class="content" />
	</div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import AppHeader from './layouts/AppHeader.vue'
import AppNavbar from './layouts/AppNavbar.vue'
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()
const router = useRouter()

const handleLogout = () => {
	auth.logout()
	router.push({ name: 'login' })
}
</script>

<style scoped>
.user-view {
	display: flex;
	height: 100%;
	width: 100%;
}

.content {
	overflow: auto;
	max-height: 100%;
	padding: 1rem;
	width: 100%;
}
</style>
