<template>
	<div class="rss-item">
		<p class="field iptc-field">{{ props.iptcCategory }}</p>
		<p class="field">{{ props.url }}</p>
		<button class="x-button">X</button>
	</div>
</template>

<script setup lang="ts">
type Props = { id: number; iptcCategory: string; url: string };
const props = defineProps<Props>();
</script>

<style scoped>
.rss-item {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	border: 1px solid black;
	padding-left: 1rem;
	width: 100%;
}

.iptc-field {
	border: 1px solid black;
	padding: 0.5rem;
}
</style>
