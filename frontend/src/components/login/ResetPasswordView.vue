<template>
	<div class="view">
		<div class="login-register-modal">
			<div class="options">
				<div class="option option--active option--title">NUEVA CONTRASEÑA</div>
			</div>
			<div class="reset-form">
				<p v-if="!token" class="error-msg">
					Enlace inválido. Solicita un nuevo correo de recuperación.
				</p>
				<template v-else-if="success">
					<p class="success-msg">
						Contraseña actualizada correctamente. Ya puedes iniciar sesión.
					</p>
					<button @click="router.push({ name: 'login' })" class="form-button">
						IR AL LOGIN
					</button>
				</template>
				<template v-else>
					<label>
						NUEVA CONTRASEÑA
						<input v-model="newPassword" type="password" autocomplete="new-password" />
					</label>
					<label>
						CONFIRMAR CONTRASEÑA
						<input v-model="confirmPassword" type="password" autocomplete="new-password" />
					</label>
					<p v-if="errorMsg" class="error-msg">{{ errorMsg }}</p>
					<button @click="submit" :disabled="loading" class="form-button">
						{{ loading ? 'GUARDANDO...' : 'GUARDAR CONTRASEÑA' }}
					</button>
				</template>
			</div>
		</div>
	</div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

const token = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const success = ref(false)
const errorMsg = ref('')

onMounted(() => {
	token.value = (route.query.token as string) ?? ''
})

const submit = async () => {
	errorMsg.value = ''
	if (newPassword.value.length < 6) {
		errorMsg.value = 'La contraseña debe tener al menos 6 caracteres.'
		return
	}
	if (newPassword.value !== confirmPassword.value) {
		errorMsg.value = 'Las contraseñas no coinciden.'
		return
	}
	loading.value = true
	try {
		const res = await fetch('/api/v1/auth/reset-password', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ token: token.value, new_password: newPassword.value }),
		})
		if (!res.ok) {
			const data = await res.json().catch(() => ({}))
			errorMsg.value = data.detail ?? 'El enlace ha expirado o no es válido.'
		} else {
			success.value = true
		}
	} catch {
		errorMsg.value = 'Error de conexión. Inténtalo de nuevo.'
	} finally {
		loading.value = false
	}
}
</script>

<style scoped>
.login-register-modal {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
	border: 2px solid var(--black);
	width: max-content;
}

.options {
	display: grid;
	grid-template-columns: 1fr;
	width: 100%;
}

.option {
	color: white;
	background-color: var(--black);
	padding: 1rem;
	transition: 0.3s;
}

.option--active {
	font-size: 1.5rem;
	color: black;
	background-color: rgb(255, 255, 255);
}

.option--title {
	pointer-events: none;
}

.reset-form {
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
	color: red;
	border: 1px solid red;
	background-color: #fdd;
	padding: 0.75rem;
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
