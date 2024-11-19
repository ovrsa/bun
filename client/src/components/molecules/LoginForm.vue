<template>
  <form @submit.prevent="onSubmit" class="space-y-6">
    <h2 class="text-2xl mb-20 text-center">Login</h2>

    <InputField
      type="email"
      v-model="email"
      placeholder="Email"
      :errorMessage="errors.email ? 'Email is required.' : ''"
    />

    <InputField
      type="password"
      v-model="password"
      placeholder="Password"
      :errorMessage="errors.password ? 'Password is required.' : ''"
    />

    <!-- <div class="text-center pt-5">
      <a href="" class="text-blue-600 text-sm hover:underline">
        Forgot your password?
      </a>
    </div> -->

    <Button type="submit">Log In</Button>

    <div class="text-center">
      <span class="text-sm text-gray-700">Don't have an account?</span>
      <a href="/signup" class="text-blue-600 text-sm hover:underline">
        Sign up now
      </a>
    </div>

    <div v-if="errorMessage" class="mt-4 text-red-500 text-center">
      {{ errorMessage }}
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import type { AxiosError } from 'axios'
import InputField from '@/components/atoms/InputField.vue'
import Button from '@/components/atoms/Button.vue'
import apiClient from '@/services/auth'

const email = ref('')
const password = ref('')
const errors = ref({ email: false, password: false })
const errorMessage = ref('')

const store = useStore()
const router = useRouter()

const onSubmit = async () => {
  errors.value.email = !email.value
  errors.value.password = !password.value

  if (!errors.value.email && !errors.value.password) {
    try {
      const response = await apiClient.post('login/', {
        email: email.value,
        password: password.value,
      })
      await store.dispatch('auth/checkAuth')
      router.push('/')
    } catch (err: unknown) {
      const error = err as AxiosError

      if (error.response && error.response.data) {
        errorMessage.value = Object.values(
          error.response.data as Record<string, any>
        )
          .reduce((acc, val) => acc.concat(val), [])
          .join(' ')
      } else {
        errorMessage.value = 'ログインに失敗しました。'
        console.error(`ログインに失敗しました。${error}`)
      }
    }
  }
}
</script>
