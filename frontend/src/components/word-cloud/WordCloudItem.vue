<template>
	<div class="word-cloud-item">
		<p class="title">{{ props.title }}</p>
	</div>
</template>

<script setup lang="ts">
type Props = { title: string };
const props = defineProps<Props>();
</script>

<style scoped>
.word-cloud-item {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	border: 2px solid var(--black);
	padding: 1rem;
}
</style>
