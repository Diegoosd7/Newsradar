<template>
	<AppHeader />
	<div class="user-view">
		<AppNavbar role="GESTOR" />
		<RouterView class="content" />
	</div>
</template>

<script setup lang="ts">
import AppHeader from "./layouts/AppHeader.vue";
import AppNavbar from "./layouts/AppNavbar.vue";
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
