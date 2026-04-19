<template>
	<div class="login-form">
		<p v-if="error" class="error-msg">{{ error }}</p>
		<p v-if="success" class="success-msg">
			Cuenta creada. Revisa tu email para verificarla y luego inicia sesión.
		</p>
		<template v-if="!success">
			<label>
				NOMBRE
				<input v-model="fields.first_name" type="text" name="first_name" autocomplete="given-name" />
			</label>
			<label>
				APELLIDOS
				<input v-model="fields.last_name" type="text" name="last_name" autocomplete="family-name" />
			</label>
			<label>
				ORGANIZACIÓN
				<input v-model="fields.organization" type="text" name="organization" autocomplete="organization" />
			</label>
			<label>
				EMAIL
				<input v-model="fields.email" type="email" name="email" autocomplete="email" />
			</label>
			<label>
				CONTRASEÑA
				<input v-model="fields.password" type="password" name="password" autocomplete="new-password" />
			</label>
			<button @click="sendForm" :disabled="loading" class="form-button">
				{{ loading ? 'REGISTRANDO...' : 'CREAR CUENTA' }}
			</button>
		</template>
	</div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useApiCall } from '@/api/useApiCall'

const api = useApiCall()

const fields = reactive({
	first_name: '',
	last_name: '',
	organization: '',
	email: '',
	password: '',
})
const loading = ref(false)
const error = ref('')
const success = ref(false)

const sendForm = async () => {
	error.value = ''
	if (!fields.first_name || !fields.last_name || !fields.organization || !fields.email || !fields.password) {
		error.value = 'Por favor, rellena todos los campos.'
		return
	}
	if (fields.password.length < 6) {
		error.value = 'La contraseña debe tener al menos 6 caracteres.'
		return
	}
	loading.value = true
	try {
		await api.register({
			first_name: fields.first_name,
			last_name: fields.last_name,
			organization: fields.organization,
			email: fields.email,
			password: fields.password,
		})
		success.value = true
	} catch (e: unknown) {
		error.value = e instanceof Error ? e.message : 'Error al registrarse.'
	} finally {
		loading.value = false
	}
}
</script>

<style scoped>
.login-form {
	display: flex;
	flex-direction: column;
	gap: 1rem;
	padding: 1rem;
	width: 400px;
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

.form-button:hover:not(:disabled) {
	color: rgb(141, 141, 141);
}

.form-button:disabled {
	opacity: 0.6;
	cursor: not-allowed;
}

.error-msg {
	color: rgb(203, 61, 61);
	border: 1px solid rgb(203, 61, 61);
	background-color: rgb(254, 236, 236);
	padding: 0.5rem;
	font-size: 0.9rem;
}

.success-msg {
	color: green;
	border: 1px solid green;
	background-color: #d5f1d5;
	padding: 0.75rem;
	font-size: 0.9rem;
}
</style>
