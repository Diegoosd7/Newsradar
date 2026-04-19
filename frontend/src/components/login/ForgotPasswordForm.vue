<template>
	<div class="login-form">
		<p v-if="sent" class="success-msg">
			Si existe una cuenta con ese email, recibirás instrucciones para restablecer tu contraseña.
		</p>
		<template v-if="!sent">
			<p class="info-text">
				Introduce tu email y te enviaremos un enlace para restablecer tu contraseña.
			</p>
			<label>
				EMAIL
				<input v-model="email" type="email" name="email" autocomplete="email" />
			</label>
			<button @click="sendForm" :disabled="loading" class="form-button">
				{{ loading ? 'ENVIANDO...' : 'ENVIAR ENLACE' }}
			</button>
		</template>
		<button @click="emit('back-to-login')" class="back-button">
			← Volver al inicio de sesión
		</button>
	</div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const emit = defineEmits<{ 'back-to-login': [] }>()

const email = ref('')
const loading = ref(false)
const sent = ref(false)

const sendForm = async () => {
	if (!email.value) return
	loading.value = true
	// El backend aún no tiene endpoint de recuperación de contraseña.
	// Simulamos un delay y mostramos el mensaje de éxito genérico.
	await new Promise((resolve) => setTimeout(resolve, 800))
	loading.value = false
	sent.value = true
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

.info-text {
	color: #555;
	font-size: 0.9rem;
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

.back-button {
	background: none;
	border: none;
	color: gray;
	text-decoration: underline;
	cursor: pointer;
	font-size: 0.85rem;
	text-align: left;
	padding: 0;
}

.success-msg {
	color: green;
	border: 1px solid green;
	background-color: #d5f1d5;
	padding: 0.75rem;
	font-size: 0.9rem;
}
</style>
