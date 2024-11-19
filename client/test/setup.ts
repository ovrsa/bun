import { server } from '../mocks/server'
import { beforeAll, afterEach, afterAll } from 'vitest'
import { expect } from 'vitest'
import matchers from '@testing-library/jest-dom/matchers'

expect.extend(matchers)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())
