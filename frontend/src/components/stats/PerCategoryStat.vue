<template>
	<div class="per-category-stat">
		<p class="title">{{ title }}</p>
	</div>
</template>

<script setup lang="ts">
type Props = { title: string };
const props = defineProps<Props>();
</script>

<style scoped>
.per-category-stat {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	border: 2px solid var(--black);
	padding: 1rem;
}
</style>
