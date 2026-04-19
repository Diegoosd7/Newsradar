<template>
	<div class="view">
		<div class="header">
			<h1>Notificaciones</h1>
		</div>
		<div class="main">
			<div class="container">
				<template v-for="notification in notifications">
					<NotificationItem v-bind="notification" />
				</template>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import NotificationItem from "./NotificationItem.vue";
import { ref } from "vue";

const notifications = ref([
	{
		alertTitle: "MI ALERTA",
		datetime: "10/03/2026 - 18:32",
		news: {
			origin: "El País",
			publication: "10/03/2026 - 10:04",
			title: "Título de la noticia",
			summary: "Lorem ipsum",
		},
	},
	{
		alertTitle: "MI ALERTA",
		datetime: "10/03/2026 - 18:32",
		news: {
			origin: "El País",
			publication: "10/03/2026 - 10:04",
			title: "Título de la noticia",
			summary: "Lorem ipsum",
		},
	},
]);
</script>

<style scoped>
.main {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}

.container {
	display: flex;
	flex-direction: column;
	gap: 1rem;
	width: max-content;
}
</style>
