<template>
  <div>
    <h2>メール確認</h2>
    <div v-if="message">
      <p>{{ message }}</p>
      <p><router-link to="/login">ログインページへ</router-link></p>
    </div>
    <div v-if="errorMessage">
      <p style="color: red">{{ errorMessage }}</p>
      <p><router-link to="/register">再度登録を試みる</router-link></p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      message: '',
      errorMessage: '',
    }
  },
  async created() {
    const token = this.$route.params.token
    try {
      const response = await axios.get(
        `http://localhost:8000/api/verify-email/${token}/`
      )
      this.message = response.data.message
    } catch (error) {
      if (error.response && error.response.data) {
        this.errorMessage = error.response.data.error
      } else {
        this.errorMessage = 'メール確認に失敗しました。'
      }
    }
  },
}
</script>
