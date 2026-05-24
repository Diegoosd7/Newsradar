<template>
	<div class="view">
		<div class="header">
			<h1>Notificaciones</h1>
		</div>
		<div class="main">
			<p v-if="error" class="error-msg">{{ error }}</p>
			<p v-if="loading">Cargando notificaciones...</p>
			<p v-else-if="notifications.length === 0">No tienes notificaciones todavía.</p>
			<p v-else class="count-line">
				Total de notificaciones: <strong>{{ notifications.length }}</strong>
			</p>
			<div class="container">
				<NotificationItem
					v-for="notification in notifications"
					:key="notification.id"
					:alert-title="alertTitle(notification.alert_id)"
					:datetime="formatDateTime(notification.timestamp)"
					:news="{
						origin: notification.source_name ?? '—',
						publication: formatDateTime(notification.news_published),
						title: notification.news_title ?? '—',
						summary: notification.news_summary ?? '—',
					}"
					@delete="onDelete(notification)"
				/>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import NotificationItem from "./NotificationItem.vue";
import { ref, onMounted } from "vue";
import { useApiCall } from "@/api/useApiCall";
import { useAuthStore } from "@/stores/auth";
import type { AlertResponse, NotificationResponse } from "@/api/types";

const api = useApiCall();
const auth = useAuthStore();

const notifications = ref<NotificationResponse[]>([]);
const alerts = ref<AlertResponse[]>([]);
const loading = ref<boolean>(false);
const error = ref<string>("");

const alertTitle = (alertId: number): string => {
	const a = alerts.value.find((x) => x.id === alertId);
	return a ? a.name : `Alerta #${alertId}`;
};

const formatDateTime = (iso: string | null | undefined): string => {
    if (!iso) return "—";
    const d = new Date(iso);
    if (Number.isNaN(d.getTime())) return iso;
    return d.toLocaleString("es-ES", {
        timeZone: "Europe/Madrid",
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    }).replace(",", " -");
};

const loadAll = async () => {
	if (!auth.token || !auth.user) return;
	loading.value = true;
	error.value = "";
	try {
		const [n, a] = await Promise.all([
			api.getUserNotifications(auth.token, auth.user.id),
			api.getUserAlerts(auth.token, auth.user.id),
		]);
		notifications.value = n;
		alerts.value = a;
	} catch (e: unknown) {
		error.value = e instanceof Error ? e.message : "Error cargando notificaciones.";
	} finally {
		loading.value = false;
	}
};

const onDelete = async (notification: NotificationResponse) => {
	if (!auth.token || !auth.user) return;
	if (!confirm("¿Eliminar esta notificación?")) return;
	try {
		await api.deleteAlertNotification(
			auth.token,
			auth.user.id,
			notification.alert_id,
			notification.id,
		);
		await loadAll();
	} catch (e: unknown) {
		alert(e instanceof Error ? e.message : "Error eliminando notificación.");
	}
};

onMounted(loadAll);
</script>

<style scoped>
.main {
	display: flex;
	flex-direction: column;
	gap: 1rem;
	justify-content: center;
	align-items: center;
}

.container {
	display: flex;
	flex-direction: column;
	gap: 1rem;
	width: max-content;
}

.count-line {
	font-size: 1rem;
}

.error-msg {
	color: rgb(203, 61, 61);
	border: 1px solid rgb(203, 61, 61);
	background-color: rgb(254, 236, 236);
	padding: 0.5rem;
	font-size: 0.9rem;
}
</style>
