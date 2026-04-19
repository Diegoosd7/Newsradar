<template>
	<div class="personal-info">
		<div class="personal-info-section">
			<p class="title">INFORMACIÓN PERSONAL</p>
			<div class="form">
				<label>
					NOMBRE
					<input v-model="fields.name" type="text" name="name" />
				</label>
				<label>
					APELLIDOS
					<input
						v-model="fields.surnames"
						type="text"
						name="surnames"
					/>
				</label>
				<label>
					ORGANIZACIÓN
					<input
						v-model="fields.organization"
						type="text"
						name="organization"
					/>
				</label>
				<label>
					EMAIL
					<input v-model="fields.email" type="text" name="email" />
				</label>
			</div>
			<button @click="sendForm" class="form-button">EDITAR</button>
			<button class="delete-account-button">BORRAR LA CUENTA</button>
		</div>
	</div>
</template>

<script setup lang="ts">
import { reactive } from "vue";

const fields = reactive({
	name: "",
	surnames: "",
	organization: "",
	email: "",
});

const sendForm = () => {
	console.log("Login form sent!");
};
</script>

<style scoped>
.personal-info {
	display: flex;
	flex-direction: column;
	gap: 1rem;
	width: 50%;
}

.personal-info-section {
	display: flex;
	flex-direction: column;
	gap: 1rem;
	border: 2px solid var(--black);
	padding: 1rem;
}

.form {
	display: grid;
	grid-template-columns: repeat(2, 1fr);
	flex-direction: column;
	gap: 1rem;
}

.title {
	font-size: 1.2rem;
	font-weight: bold;
	text-align: center;
}

.delete-account-button {
	padding: 1rem;
	color: white;
	white-space: nowrap;
	color: rgb(203, 61, 61);
	border: 1px solid rgb(203, 61, 61);
	/* background-color: rgb(254, 236, 236); */
	transition: 0.3s;
}

.delete-account-button:hover {
	background-color: rgb(241, 210, 210);
}
</style>
