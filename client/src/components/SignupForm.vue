<template>
  <form @submit.prevent="onSubmit" class="space-y-6">
    <h2 class="text-2xl mb-8 text-center">Create Account</h2>

    <!-- email -->
    <div>
      <input
        id="email"
        type="email"
        v-model="email"
        class="w-full p-2 border border-gray-300 rounded-lg bg-white bg-opacity-50 placeholder-gray-400"
        placeholder="Email"
      />
      <p v-if="errors.email" class="text-red-500 text-xs mt-1">
        Email is required.
      </p>
    </div>

    <!-- password -->
    <div>
      <input
        id="password"
        type="password"
        v-model="password"
        class="w-full p-2 border border-gray-300 rounded-lg bg-white bg-opacity-50 placeholder-gray-400"
        placeholder="Password"
      />
      <p v-if="errors.password" class="text-red-500 text-xs mt-1">
        Password is required.
      </p>
    </div>

    <!-- Submit -->
    <button type="submit" class="w-full bg-blue-600 text-white p-2 rounded-lg">
      Create Account
    </button>

    <div class="mt-6 text-center">
      <span class="text-sm text-gray-700">Already have an account?</span>
      <a href="/login" class="text-blue-600 text-sm hover:underline"
        >Login now</a
      >
    </div>
  </form>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const email = ref('');
const password = ref('');
const errors = ref({ email: false, password: false });

// const { handleEmailSignup } = useEmailSignup();

const onSubmit = () => {
  // バリデーション
  if (!email.value) {
    errors.value.email = true;
  } else {
    errors.value.email = false;
  }

  if (!password.value) {
    errors.value.password = true;
  } else {
    errors.value.password = false;
  }

  if (!errors.value.email && !errors.value.password) {
    // handleEmailSignup({ email: email.value, password: password.value });
  }
};
</script>

<style scoped></style>
