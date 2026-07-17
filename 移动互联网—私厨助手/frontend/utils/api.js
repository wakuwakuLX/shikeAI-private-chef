const BASE_URL = 'http://localhost:8000'

export function request(url, method = 'GET', data = {}, timeout = 180000) {
  return new Promise((resolve, reject) => {
    uni.request({
      url: BASE_URL + url,
      method: method,
      data: data,
      header: {
        'Content-Type': 'application/json'
      },
      timeout: timeout,
      success: (res) => {
        if (res.statusCode === 200) {
          resolve(res.data)
        } else {
          reject(res)
        }
      },
      fail: (err) => {
        reject(err)
      }
    })
  })
}

export function generateRecipes(userRequest) {
  return request('/api/chat', 'POST', {
    user_request: userRequest
  })
}

export function getHistory(limit = 20) {
  return request(`/api/history?limit=${limit}`)
}

export function deleteHistory(historyId) {
  return request(`/api/history/${historyId}`, 'DELETE')
}

export function getFavorites() {
  return request('/api/favorites')
}

export function addFavorite(recipeData) {
  return request('/api/favorites', 'POST', recipeData)
}

export function removeFavorite(recipeId) {
  return request(`/api/favorites/${recipeId}`, 'DELETE')
}

export function getConversations() {
  return request('/api/conversations')
}

export function getConversationMessages(conversationId) {
  return request(`/api/conversations/${conversationId}/messages`)
}

export function deleteConversation(conversationId) {
  return request(`/api/conversations/${conversationId}`, 'DELETE')
}
