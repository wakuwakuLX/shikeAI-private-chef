const FAVORITES_KEY = 'shikeai_favorites'
const HISTORY_KEY = 'shikeai_history'
const SETTINGS_KEY = 'shikeai_settings'

export function getLocalFavorites() {
  try {
    const data = uni.getStorageSync(FAVORITES_KEY)
    return data ? JSON.parse(data) : []
  } catch (e) {
    return []
  }
}

export function saveLocalFavorite(recipe) {
  const favorites = getLocalFavorites()
  const exists = favorites.some(f => f.id === recipe.id)
  if (!exists) {
    favorites.unshift(recipe)
    uni.setStorageSync(FAVORITES_KEY, JSON.stringify(favorites))
    return true
  }
  return false
}

export function removeLocalFavorite(recipeId) {
  const favorites = getLocalFavorites()
  const filtered = favorites.filter(f => f.id !== recipeId)
  uni.setStorageSync(FAVORITES_KEY, JSON.stringify(filtered))
}

export function isLocalFavorite(recipeId) {
  const favorites = getLocalFavorites()
  return favorites.some(f => f.id === recipeId)
}

export function getLocalHistory() {
  try {
    const data = uni.getStorageSync(HISTORY_KEY)
    return data ? JSON.parse(data) : []
  } catch (e) {
    return []
  }
}

export function saveLocalHistory(item) {
  const history = getLocalHistory()
  history.unshift(item)
  if (history.length > 50) {
    history.pop()
  }
  uni.setStorageSync(HISTORY_KEY, JSON.stringify(history))
}

export function removeLocalHistory(id) {
  const history = getLocalHistory()
  const filtered = history.filter(h => h.id !== id)
  uni.setStorageSync(HISTORY_KEY, JSON.stringify(filtered))
}

export function getSettings() {
  try {
    const data = uni.getStorageSync(SETTINGS_KEY)
    return data ? JSON.parse(data) : {}
  } catch (e) {
    return {}
  }
}

export function saveSettings(settings) {
  uni.setStorageSync(SETTINGS_KEY, JSON.stringify(settings))
}
