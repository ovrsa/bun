// src/tests/user.test.ts
import { describe, it, expect } from 'vitest'
import axios from 'axios'

describe('API tests', () => {
  it('should return user data', async () => {
    const response = await axios.get('/api/user')
    expect(response.data).toEqual({ id: 1, name: 'John Doe' })
  })

  it('should return a token on login', async () => {
    const response = await axios.post('/api/login')
    expect(response.data).toEqual({ token: 'fake-token' })
  })
})
