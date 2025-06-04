import { render } from '@testing-library/react'
import App from './App'
import { BrowserRouter } from 'react-router-dom'
import { describe, it, expect } from 'vitest'

describe('App', () => {
  it('renders without crashing', () => {
    render(
      <BrowserRouter>
        <App />
      </BrowserRouter>
    )
    expect(true).toBe(true)
  })
})
