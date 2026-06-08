import { initChatWidget } from './chat-widget'

function initSmoothScroll(): void {
  document.querySelectorAll<HTMLAnchorElement>('a[href*="#"]').forEach((link) => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href')
      if (!href || !href.includes('#')) return

      const hash = href.slice(href.indexOf('#'))
      if (hash === '#') return

      const onHome = window.location.pathname === '/' || window.location.pathname === '/index.html'
      if (!onHome && href.startsWith('/#')) {
        return
      }

      const target = document.querySelector(hash)
      if (!target) return

      e.preventDefault()
      target.scrollIntoView({ behavior: 'smooth', block: 'start' })
      history.pushState(null, '', hash)
    })
  })
}

function initServicesHashScroll(): void {
  if (window.location.hash !== '#services') return
  const target = document.getElementById('services')
  if (!target) return
  requestAnimationFrame(() => {
    target.scrollIntoView({ behavior: 'smooth', block: 'start' })
  })
}

function initMotionEnter(): void {
  const motionIds = [
    'comp-j6w6mgxq',
    'comp-j6w888ep',
    'comp-j6w6mgy4',
    'comp-mfo1u4y8',
  ]

  motionIds.forEach((id) => {
    const el = document.getElementById(id)
    if (!el) return
    el.addEventListener('animationend', () => {
      el.dataset.motionEnter = 'done'
    })
  })
}

function initSkipToContent(): void {
  const skipBtn = document.getElementById('SKIP_TO_CONTENT_BTN')
  const main = document.getElementById('PAGES_CONTAINER')
  if (skipBtn && main) {
    skipBtn.addEventListener('click', () => {
      main.focus()
      main.scrollIntoView({ behavior: 'smooth' })
    })
  }
}

const chatRoot = document.getElementById('chat-widget-root')
if (chatRoot) initChatWidget(chatRoot)

initSmoothScroll()
initServicesHashScroll()
initMotionEnter()
initSkipToContent()
