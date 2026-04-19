import AccountView from "@/components/account/AccountView.vue";
import AdminView from "@/components/admin/AdminView.vue";
import AlertsView from "@/components/alerts/AlertsView.vue";
import LoginView from "@/components/login/LoginView.vue";
import NotificationsView from "@/components/notifications/NotificationsView.vue";
import SourcesRssView from "@/components/sources-rss/SourcesRssView.vue";
import StatsView from "@/components/stats/StatsView.vue";
import WordCloudView from "@/components/word-cloud/WordCloudView.vue";
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
	history: createWebHistory(import.meta.env.BASE_URL),
	routes: [
		{
			path: "/",
			name: "login",
			component: LoginView,
		},
		{
			path: "/admin",
			name: "admin",
			component: AdminView,
		},
		{
			path: "/estadisticas",
			name: "estadisticas",
			component: StatsView,
		},
		{
			path: "/nube-de-palabras",
			name: "nube-de-palabras",
			component: WordCloudView,
		},
		{
			path: "/fuentes-y-rss",
			name: "fuentes-y-rss",
			component: SourcesRssView,
		},
		{
			path: "/alertas",
			name: "alertas",
			component: AlertsView,
		},
		{
			path: "/notificaciones",
			name: "notificaciones",
			component: NotificationsView,
		},
		{
			path: "/cuenta",
			name: "cuenta",
			component: AccountView,
		},
	],
});

export default router;
