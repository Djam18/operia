export type CurrencyCode = 'EUR' | 'XOF' | 'XAF' | 'MAD' | 'KES' | 'USD'

export interface CurrencyPreset {
  code: CurrencyCode
  symbol: string
  label: string
  typicalAvg: number
  min: number
  max: number
  step: number
}

export const CURRENCY_PRESETS: Record<CurrencyCode, CurrencyPreset> = {
  EUR: {
    code: 'EUR',
    symbol: '€',
    label: 'EUR (€)',
    typicalAvg: 3800,
    min: 500,
    max: 25000,
    step: 500,
  },
  XOF: {
    code: 'XOF',
    symbol: 'FCFA',
    label: 'FCFA (UEMOA / CEMAC)',
    typicalAvg: 2500000,
    min: 200000,
    max: 20000000,
    step: 100000,
  },
  XAF: {
    code: 'XAF',
    symbol: 'FCFA',
    label: 'FCFA (CEMAC)',
    typicalAvg: 2500000,
    min: 200000,
    max: 20000000,
    step: 100000,
  },
  MAD: {
    code: 'MAD',
    symbol: 'MAD',
    label: 'MAD (Dirham Marocain)',
    typicalAvg: 42000,
    min: 5000,
    max: 300000,
    step: 5000,
  },
  KES: {
    code: 'KES',
    symbol: 'KES',
    label: 'KES (Shilling Kenyan)',
    typicalAvg: 450000,
    min: 20000,
    max: 2000000,
    step: 20000,
  },
  USD: {
    code: 'USD',
    symbol: '$',
    label: 'USD ($)',
    typicalAvg: 4200,
    min: 500,
    max: 30000,
    step: 500,
  },
}

export function formatCurrency(amount: number, currency: string = 'EUR'): string {
  const rounded = Math.round(amount)
  const formattedNumber = rounded.toLocaleString('fr-FR')
  const upper = (currency || 'EUR').trim().toUpperCase()

  switch (upper) {
    case 'EUR':
    case '€':
      return `${formattedNumber} €`
    case 'XOF':
    case 'XAF':
    case 'FCFA':
      return `${formattedNumber} FCFA`
    case 'MAD':
    case 'DH':
      return `${formattedNumber} MAD`
    case 'KES':
      return `${formattedNumber} KES`
    case 'USD':
    case '$':
      return `$${rounded.toLocaleString('en-US')}`
    default:
      return `${formattedNumber} ${currency}`
  }
}
