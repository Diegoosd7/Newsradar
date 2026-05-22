<template>
	<div class="rss-item">
		<p class="field iptc-field">{{ props.iptcCategory }}</p>
		<p class="field url-field">{{ props.url }}</p>
		<button @click="deleteItem" class="x-button">X</button>
	</div>
</template>

<script setup lang="ts">
import { useApiCall } from "@/api/useApiCall";
import { useAuthStore } from "@/stores/auth";

type Props = { id: number; sourceId: number; iptcCategory: string; url: string };
const props = defineProps<Props>();
const emit = defineEmits<{ deleted: [] }>();

const api = useApiCall();
const auth = useAuthStore();

const deleteItem = async () => {
	if (!auth.token) return;
	if (!confirm("¿Eliminar este canal RSS?")) return;
	try {
		await api.deleteSourceChannel(auth.token, props.sourceId, props.id);
		emit("deleted");
	} catch (e: unknown) {
		alert(e instanceof Error ? e.message : "Error eliminando canal RSS.");
	}
};
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
	white-space: nowrap;
}

.url-field {
	flex: 1;
	word-break: break-all;
}

.x-button {
	padding: 0.5rem 1rem;
}
</style>
