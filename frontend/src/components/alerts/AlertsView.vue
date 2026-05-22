<template>
	<div class="view">
		<div class="header">
			<h1>Alertas</h1>
		</div>
		<div class="main">
			<button @click="toggleNewAlert" class="form-button">
				+ NUEVA ALERTA
			</button>
			<p v-if="error" class="error-msg">{{ error }}</p>
			<NewAlertItem
				v-if="showNewAlert"
				:categories="categories"
				:sources="sources"
				:channels="channels"
				@created="onAlertCreated"
			/>
			<p v-if="loading">Cargando alertas...</p>
			<p v-else-if="alerts.length === 0">No tienes alertas todavía.</p>
			<div v-else class="container">
				<div class="table-header">
					<div>TITULO</div>
					<div>DESCRIPTORES</div>
					<div>CATEGORÍA</div>
					<div>CRON</div>
					<div>NOTIFICACIONES</div>
					<div>RSS</div>
					<div>ACCIONES</div>
				</div>
				<AlertItem
					v-for="alert in alerts"
					:key="alert.id"
					:alert="alert"
					:channels="channels"
					:sources="sources"
					@deleted="loadAlerts"
				/>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import NewAlertItem from "./NewAlertItem.vue";
import AlertItem from "./AlertItem.vue";
import { useApiCall } from "@/api/useApiCall";
import { useAuthStore } from "@/stores/auth";
import type {
	AlertResponse,
	CategoryResponse,
	InformationSourceResponse,
	RssChannelResponse,
} from "@/api/types";

const api = useApiCall();
const auth = useAuthStore();

const showNewAlert = ref<boolean>(false);
const alerts = ref<AlertResponse[]>([]);
const categories = ref<CategoryResponse[]>([]);
const sources = ref<InformationSourceResponse[]>([]);
const channels = ref<RssChannelResponse[]>([]);
const loading = ref<boolean>(false);
const error = ref<string>("");

const toggleNewAlert = () => {
	showNewAlert.value = !showNewAlert.value;
};

const loadAlerts = async () => {
	if (!auth.token || !auth.user) return;
	loading.value = true;
	error.value = "";
	try {
		alerts.value = await api.getUserAlerts(auth.token, auth.user.id);
	} catch (e: unknown) {
		error.value = e instanceof Error ? e.message : "Error cargando alertas.";
	} finally {
		loading.value = false;
	}
};

const loadCatalogs = async () => {
	if (!auth.token) return;
	try {
		const [cats, srcs, chs] = await Promise.all([
			api.getCategories(auth.token),
			api.getSources(auth.token),
			api.getAllChannels(auth.token),
		]);
		categories.value = cats;
		sources.value = srcs;
		channels.value = chs;
	} catch (e: unknown) {
		console.warn("No se pudieron cargar catálogos:", e);
	}
};

const onAlertCreated = async () => {
	showNewAlert.value = false;
	await loadAlerts();
};

onMounted(async () => {
	await Promise.all([loadAlerts(), loadCatalogs()]);
});
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

.error-msg {
	color: rgb(203, 61, 61);
	border: 1px solid rgb(203, 61, 61);
	background-color: rgb(254, 236, 236);
	padding: 0.5rem;
	font-size: 0.9rem;
}
</style>
