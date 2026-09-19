import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import UiCard from '../src/components/ui/UiCard.vue'
import UiBadge from '../src/components/ui/UiBadge.vue'
import UiButton from '../src/components/ui/UiButton.vue'
import UiDialog from '../src/components/ui/UiDialog.vue'
import UiTabs from '../src/components/ui/UiTabs.vue'

describe('UI Primitives Suite', () => {
  it('renders UiCard with slots and border variants', () => {
    const wrapper = mount(UiCard, {
      props: { borderVariant: 'warning' },
      slots: {
        header: 'Card Header Title',
        default: 'Main Card Content',
        footer: 'Card Footer Actions',
      },
    })

    expect(wrapper.text()).toContain('Card Header Title')
    expect(wrapper.text()).toContain('Main Card Content')
    expect(wrapper.text()).toContain('Card Footer Actions')
    expect(wrapper.classes()).toContain('border-amber-200/90')
  })

  it('renders UiBadge with different variants', () => {
    const wrapperSuccess = mount(UiBadge, {
      props: { variant: 'success' },
      slots: { default: 'Active' },
    })
    expect(wrapperSuccess.text()).toBe('Active')
    expect(wrapperSuccess.classes()).toContain('bg-emerald-100')

    const wrapperWarning = mount(UiBadge, {
      props: { variant: 'warning' },
      slots: { default: 'Pending' },
    })
    expect(wrapperWarning.classes()).toContain('bg-amber-100')
  })

  it('renders UiButton with loading state and emits click', async () => {
    const wrapper = mount(UiButton, {
      props: { loading: false },
      slots: { default: 'Submit Action' },
    })

    expect(wrapper.text()).toContain('Submit Action')
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toHaveLength(1)

    // With loading
    await wrapper.setProps({ loading: true })
    expect(wrapper.find('svg.animate-spin').exists()).toBe(true)
    expect(wrapper.attributes('disabled')).toBeDefined()
  })

  it('renders UiTabs and emits update:modelValue on tab click', async () => {
    const items = [
      { label: 'All', value: 'ALL', badge: 10 },
      { label: 'Pending', value: 'PENDING', badge: 3 },
    ]

    const wrapper = mount(UiTabs, {
      props: {
        items,
        modelValue: 'ALL',
      },
    })

    expect(wrapper.text()).toContain('All')
    expect(wrapper.text()).toContain('Pending')
    expect(wrapper.text()).toContain('10')

    const buttons = wrapper.findAll('button')
    await buttons[1].trigger('click')
    expect(wrapper.emitted('update:modelValue')?.[0]).toEqual(['PENDING'])
  })

  it('renders UiDialog when open is true', () => {
    const wrapper = mount(UiDialog, {
      props: { open: true },
      slots: {
        title: 'Action Details Dialog',
        default: 'Dialog Body Content',
      },
    })

    expect(wrapper.html()).toBeDefined()
  })
})
