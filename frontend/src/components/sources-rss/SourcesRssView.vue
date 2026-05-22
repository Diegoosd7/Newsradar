<template>
	<div class="view">
		<div class="header">
			<h1>Fuentes y RSS</h1>
		</div>
		<div class="main">
			<div>
				<button @click="toggleNewSource" class="form-button">
					+ NUEVA FUENTE
				</button>
			</div>
			<p v-if="error" class="error-msg">{{ error }}</p>
			<NewSourceItem v-if="showNewSource" @created="onSourceCreated" />
			<p v-if="loading">Cargando fuentes...</p>
			<p v-else-if="sources.length === 0">No hay fuentes todavía.</p>
			<div class="container">
				<SourceItem
					v-for="source in sources"
					:key="source.id"
					:id="source.id"
					:name="source.name"
					:url="source.url"
					:categories="categories"
					@deleted="loadSources"
				/>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import NewSourceItem from "./NewSourceItem.vue";
import SourceItem from "./SourceItem.vue";
import { ref, onMounted } from "vue";
import { useApiCall } from "@/api/useApiCall";
import { useAuthStore } from "@/stores/auth";
import type { InformationSourceResponse, CategoryResponse } from "@/api/types";

const api = useApiCall();
const auth = useAuthStore();

const sources = ref<InformationSourceResponse[]>([]);
const categories = ref<CategoryResponse[]>([]);
const showNewSource = ref<boolean>(false);
const loading = ref<boolean>(false);
const error = ref<string>("");

const toggleNewSource = () => {
	showNewSource.value = !showNewSource.value;
};

const loadSources = async () => {
	if (!auth.token) return;
	loading.value = true;
	error.value = "";
	try {
		sources.value = await api.getSources(auth.token);
	} catch (e: unknown) {
		error.value = e instanceof Error ? e.message : "Error cargando fuentes";
	} finally {
		loading.value = false;
	}
};

const loadCategories = async () => {
	if (!auth.token) return;
	try {
		categories.value = await api.getCategories(auth.token);
	} catch (e: unknown) {
		// Categorías son secundarias para la vista; no bloqueamos por error aquí.
		console.warn("No se pudieron cargar categorías:", e);
	}
};

const onSourceCreated = async () => {
	showNewSource.value = false;
	await loadSources();
};

onMounted(async () => {
	await Promise.all([loadSources(), loadCategories()]);
});
</script>

<style scoped>
.main {
	display: flex;
	flex-direction: column;
	gap: 1rem;
}

.container {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	gap: 1rem;
}

.form-button {
	width: max-content;
}

.error-msg {
	color: rgb(203, 61, 61);
	border: 1px solid rgb(203, 61, 61);
	background-color: rgb(254, 236, 236);
	padding: 0.5rem;
	font-size: 0.9rem;
}
</style>
