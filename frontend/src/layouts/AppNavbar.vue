<template>
	<div class="app-navbar">
		<div class="main-buttons">
			<NavItem link="/estadisticas" name="ESTADÍSTICAS" />
			<NavItem link="/nube-de-palabras" name="NUBE DE PALABRAS" />
			<NavItem
				v-if="props.role === 'GESTOR'"
				link="/fuentes-y-rss"
				name="FUENTES Y RSS"
			/>
			<NavItem
				v-if="props.role === 'GESTOR'"
				link="/alertas"
				name="ALERTAS"
			/>
			<NavItem link="/notificaciones" name="NOTIFICACIONES" />
			<NavItem link="/cuenta" name="CUENTA" />
		</div>
		<RouterLink to="/" class="cerrar-sesion">CERRAR SESIÓN</RouterLink>
	</div>
</template>

<script setup lang="ts">
import NavItem from "./NavItem.vue";
import { RouterLink } from "vue-router";

type Props = { role: "LECTOR" | "GESTOR" };
const props = defineProps<Props>();
</script>

<style scoped>
.app-navbar {
	background-color: var(--black);
	display: flex;
	flex-direction: column;
	justify-content: space-between;
	padding: 1rem;
	border-top: 1px solid white;
}

.cerrar-sesion {
	padding: 1rem;
	color: white;
	white-space: nowrap;
	color: rgb(203, 61, 61);
}

.cerrar-sesion:hover {
	background-color: rgb(49, 26, 26);
}
</style>
