import '@testing-library/jest-dom/vitest'
import { afterAll, beforeAll } from 'vitest'

beforeAll(() => {
  console.log('beforeAll')
})
afterAll(() => {
  console.log('afterAll')
})
