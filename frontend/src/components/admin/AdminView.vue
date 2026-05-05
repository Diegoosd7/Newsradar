<template>
	<div class="view">
		<div class="header">
			<h1>Admin</h1>
		</div>
		<div class="main">
			<RouterLink to="/" class="cerrar-sesion">CERRAR SESIÓN</RouterLink>
			<div class="container">
				<template v-for="user in users">
					<AdminItem v-bind="user" />
				</template>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import AdminItem from "./AdminItem.vue";
import { onBeforeMount, ref } from "vue";
import type { Role } from "@/types/index";

const users = ref<{ name: string; organization_name: string; email: string; role: Role }[]>([]);

const getUsers = () => {
	users.value = [
		{
			name: "Juan Perez",
			organization_name: "UC3M",
			email: "juan@gmail.com",
			role: "LECTOR",
		},
		{
			name: "Juan Perezzzzzzzzzzzzz",
			organization_name: "URJC",
			email: "juanzzz@gmail.com",
			role: "GESTOR",
		},
	];
};

onBeforeMount(() => {
	getUsers();
});
</script>

<style scoped>
.main {
	display: flex;
	flex-direction: column;
	gap: 1rem;
}

.header {
	display: flex;
	justify-content: space-between;
	align-items: center;
	width: 100%;
}

.cerrar-sesion {
	padding: 1rem;
	color: white;
	white-space: nowrap;
	color: rgb(203, 61, 61);
	border: 2px solid rgb(203, 61, 61);
	transition: 0.3s;
	width: max-content;
}

.cerrar-sesion:hover {
	background-color: rgb(241, 210, 210);
}

.container {
	display: flex;
	flex-direction: column;
	gap: 1rem;
	width: max-content;
}
</style>
