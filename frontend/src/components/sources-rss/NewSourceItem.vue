<template>
	<div class="new-source-item">
		<input v-model="fields.name" class="field" type="text" name="name" placeholder="Nombre..." />
		<input v-model="fields.url" class="field" type="text" name="url" placeholder="URL..." />
		<button :disabled="loading" @click="sendForm" class="add-button">{{ loading ? '...' : '+' }}</button>
	</div>
	<p v-if="error" class="error-msg">{{ error }}</p>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";
import { useApiCall } from "@/api/useApiCall";
import { useAuthStore } from "@/stores/auth";

const emit = defineEmits<{ created: [] }>();

const api = useApiCall();
const auth = useAuthStore();

const fields = reactive({ name: "", url: "" });
const loading = ref(false);
const error = ref("");

const sendForm = async () => {
	error.value = "";
	if (!fields.name.trim() || !fields.url.trim()) {
		error.value = "Por favor, rellena nombre y URL.";
		return;
	}
	if (!auth.token) {
		error.value = "Sesión no iniciada.";
		return;
	}
	loading.value = true;
	try {
		await api.createSource(auth.token, {
			name: fields.name.trim(),
			url: fields.url.trim(),
		});
		fields.name = "";
		fields.url = "";
		emit("created");
	} catch (e: unknown) {
		error.value = e instanceof Error ? e.message : "Error creando fuente.";
	} finally {
		loading.value = false;
	}
};
</script>

<style scoped>
.new-source-item {
	display: flex;
	gap: 1rem;
	border: 2px solid var(--black);
	padding: 1rem;
}

.field {
	padding: 0.5rem;
	flex: 1;
	border: 1px solid black;
}

.add-button {
	font-size: 1.5rem;
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
