import { describe, it, expect } from 'vitest'
import { formatCurrency, CURRENCY_PRESETS } from '../src/utils/currency'
import { useI18n } from '../src/composables/useI18n'
import { useAnalytics } from '../src/composables/useAnalytics'

describe('Composables & Utilities Suite', () => {
  describe('formatCurrency', () => {
    it('formats EUR correctly with space and euro symbol', () => {
      const formatted = formatCurrency(86420, 'EUR')
      expect(formatted).toContain('86')
      expect(formatted).toContain('420')
      expect(formatted).toContain('€')
    })

    it('formats XOF / FCFA correctly', () => {
      const formatted = formatCurrency(18200000, 'XOF')
      expect(formatted).toContain('18')
      expect(formatted).toContain('FCFA')
    })

    it('formats MAD (Moroccan Dirham) correctly', () => {
      const formatted = formatCurrency(450000, 'MAD')
      expect(formatted).toContain('450')
      expect(formatted).toContain('MAD')
    })

    it('formats KES (Kenyan Shilling) correctly', () => {
      const formatted = formatCurrency(850000, 'KES')
      expect(formatted).toContain('850')
      expect(formatted).toContain('KES')
    })

    it('formats USD with dollar sign correctly', () => {
      const formatted = formatCurrency(12500, 'USD')
      expect(formatted).toContain('$')
      expect(formatted).toContain('12,500')
    })

    it('handles zero and missing currency fallback', () => {
      expect(formatCurrency(0, 'EUR')).toContain('0')
      expect(formatCurrency(100)).toContain('100')
    })
  })

  describe('useI18n', () => {
    it('translates nested paths and performs variable interpolation', () => {
      const { t, setLocale, locale } = useI18n()
      setLocale('fr')
      expect(locale.value).toBe('fr')
      expect(t('nav.dashboard')).toBe('Dashboard')
      expect(t('dashboard.welcome')).toBe('Bonjour Alex')
      expect(t('agent.invoices_identified', { count: 42 })).toContain('42')

      setLocale('en')
      expect(locale.value).toBe('en')
      expect(t('dashboard.welcome')).toBe('Welcome Alex')
      expect(t('agent.invoices_identified', { count: 42 })).toContain('42')

      // Reset to French for other tests
      setLocale('fr')
    })

    it('returns path string if key is not found', () => {
      const { t } = useI18n()
      expect(t('non_existent.nested.key')).toBe('non_existent.nested.key')
    })
  })

  describe('useAnalytics', () => {
    it('initializes with EUR and scales values upon currency switch', () => {
      const { t } = useI18n()
      const { selectedCurrency, currentRecoveredAmount, supportedCurrencies } = useAnalytics(t)
      expect(selectedCurrency.value).toBe('EUR')
      expect(currentRecoveredAmount.value).toBe(86420)
      expect(supportedCurrencies.length).toBe(4)

      selectedCurrency.value = 'XOF'
      expect(selectedCurrency.value).toBe('XOF')
      expect(currentRecoveredAmount.value).toBe(56680000)

      selectedCurrency.value = 'EUR'
      expect(selectedCurrency.value).toBe('EUR')
      expect(currentRecoveredAmount.value).toBe(86420)
    })
  })
})
