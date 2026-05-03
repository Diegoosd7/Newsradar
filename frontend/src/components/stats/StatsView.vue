<template>
	<div class="view">
		<div class="header">
			<h1>Estadísticas</h1>
		</div>

		<div v-if="errorMessage" class="error-message">
			{{ errorMessage }}
		</div>

		<div class="main">
			<div class="total-number-container">
				<TotalNumberStat
					v-for="stat in totalNumberStats"
					:key="stat.title"
					:title="stat.title"
					:number="stat.number"
				/>
			</div>

			<div class="per-category-container">
				<PerCategoryStat
					title="NOTICIAS POR CATEGORÍA"
					:items="newsByCategory"
				/>
				<PerCategoryStat
					title="ALERTAS POR CATEGORÍA"
					:items="alertsByCategory"
				/>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import PerCategoryStat from "./PerCategoryStat.vue";
import TotalNumberStat from "./TotalNumberStat.vue";
import { useApiCall } from "@/api/useApiCall";
import { useAuthStore } from "@/stores/auth";
import type { CategoryCountItem } from "@/api/types";

type TotalNumberStatItem = {
	title: string;
	number: number;
};

const api = useApiCall();
const auth = useAuthStore();

const errorMessage = ref("");

const totalNumberStats = ref<TotalNumberStatItem[]>([
	{ title: "FUENTES", number: 0 },
	{ title: "RSS", number: 0 },
	{ title: "NOTICIAS", number: 0 },
	{ title: "ALERTAS", number: 0 },
]);

const newsByCategory = ref<CategoryCountItem[]>([]);
const alertsByCategory = ref<CategoryCountItem[]>([]);

const loadDashboardStats = async () => {
	if (!auth.token) {
		errorMessage.value = "No hay sesión activa.";
		return;
	}

	try {
		const data = await api.getDashboardStats(auth.token);

		totalNumberStats.value = [
			{ title: "FUENTES", number: data.summary.sources },
			{ title: "RSS", number: data.summary.rss_channels },
			{ title: "NOTICIAS", number: data.summary.news },
			{ title: "ALERTAS", number: data.summary.alerts },
		];

		newsByCategory.value = data.news_by_category;
		alertsByCategory.value = data.alerts_by_category;
		errorMessage.value = "";
	} catch (error) {
		console.error(error);
		errorMessage.value = "No se pudieron cargar las estadísticas.";
	}
};

onMounted(() => {
	loadDashboardStats();
});
</script>

<style scoped>
.view,
.main {
	display: flex;
	flex-direction: column;
	gap: 1rem;
}

.total-number-container {
	display: grid;
	grid-template-columns: repeat(4, 1fr);
	gap: 1rem;
}

.per-category-container {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	gap: 1rem;
}

.error-message {
	padding: 0.75rem 1rem;
	border: 2px solid #b00020;
	color: #b00020;
	background: #fff5f6;
}
</style>