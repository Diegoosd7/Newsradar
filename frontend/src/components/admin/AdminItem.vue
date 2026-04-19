<template>
	<div class="admin-item">
		<div class="user-info">
			<p class="name">{{ props.name }}</p>
			<p>{{ props.organization_name }}</p>
			<p>{{ props.email }}</p>
		</div>
		<div class="interactive">
			<select name="role" class="select-role" v-model="assignedRole">
				<option value="LECTOR">Lector</option>
				<option value="GESTOR">Gestor</option>
			</select>
			<button @click="deleteUser" class="x-button">X</button>
		</div>
	</div>
</template>

<script setup lang="ts">
import type { Role } from "@/types/index";
import { ref, watch } from "vue";

type Props = {
	name: string;
	organization_name: string;
	email: string;
	role: Role;
};
const props = defineProps<Props>();

const assignedRole = ref<Role>(props.role);

watch(assignedRole, () => {
	console.log(`Update role: ${assignedRole.value}`);
});

const deleteUser = () => {
	if (
		confirm(
			`¿Estás seguro de que quieres eliminar el usuario ${props.name}?`,
		)
	) {
		console.log(`delete ${props.name}`);
	}
};
</script>

<style scoped>
.admin-item {
	display: flex;
	justify-content: space-between;
	border: 2px solid var(--black);
	width: 100%;
	padding: 1rem;
	padding-right: 0;
	gap: 2rem;
}

/* lEFT */

.user-info {
	display: flex;
	flex-direction: column;
}

.name {
	font-size: 1.2rem;
	font-weight: bold;
	margin-bottom: 0.5rem;
}

/* RIGHT */

.interactive {
	display: flex;
	/* gap: 1rem; */
	align-items: center;
}

.select-role {
	height: min-content;
}
</style>
