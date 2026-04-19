<template>
	<div class="login-form">
		<p v-if="error" class="error-msg">{{ error }}</p>
		<label>
			EMAIL
			<input v-model="fields.email" type="email" name="email" autocomplete="email" />
		</label>
		<label>
			CONTRASEÑA
			<input v-model="fields.password" type="password" name="password" autocomplete="current-password" />
		</label>
		<button @click="sendForm" :disabled="loading" class="form-button">
			{{ loading ? 'CARGANDO...' : 'ENTRAR' }}
		</button>
		<button @click="emit('forgot-password')" class="forgot-button">
			¿Olvidaste tu contraseña?
		</button>
	</div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const emit = defineEmits<{ 'forgot-password': [] }>()

const router = useRouter()
const auth = useAuthStore()

const fields = reactive({ email: '', password: '' })
const loading = ref(false)
const error = ref('')

const sendForm = async () => {
	error.value = ''
	if (!fields.email || !fields.password) {
		error.value = 'Por favor, rellena todos los campos.'
		return
	}
	loading.value = true
	try {
		await auth.login(fields.email, fields.password)
		router.push({ name: 'estadisticas' })
	} catch (e: unknown) {
		error.value = e instanceof Error ? e.message : 'Error al iniciar sesión.'
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

.forgot-button {
	background: none;
	border: none;
	color: gray;
	text-decoration: underline;
	cursor: pointer;
	font-size: 0.85rem;
	text-align: left;
	padding: 0;
}

.error-msg {
	color: rgb(203, 61, 61);
	border: 1px solid rgb(203, 61, 61);
	background-color: rgb(254, 236, 236);
	padding: 0.5rem;
	font-size: 0.9rem;
}
</style>
