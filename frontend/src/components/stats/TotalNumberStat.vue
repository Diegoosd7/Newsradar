<template>
	<div class="total-number-stat">
		<p class="title">{{ title }}</p>
		<p class="number">{{ number }}</p>
	</div>
</template>

<script setup lang="ts">
type Props = {
	title: string;
	number: number;
};

defineProps<Props>();
</script>

<style scoped>
.total-number-stat {
	border: 2px solid var(--black);
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	width: 100%;
	padding: 1rem;
	min-height: 140px;
}

.title {
	margin: 0;
}

.number {
	font-weight: bold;
	font-size: 2rem;
	margin: 0.5rem 0 0;
}
</style>