<template>
	<div class="view">
		<div class="header">
			<h1>Alertas</h1>
		</div>
		<div class="main">
			<button @click="toggleNewAlert" class="form-button">
				+ NUEVA ALERTA
			</button>
			<NewAlertItem v-if="showNewAlert" />
			<div class="container">
				<div class="table-header">
					<div>TITULO</div>
					<div>DESCRIPTORES</div>
					<div>CATEGORÍA</div>
					<div>CRON</div>
					<div>NOTIFICACIONES</div>
					<div>RSS</div>
					<div>ACCIONES</div>
				</div>
				<AlertItem />
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import NewAlertItem from "./NewAlertItem.vue";
import AlertItem from "./AlertItem.vue";

const showNewAlert = ref<boolean>(false);

const toggleNewAlert = () => {
	showNewAlert.value = !showNewAlert.value;
};
</script>

<style scoped>
.main {
	display: flex;
	flex-direction: column;
	gap: 1rem;
}

.form-button {
	width: max-content;
}

.container {
	display: flex;
	flex-direction: column;
	/* gap: 1rem; */
}

.table-header {
	border: 2px solid var(--black);
	padding: 1rem 0;
	font-weight: bold;
	display: grid;
	grid-template-columns: repeat(7, 150px);
	width: max-content;
	gap: 0.5rem;
	text-align: center;
	background-color: var(--black);
	color: white;
}
</style>
