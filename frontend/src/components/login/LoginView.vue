<template>
	<div class="view">
		<div class="login-register-modal">
			<template v-if="activeForm !== 'FORGOT_PASSWORD'">
				<div class="options">
					<button
						@click="activeForm = 'LOGIN'"
						:class="['option', activeForm === 'LOGIN' ? 'option--active' : '']"
					>
						LOGIN
					</button>
					<button
						@click="activeForm = 'REGISTER'"
						:class="['option', activeForm === 'REGISTER' ? 'option--active' : '']"
					>
						REGISTRO
					</button>
				</div>
				<LoginForm v-if="activeForm === 'LOGIN'" @forgot-password="activeForm = 'FORGOT_PASSWORD'" />
				<RegisterForm v-else />
			</template>
			<template v-else>
				<div class="options">
					<div class="option option--active option--title">RECUPERAR CONTRASEÑA</div>
				</div>
				<ForgotPasswordForm @back-to-login="activeForm = 'LOGIN'" />
			</template>
		</div>
	</div>
</template>

<script setup lang="ts">
import LoginForm from './LoginForm.vue'
import RegisterForm from './RegisterForm.vue'
import ForgotPasswordForm from './ForgotPasswordForm.vue'
import { ref } from 'vue'

const activeForm = ref<'LOGIN' | 'REGISTER' | 'FORGOT_PASSWORD'>('LOGIN')
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
	grid-template-columns: 1fr 1fr;
	width: 100%;
}

.option {
	color: white;
	background-color: var(--black);
	padding: 1rem;
	transition: 0.3s;
}

.option--active,
.option:hover {
	font-size: 1.5rem;
	color: black;
	background-color: rgb(255, 255, 255);
}

.option--title {
	grid-column: 1 / -1;
	pointer-events: none;
}
</style>
