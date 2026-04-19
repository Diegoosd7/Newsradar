<template>
	<div class="login-form">
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
import { reactive } from "vue";

const fields = reactive({
	email: "",
	password: "",
});

const sendForm = () => {
	console.log("Register form sent!");
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
