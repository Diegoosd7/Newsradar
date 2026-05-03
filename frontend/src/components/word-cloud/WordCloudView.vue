<template>
	<div class="view">
		<div class="header">
			<h1>Nube de palabras</h1>
		</div>

		<div v-if="errorMessage" class="error-message">
			{{ errorMessage }}
		</div>

		<div class="container">
			<WordCloudItem
				v-for="item in items"
				:key="`${item.category_code}-${item.category_label}`"
				:title="item.category_label"
				:words="item.words"
			/>
		</div>
	</div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import WordCloudItem from "./WordCloudItem.vue";
import { useApiCall } from "@/api/useApiCall";
import { useAuthStore } from "@/stores/auth";
import type { TrendingCategoryItem } from "@/api/types";

const api = useApiCall();
const auth = useAuthStore();

const items = ref<TrendingCategoryItem[]>([]);
const errorMessage = ref("");

const loadTrendingWords = async () => {
	if (!auth.token) {
		errorMessage.value = "No hay sesión activa.";
		return;
	}

	try {
		const data = await api.getDashboardStats(auth.token);
		items.value = data.trending_by_category;
		errorMessage.value = "";
	} catch (error) {
		console.error(error);
		errorMessage.value = "No se pudo cargar la nube de palabras.";
	}
};

onMounted(() => {
	loadTrendingWords();
});
</script>

<style scoped>
.view {
	display: flex;
	flex-direction: column;
	gap: 1rem;
}

.container {
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