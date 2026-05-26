import DefaultTheme from 'vitepress/theme'
import './style.css'

export default {
  extends: DefaultTheme,
  enhanceApp({ router }) {
    if (typeof window === 'undefined') return

    // 创建 iOS 风格加载遮罩
    const overlay = document.createElement('div')
    overlay.className = 'loading-overlay'
    overlay.innerHTML = '<div class="loading-spinner"></div>'
    document.body.appendChild(overlay)

    let timer: ReturnType<typeof setTimeout> | null = null
    let startTime = 0

    router.onBeforeRouteChange = () => {
      startTime = Date.now()
      overlay.classList.add('active')
    }

    router.onAfterRouteChanged = () => {
      const elapsed = Date.now() - startTime
      const delay = Math.max(0, 400 - elapsed)

      if (timer) clearTimeout(timer)
      timer = setTimeout(() => {
        overlay.classList.remove('active')
      }, delay)
    }
  }
}
