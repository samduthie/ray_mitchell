import { initChatWidget } from './chat-widget'

function initMobileNav(): void {
  const toggle = document.getElementById('nav-toggle')
  const nav = document.getElementById('site-nav')
  if (!toggle || !nav) return

  const setOpen = (open: boolean) => {
    nav.classList.toggle('is-open', open)
    toggle.setAttribute('aria-expanded', String(open))
    toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu')
  }

  toggle.addEventListener('click', () => {
    setOpen(!nav.classList.contains('is-open'))
  })

  nav.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', () => setOpen(false))
  })

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') setOpen(false)
  })
}

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

function initSkipToContent(): void {
  const skip = document.querySelector<HTMLAnchorElement>('.skip-link')
  const main = document.getElementById('main')
  if (!skip || !main) return
  skip.addEventListener('click', (e) => {
    e.preventDefault()
    main.focus()
    main.scrollIntoView({ behavior: 'smooth' })
  })
}

const chatRoot = document.getElementById('chat-widget-root')
if (chatRoot) initChatWidget(chatRoot)

initMobileNav()
initSmoothScroll()
initServicesHashScroll()
initSkipToContent()
