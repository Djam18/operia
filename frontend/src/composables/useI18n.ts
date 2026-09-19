import { ref, computed } from 'vue'
import frDict from '../locales/fr.json'
import enDict from '../locales/en.json'

export type Locale = 'fr' | 'en'

const currentLocale = ref<Locale>('fr')

type DictNode = string | { [key: string]: DictNode }

const dicts: Record<Locale, Record<string, DictNode>> = {
  fr: frDict,
  en: enDict,
}

export function useI18n() {
  const t = (path: string, params?: Record<string, string | number>): string => {
    const keys = path.split('.')
    let current: DictNode = dicts[currentLocale.value]

    for (const key of keys) {
      if (typeof current === 'object' && current !== null && key in current) {
        current = current[key]
      } else {
        return path
      }
    }

    if (typeof current !== 'string') {
      return path
    }

    let text = current
    if (params) {
      for (const [paramKey, val] of Object.entries(params)) {
        text = text.replace(new RegExp(`\\{${paramKey}\\}`, 'g'), String(val))
      }
    }

    return text
  }

  const setLocale = (loc: Locale) => {
    currentLocale.value = loc
  }

  const locale = computed(() => currentLocale.value)

  return { t, setLocale, locale }
}
