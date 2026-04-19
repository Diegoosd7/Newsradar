<template>
	<div class="personal-info">
		<div class="personal-info-section">
			<p class="title">INFORMACIÓN PERSONAL</p>
			<p v-if="error" class="error-msg">{{ error }}</p>
			<p v-if="success" class="success-msg">Datos actualizados correctamente.</p>
			<div class="form">
				<label>
					NOMBRE
					<input v-model="fields.first_name" type="text" name="first_name" />
				</label>
				<label>
					APELLIDOS
					<input v-model="fields.last_name" type="text" name="last_name" />
				</label>
				<label>
					ORGANIZACIÓN
					<input v-model="fields.organization" type="text" name="organization" />
				</label>
				<label>
					EMAIL
					<input v-model="fields.email" type="email" name="email" />
				</label>
			</div>
			<button @click="saveProfile" :disabled="loading" class="form-button">
				{{ loading ? 'GUARDANDO...' : 'EDITAR' }}
			</button>
		</div>
		<div class="personal-info-section">
			<p class="title">CAMBIAR CONTRASEÑA</p>
			<p v-if="pwError" class="error-msg">{{ pwError }}</p>
			<p v-if="pwSuccess" class="success-msg">Contraseña actualizada correctamente.</p>
			<label>
				NUEVA CONTRASEÑA
				<input v-model="newPassword" type="password" name="new_password" autocomplete="new-password" />
			</label>
			<button @click="savePassword" :disabled="pwLoading" class="form-button">
				{{ pwLoading ? 'GUARDANDO...' : 'CAMBIAR CONTRASEÑA' }}
			</button>
		</div>
		<button @click="deleteAccount" class="delete-account-button">BORRAR LA CUENTA</button>
	</div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useApiCall } from '@/api/useApiCall'

const auth = useAuthStore()
const api = useApiCall()
const router = useRouter()

const fields = reactive({
	first_name: '',
	last_name: '',
	organization: '',
	email: '',
})

onMounted(() => {
	if (auth.user) {
		fields.first_name = auth.user.first_name
		fields.last_name = auth.user.last_name
		fields.organization = auth.user.organization
		fields.email = auth.user.email
	}
})

const loading = ref(false)
const error = ref('')
const success = ref(false)

const saveProfile = async () => {
	error.value = ''
	success.value = false
	if (!auth.user || !auth.token) return
	loading.value = true
	try {
		const [updated, roles] = await Promise.all([
			api.updateUser(auth.token, auth.user.id, {
				first_name: fields.first_name,
				last_name: fields.last_name,
				organization: fields.organization,
				email: fields.email,
			}),
			api.getRoles(auth.token),
		])
		auth.updateUser(updated, roles)
		success.value = true
	} catch (e: unknown) {
		error.value = e instanceof Error ? e.message : 'Error al actualizar.'
	} finally {
		loading.value = false
	}
}

const newPassword = ref('')
const pwLoading = ref(false)
const pwError = ref('')
const pwSuccess = ref(false)

const savePassword = async () => {
	pwError.value = ''
	pwSuccess.value = false
	if (!auth.user || !auth.token) return
	if (newPassword.value.length < 6) {
		pwError.value = 'La contraseña debe tener al menos 6 caracteres.'
		return
	}
	pwLoading.value = true
	try {
		const [updated, roles] = await Promise.all([
			api.updateUser(auth.token, auth.user.id, { password: newPassword.value }),
			api.getRoles(auth.token),
		])
		auth.updateUser(updated, roles)
		newPassword.value = ''
		pwSuccess.value = true
	} catch (e: unknown) {
		pwError.value = e instanceof Error ? e.message : 'Error al cambiar contraseña.'
	} finally {
		pwLoading.value = false
	}
}

const deleteAccount = async () => {
	if (!auth.user || !auth.token) return
	if (!confirm('¿Seguro que quieres borrar tu cuenta? Esta acción no se puede deshacer.')) return
	try {
		await api.deleteUser(auth.token, auth.user.id)
		auth.logout()
		router.push({ name: 'login' })
	} catch (e: unknown) {
		error.value = e instanceof Error ? e.message : 'Error al borrar la cuenta.'
	}
}
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
	gap: 1rem;
}

label {
	display: flex;
	flex-direction: column;
	gap: 0.2rem;
}

input {
	padding: 0.5rem;
	border: 1px solid black;
	background-color: white;
}

.title {
	font-size: 1.2rem;
	font-weight: bold;
	text-align: center;
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

.delete-account-button {
	padding: 1rem;
	color: rgb(203, 61, 61);
	border: 1px solid rgb(203, 61, 61);
	transition: 0.3s;
}

.delete-account-button:hover {
	background-color: rgb(241, 210, 210);
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
	padding: 0.5rem;
	font-size: 0.9rem;
}
</style>
