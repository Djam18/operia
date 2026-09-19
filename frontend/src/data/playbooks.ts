export interface Playbook {
  id: string
  title: string
  description: string
  category: 'Finance' | 'CRM' | 'Audit'
  badgeVariant: 'default' | 'success' | 'warning' | 'destructive' | 'secondary'
  source: string
  duration: string
  defaultPrompt: string
}

export const PLAYBOOKS: Playbook[] = [
  {
    id: 'pb-1',
    title: 'Relance préventive J-5',
    description: 'Notifie par courriel les clients de leur prochaine échéance pour accélérer les encaissements.',
    category: 'Finance',
    badgeVariant: 'default',
    source: 'ERP + Messagerie',
    duration: '< 15s',
    defaultPrompt: 'Prépare les relances préventives pour toutes les factures à échéance dans 5 jours.',
  },
  {
    id: 'pb-2',
    title: 'Recouvrement créances > 30j',
    description: 'Isole les retards, vérifie les litiges CRM et prépare les relances de niveau 2.',
    category: 'Finance',
    badgeVariant: 'warning',
    source: 'Finance + CRM',
    duration: '< 20s',
    defaultPrompt: 'Quelles factures dépassent 30 jours de retard ? Prépare les relances pour les clients sans litige.',
  },
  {
    id: 'pb-3',
    title: 'Revue des plafonds d’encours VIP',
    description: 'Ajuste les limites de crédit dans l’ERP pour les 10 meilleurs payeurs de l’année.',
    category: 'CRM',
    badgeVariant: 'success',
    source: 'ERP Crédit',
    duration: '< 10s',
    defaultPrompt: 'Analyse les 10 meilleurs clients en volume et propose une augmentation de 15 % de leur plafond d’encours.',
  },
  {
    id: 'pb-4',
    title: 'Audit des commandes bloquées',
    description: 'Identifie les goulots d’étranglement logistiques et alerte les responsables d’approvisionnement.',
    category: 'Audit',
    badgeVariant: 'destructive',
    source: 'ERP Commandes',
    duration: '< 30s',
    defaultPrompt: 'Liste toutes les commandes avec statut bloqué et résume la cause racine.',
  },
  {
    id: 'pb-5',
    title: 'Export TVA & Grand Livre',
    description: 'Génère un fichier certifié des écritures fiscales pour la clôture comptable.',
    category: 'Audit',
    badgeVariant: 'secondary',
    source: 'Base financière',
    duration: '< 25s',
    defaultPrompt: 'Prépare un export certifié du grand livre comptable pour le trimestre en cours.',
  },
  {
    id: 'pb-6',
    title: 'Campagne de recouvrement Panafrique',
    description: 'Filtre les comptes UEMOA & CEMAC en FCFA et prépare une relance WhatsApp/Email.',
    category: 'Finance',
    badgeVariant: 'default',
    source: 'ERP International',
    duration: '< 18s',
    defaultPrompt: 'Isole tous les comptes en zone FCFA (XOF/XAF) avec plus de 15 jours de retard et prépare les notifications.',
  },
]
