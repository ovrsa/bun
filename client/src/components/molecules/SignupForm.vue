<template>
  <form @submit.prevent="onSubmit" class="space-y-6">
    <h2 class="text-2xl mb-20 text-center">Create Account</h2>

    <InputField
      type="text"
      v-model="user.username"
      placeholder="Username"
      :errorMessage="errors.username ? 'Username is required.' : ''"
    />

    <InputField
      type="email"
      v-model="user.email"
      placeholder="Email"
      :errorMessage="errors.email ? 'Email is required.' : ''"
    />

    <InputField
      type="password"
      v-model="user.password"
      placeholder="Password"
      :errorMessage="errors.password ? 'Password is required.' : ''"
    />

    <InputField
      type="password"
      v-model="user.password_confirm"
      placeholder="Confirm Password"
      :errorMessage="
        errors.password_confirm ? 'Password confirmation is required.' : ''
      "
    />

    <Button type="submit">Create Account</Button>

    <div class="text-center">
      <span class="text-sm text-gray-700">Already have an account?</span>
      <a href="/login" class="text-blue-600 text-sm hover:underline"
        >Login now</a
      >
    </div>

    <Alert v-if="message" class="mt-4">
      <RocketIcon class="h-4 w-4 text-green-600" />
      <AlertTitle>Success!</AlertTitle>
      <AlertDescription>
        {{ message }}
      </AlertDescription>
    </Alert>

    <Alert v-if="errorMessage" class="mt-4" variant="destructive">
      <RocketIcon class="h-4 w-4 text-red-600" />
      <AlertTitle>Error!</AlertTitle>
      <AlertDescription>
        {{ errorMessage }}
      </AlertDescription>
    </Alert>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import InputField from '@/components/atoms/InputField.vue'
import Button from '@/components/atoms/Button.vue'
import { RocketIcon } from '@radix-icons/vue'
import apiClient from '@/services/auth'
import type { AxiosError } from 'axios'

const user = ref({
  username: '',
  email: '',
  password: '',
  password_confirm: '',
})

const message = ref('')
const errorMessage = ref('')
const errors = ref({
  username: false,
  email: false,
  password: false,
  password_confirm: false,
})

const onSubmit = async () => {
  errors.value.username = !user.value.username
  errors.value.email = !user.value.email
  errors.value.password = !user.value.password
  errors.value.password_confirm = !user.value.password_confirm

  if (
    !errors.value.username &&
    !errors.value.email &&
    !errors.value.password &&
    !errors.value.password_confirm
  ) {
    try {
      const response = await apiClient.post('register/', user.value)
      message.value =
        'ご登録のメールアドレスに確認メールをお送りしました。メール内のリンクをクリックして、アカウントを有効化してください。'
      errorMessage.value = ''

      user.value.username = ''
      user.value.email = ''
      user.value.password = ''
      user.value.password_confirm = ''
    } catch (err: unknown) {
      const error = err as AxiosError

      if (error.response && error.response.data) {
        const responseData = error.response.data as { [key: string]: string[] }
        errorMessage.value = Object.values(responseData)
          .reduce((acc, val) => acc.concat(val), [])
          .join(' ')
      } else {
        errorMessage.value = '登録に失敗しました。'
      }
    }
  }
}
</script>

<style scoped></style>
