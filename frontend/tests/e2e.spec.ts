import { test, expect } from '@playwright/test'

test.describe('OpérIA E2E Operations, Auth & HITL Flow', () => {
  test('logs in and navigates through Dashboard, Agent, Operations, Data and Analytics', async ({ page }) => {
    // 1. Initial navigation redirects to /login when unauthenticated
    await page.goto('/')
    await expect(page).toHaveURL(/.*\/login/)
    await expect(page.locator('text=OpérIA')).toBeVisible()

    // 2. Perform Login with default credentials
    await page.fill('input[type="email"]', 'admin@operia.io')
    await page.fill('input[type="password"]', 'admin123')
    await page.click('button[type="submit"]')

    // 3. Dashboard after login
    await expect(page).toHaveURL('/')
    await expect(page.locator('text=Bonjour Alex')).toBeVisible()
    await expect(page.locator('text=Requêtes')).toBeVisible()

    // 4. Click "Examiner" to go to Agent view
    await page.click('text=Examiner')
    await expect(page).toHaveURL('/agent')
    await expect(page.locator('text=Factures impayées').first()).toBeVisible()
    await expect(page.locator('text=Mode contrôlé')).toBeVisible()

    // 5. Navigate to Opérations
    await page.locator('nav a[href="/operations"]').click()
    await expect(page).toHaveURL('/operations')
    await expect(page.locator('text=Valider la sélection')).toBeVisible()

    // 6. Navigate to Données
    await page.locator('nav a[href="/data"]').click()
    await expect(page).toHaveURL('/data')
    await expect(page.locator('text=sources métier connectées')).toBeVisible()

    // 7. Navigate to Analytics (Analytics)
    await page.locator('nav a[href="/analytics"]').click()
    await expect(page).toHaveURL('/analytics')
    await expect(page.locator('text=86 420 €').first()).toBeVisible()
    await expect(page.locator('h4:has-text("DSO")').first()).toBeVisible()
    await expect(page.locator('h4:has-text("Pareto")').first()).toBeVisible()

    // 8. Navigate to Settings (HITL Guardrails)
    await page.locator('nav a[href="/settings"]').click()
    await expect(page).toHaveURL('/settings')
    await expect(page.locator('text=Contrôle et validations')).toBeVisible()

    // 9. Navigate to Templates (Playbooks)
    await page.locator('nav a[href="/templates"]').click()
    await expect(page).toHaveURL('/templates')
    await expect(page.locator('text=Relance préventive J-5')).toBeVisible()

    // 10. Navigate to Admin Panel
    await page.locator('nav a[href="/admin"]').click()
    await expect(page).toHaveURL('/admin')
    await expect(page.locator('text=Administration').first()).toBeVisible()
    await expect(page.locator('text=Santé Système').first()).toBeVisible()

    // 11. Test Language Switcher (FR -> EN)
    await page.goto('/')
    await page.click('button:has-text("FR")')
    await expect(page.locator('button:has-text("EN")')).toBeVisible()
    await expect(page.locator('text=Welcome Alex')).toBeVisible()
  })

  test('tests all buttons in Conversations section: new, switch, search, prompts, and actions', async ({ page }) => {
    // 1. Log in
    await page.goto('/login')
    await page.fill('input[type="email"]', 'admin@operia.io')
    await page.fill('input[type="password"]', 'admin123')
    await page.click('button[type="submit"]')
    await expect(page).toHaveURL('/')

    // 2. Navigate to /agent
    await page.goto('/agent')
    await expect(page.locator('text=Factures impayées').first()).toBeVisible()

    // 3. Test "Nouveau" button to create a new conversation
    const newConvBtn = page.locator('button[title="Nouvelle conversation"]')
    await expect(newConvBtn).toBeVisible()
    await newConvBtn.click()

    // 4. Verify Empty State and Prompt Suggestions appear
    await expect(page.locator('text=Comment puis-je vous aider aujourd\'hui ?')).toBeVisible()
    const promptBtn = page.locator('text=Donne-moi les factures impayées depuis plus de 30 jours.')
    await expect(promptBtn).toBeVisible()

    // 5. Test Quick Prompt Click
    await promptBtn.click()
    await expect(page.locator('text=Donne-moi les factures impayées depuis plus de 30 jours.').first()).toBeVisible()

    // 6. Test Search input & clear button in sidebar
    const searchInput = page.locator('input[placeholder="Rechercher..."]')
    await searchInput.fill('export')
    await expect(page.locator('text=Export clients actifs')).toBeVisible()
    await expect(page.locator('text=Analyse des limites de crédit')).not.toBeVisible()

    // Click clear button (✕)
    const clearBtn = page.locator('button:has-text("✕")')
    await clearBtn.click()
    await expect(page.locator('text=Analyse des limites de crédit')).toBeVisible()

    // 7. Test switching conversation in sidebar
    await page.locator('text=Export clients actifs').first().click()
    await expect(page.locator('h1:has-text("Export clients actifs")')).toBeVisible()
    await expect(page.locator('text=Export préparé pour 42 comptes')).toBeVisible()

    // 8. Test Tool Execution accordion toggle button
    const toolsBtn = page.locator('button:has-text("Outils utilisés")').first()
    if (await toolsBtn.isVisible()) {
      await toolsBtn.click()
      await expect(page.locator('text=crm.comptes.enrich').first()).toBeVisible()
    }
  })
})
