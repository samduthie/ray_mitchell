const SPEECH_ICON = `<svg class="chat-widget__trigger-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32" fill="currentColor" fill-rule="nonzero" aria-hidden="true">
  <path d="M16 2C8.28 2 2 7.8 2 14.93a12.144 12.144 0 001.696 6.15l-1.668 7.51A1.16 1.16 0 003.63 29.9l6.914-3.072A14.835 14.835 0 0016 27.861c7.72 0 14-5.8 14-12.93S23.72 2 16 2zm4.508 16.32h-9.016a1.16 1.16 0 010-2.32h9.016a1.16 1.16 0 010 2.32zm0-4.638h-9.016a1.16 1.16 0 010-2.318h9.016a1.16 1.16 0 110 2.318z"/>
</svg>`

const EMOJI_ICON = `<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
  <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.5"/>
  <path d="M8.5 10h.01M15.5 10h.01" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
  <path d="M8.5 14.5c1 1.5 2.2 2 3.5 2s2.5-.5 3.5-2" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
</svg>`

const ATTACH_ICON = `<svg viewBox="0 0 24 24" fill="none" aria-hidden="true">
  <path d="M8.5 12.5l6.2-6.2a3 3 0 1 1 4.2 4.2l-7.5 7.5a5 5 0 0 1-7.1-7.1l8-8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
</svg>`

export function initChatWidget(root: HTMLElement): void {
  root.innerHTML = `
    <div class="chat-widget">
      <div class="chat-widget__panel" id="chat-panel" hidden role="dialog" aria-labelledby="chat-title" aria-modal="true">
        <div class="chat-widget__header">
          <div class="chat-widget__header-text">
            <h2 class="chat-widget__title" id="chat-title">Ray Mitchell: Psychotherapist and Wellbeing Consultant</h2>
            <div class="chat-widget__status">
              <span class="chat-widget__status-dot" aria-hidden="true"></span>
              <span>We'll reply as soon as we can</span>
            </div>
          </div>
          <button type="button" class="chat-widget__close" id="chat-close" aria-label="Close chat">×</button>
        </div>
        <div class="chat-widget__messages" id="chat-messages">
          <p class="chat-widget__placeholder">Send a message to start a conversation.</p>
        </div>
        <form class="chat-widget__footer" id="chat-form">
          <input
            type="text"
            class="chat-widget__input"
            id="chat-input"
            placeholder="Write your message..."
            autocomplete="off"
            aria-label="Message"
          />
          <button type="button" class="chat-widget__icon-btn" tabindex="-1" aria-hidden="true" disabled>${EMOJI_ICON}</button>
          <button type="button" class="chat-widget__icon-btn" tabindex="-1" aria-hidden="true" disabled>${ATTACH_ICON}</button>
        </form>
      </div>
      <button
        type="button"
        class="chat-widget__trigger"
        id="chat-trigger"
        aria-expanded="false"
        aria-controls="chat-panel"
        aria-label="Open chat"
      >
        ${SPEECH_ICON}
        <span class="chat-widget__trigger-label">Let's Chat!</span>
      </button>
    </div>
  `

  const trigger = root.querySelector<HTMLButtonElement>('#chat-trigger')!
  const panel = root.querySelector<HTMLDivElement>('#chat-panel')!
  const closeBtn = root.querySelector<HTMLButtonElement>('#chat-close')!
  const form = root.querySelector<HTMLFormElement>('#chat-form')!
  const input = root.querySelector<HTMLInputElement>('#chat-input')!
  const messages = root.querySelector<HTMLDivElement>('#chat-messages')!

  const open = () => {
    panel.hidden = false
    trigger.setAttribute('aria-expanded', 'true')
    input.focus()
  }

  const close = () => {
    panel.hidden = true
    trigger.setAttribute('aria-expanded', 'false')
    trigger.focus()
  }

  trigger.addEventListener('click', () => {
    if (panel.hidden) open()
    else close()
  })

  closeBtn.addEventListener('click', close)

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && !panel.hidden) close()
  })

  form.addEventListener('submit', (e) => {
    e.preventDefault()
    const text = input.value.trim()
    if (!text) return

    const placeholder = messages.querySelector('.chat-widget__placeholder')
    placeholder?.remove()

    const notice = document.createElement('p')
    notice.className = 'chat-widget__notice'
    notice.textContent =
      'Thanks for your message. Message delivery will be enabled soon — for now please email ray@raymitchell.co.uk.'
    messages.appendChild(notice)
    input.value = ''
    input.disabled = true
  })
}
