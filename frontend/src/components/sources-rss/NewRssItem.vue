<template>
	<div class="new-rss-item">
		<select v-model.number="fields.category_id" name="iptc-category">
			<option :value="0" disabled>Selecciona categoría...</option>
			<option v-for="category in props.categories" :key="category.id" :value="category.id">
				{{ category.name }}
			</option>
		</select>
		<input v-model="fields.url" class="url-field" type="text" name="url" placeholder="URL..." />
		<button :disabled="loading" @click="sendForm" class="add-button">{{ loading ? '...' : '+' }}</button>
	</div>
	<p v-if="error" class="error-msg">{{ error }}</p>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { useApiCall } from "@/api/useApiCall";
import { useAuthStore } from "@/stores/auth";
import type { CategoryResponse } from "@/api/types";

type Props = { sourceId: number; categories: CategoryResponse[] };
const props = defineProps<Props>();
const emit = defineEmits<{ created: [] }>();

const api = useApiCall();
const auth = useAuthStore();

const fields = reactive({ category_id: 0, url: "" });
const loading = ref(false);
const error = ref("");

const sendForm = async () => {
	error.value = "";
	if (!fields.category_id) {
		error.value = "Selecciona una categoría.";
		return;
	}
	if (!fields.url.trim()) {
		error.value = "Introduce una URL.";
		return;
	}
	if (!auth.token) {
		error.value = "Sesión no iniciada.";
		return;
	}
	loading.value = true;
	try {
		await api.createSourceChannel(auth.token, props.sourceId, {
			url: fields.url.trim(),
			category_id: fields.category_id,
		});
		fields.category_id = 0;
		fields.url = "";
		emit("created");
	} catch (e: unknown) {
		error.value = e instanceof Error ? e.message : "Error creando canal RSS.";
	} finally {
		loading.value = false;
	}
};
</script>

<style scoped>
.new-rss-item {
	display: flex;
	align-items: center;
	justify-content: space-between;
	gap: 1rem;
	border: 1px solid black;
	padding-left: 1rem;
}

.url-field {
	padding: 0.5rem;
	flex: 1;
	border: 1px solid black;
}

.add-button {
	font-size: 1.5rem;
	padding: 1rem;
}

.add-button:hover:not(:disabled) {
	color: green;
}

.add-button:disabled {
	opacity: 0.5;
	cursor: not-allowed;
}

.error-msg {
	color: rgb(203, 61, 61);
	border: 1px solid rgb(203, 61, 61);
	background-color: rgb(254, 236, 236);
	padding: 0.5rem;
	font-size: 0.9rem;
}
</style>
