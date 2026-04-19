<template>
	<div class="login-form">
		<label>
			NOMBRE
			<input v-model="fields.name" type="text" name="name" />
		</label>
		<label>
			APELLIDOS
			<input v-model="fields.surnames" type="text" name="surnames" />
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
		<label>
			CONTRASEÑA
			<input v-model="fields.password" type="text" name="password" />
		</label>
		<button @click="sendForm" class="form-button">CONTINUAR</button>
	</div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";

const fields = reactive({
	name: "",
	surnames: "",
	organization: "",
	email: "",
	password: "",
});

const sendForm = () => {
	console.log("Login form sent!");
};
</script>

<style scoped>
.login-form {
	display: flex;
	flex-direction: column;
	gap: 1rem;
	padding: 1rem;
	width: 400px;
	background-color: rgb(210, 210, 247);
	background-color: rgb(255, 255, 255);
}

label {
	display: flex;
	flex-direction: column;
	gap: 0.2rem;
	width: 100%;
}

input {
	padding: 0.5rem;
	width: 100%;
	background-color: white;
	border: 1px solid black;
}

.form-button {
	padding: 1rem;
	background-color: var(--black);
	color: white;
	transition: 0.3s;
}

.form-button:hover {
	color: rgb(141, 141, 141);
}
</style>
