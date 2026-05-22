<template>
	<div class="notification-item">
		<div class="header">
			<p class="title">
				Actualización de
				<span class="highlight">{{ props.alertTitle }}</span>
				en
				<span class="highlight">{{ props.datetime }}</span>
			</p>
			<button @click="emit('delete')" class="delete-button">X</button>
		</div>
		<div class="main">
			<div class="field-container">
				<div class="field">
					<p class="field-title">ORIGEN</p>
					<p>{{ props.news.origin }}</p>
				</div>
				<div class="field">
					<p class="field-title">PUBLICACIÓN</p>
					<p>{{ props.news.publication }}</p>
				</div>
			</div>
			<div class="field">
				<p class="field-title">TÍTULO</p>
				<p>{{ props.news.title }}</p>
			</div>
			<div class="field">
				<p class="field-title">RESUMEN</p>
				<p>{{ props.news.summary }}</p>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
type Props = {
	alertTitle: string;
	datetime: string;
	news: {
		origin: string;
		publication: string;
		title: string;
		summary: string;
	};
};
const props = defineProps<Props>();
const emit = defineEmits<{ delete: [] }>();
</script>

<style scoped>
.notification-item {
	width: 100%;
}

.header {
	display: flex;
	gap: 1rem;
	justify-content: space-between;
	align-items: center;
	background-color: var(--black);
	padding-left: 1rem;
	font-size: 1.5rem;
}

.title {
	color: white;
}

.highlight {
	/* border: 1px solid white; */
	/* background-color: white; */
	/* color: var(--black); */
	padding: 0 0.5rem;
	font-weight: bold;
}

.delete-button {
	color: white;
	padding: 1rem;
	font-size: 1.5rem;
}

.delete-button:hover {
	color: rgb(203, 61, 61);
}

.main {
	display: flex;
	flex-direction: column;
	gap: 1rem;
	border: 2px solid var(--black);
	padding: 1rem;
}

.field-title {
	font-weight: bold;
}

.field-container {
	display: flex;
	gap: 2rem;
}
</style>
