<template>
  <view class="container">
    <view class="page-header">
      <text class="page-title">📋 历史记录</text>
      <text class="page-desc">过往生成的菜谱记录</text>
      <view class="clear-all" @click="clearAll">
        <text>清空全部</text>
      </view>
    </view>

    <view v-if="history.length > 0" class="history-list">
      <view 
        v-for="(item, index) in history" 
        :key="index" 
        class="history-card"
      >
        <view class="card-header" @click="toggleExpand(item.id)">
          <text class="history-title">{{ item.title }}</text>
          <view class="header-right">
            <text class="history-time">{{ formatTime(item.created_at) }}</text>
            <text :class="['expand-icon', expandedId === item.id ? 'expanded' : '']">▼</text>
          </view>
        </view>
        <view class="card-content">
          <view v-if="getRecipes(item).length > 0" class="recipes-preview">
            <text class="preview-label">包含菜谱：</text>
            <text class="preview-names">{{ getRecipeNames(item).join('、') }}</text>
          </view>
        </view>
        <view v-if="expandedId === item.id" class="recipes-expand">
          <view 
            v-for="(recipe, idx) in getAllRecipes(item)" 
            :key="idx" 
            class="expand-recipe-item"
            @click="viewRecipe(recipe)"
          >
            <text class="expand-recipe-name">{{ recipe.name }}</text>
            <text class="expand-recipe-calories">🔥 {{ recipe.nutrition && recipe.nutrition.calories || 0 }} kcal</text>
            <text class="expand-arrow">→</text>
          </view>
        </view>
        <view class="card-actions">
          <view class="action-btn delete" @click.stop="deleteHistory(item)">
            <text>删除</text>
          </view>
        </view>
      </view>
    </view>

    <view v-else class="empty-state">
      <text class="empty-icon">📝</text>
      <text class="empty-title">暂无历史记录</text>
      <text class="empty-desc">生成菜谱后会自动保存到这里</text>
      <button class="btn-primary" @click="goHome">
        <text>去生成菜谱</text>
      </button>
    </view>
  </view>
</template>

<script>
import { getLocalHistory, removeLocalHistory } from '@/utils/storage'

export default {
  data() {
    return {
      history: [],
      expandedId: null
    }
  },
  onShow() {
    this.loadHistory()
  },
  methods: {
    loadHistory() {
      this.history = getLocalHistory()
    },
    getRecipes(item) {
      try {
        const data = JSON.parse(item.content)
        if (data.recipes && Array.isArray(data.recipes)) {
          return data.recipes
        }
        if (Array.isArray(data)) {
          return data
        }
        return []
      } catch (e) {
        return []
      }
    },
    getAllRecipes(item) {
      return this.getRecipes(item)
    },
    getRecipeNames(item) {
      const recipes = this.getRecipes(item)
      return recipes.slice(0, 5).map(r => r.name)
    },
    formatTime(timeStr) {
      if (!timeStr) return ''
      const date = new Date(timeStr)
      const month = date.getMonth() + 1
      const day = date.getDate()
      const hour = date.getHours().toString().padStart(2, '0')
      const minute = date.getMinutes().toString().padStart(2, '0')
      return `${month}月${day}日 ${hour}:${minute}`
    },
    toggleExpand(id) {
      this.expandedId = this.expandedId === id ? null : id
    },
    viewRecipe(recipe) {
      uni.navigateTo({
        url: `/pages/recipe-detail/recipe-detail?data=${encodeURIComponent(JSON.stringify(recipe))}`
      })
    },
    deleteHistory(item) {
      uni.showModal({
        title: '确认删除',
        content: '确定要删除这条记录吗？',
        success: (res) => {
          if (res.confirm) {
            removeLocalHistory(item.id)
            this.loadHistory()
            uni.showToast({ title: '已删除', icon: 'none' })
          }
        }
      })
    },
    clearAll() {
      uni.showModal({
        title: '确认清空',
        content: '确定要清空所有历史记录吗？',
        success: (res) => {
          if (res.confirm) {
            uni.setStorageSync('shikeai_history', '[]')
            this.loadHistory()
            uni.showToast({ title: '已清空', icon: 'none' })
          }
        }
      })
    },
    goHome() {
      uni.switchTab({
        url: '/pages/index/index'
      })
    }
  }
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  background: #FFF8F0;
  padding-bottom: 120rpx;
}

.page-header {
  background: linear-gradient(135deg, #FF8C42, #FFA76D);
  padding: 60rpx 32rpx;
  color: #FFFFFF;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10rpx 40rpx rgba(255, 140, 66, 0.3);
}

.page-header::after {
  content: '';
  position: absolute;
  top: -50rpx;
  right: -50rpx;
  width: 200rpx;
  height: 200rpx;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.page-title {
  font-size: 48rpx;
  font-weight: bold;
  display: block;
  position: relative;
  z-index: 1;
}

.page-desc {
  font-size: 28rpx;
  opacity: 0.95;
  margin-top: 12rpx;
  display: block;
  position: relative;
  z-index: 1;
}

.clear-all {
  position: absolute;
  right: 32rpx;
  top: 60rpx;
  font-size: 28rpx;
  background: rgba(255, 255, 255, 0.25);
  padding: 12rpx 24rpx;
  border-radius: 24rpx;
  position: relative;
  z-index: 1;
}

.history-list {
  padding: 24rpx;
}

.history-card {
  background: #FFFFFF;
  padding: 28rpx 32rpx;
  border-radius: 24rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 6rpx 24rpx rgba(255, 140, 66, 0.08);
  border: 1rpx solid rgba(255, 140, 66, 0.1);
  transition: all 0.3s ease;
}

.history-card:active {
  transform: scale(0.98);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16rpx;
}

.history-title {
  font-size: 34rpx;
  font-weight: 600;
  color: #5D4037;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.history-time {
  font-size: 26rpx;
  color: #998B7A;
}

.expand-icon {
  font-size: 24rpx;
  color: #CCCCCC;
  transition: transform 0.3s ease;
}

.expand-icon.expanded {
  transform: rotate(180deg);
}

.recipes-expand {
  background: #FFF8F0;
  border-radius: 16rpx;
  padding: 16rpx;
  margin-bottom: 16rpx;
  border: 1rpx solid #FFE0C8;
}

.expand-recipe-item {
  display: flex;
  align-items: center;
  padding: 20rpx;
  border-radius: 12rpx;
  margin-bottom: 12rpx;
  background: #FFFFFF;
  transition: all 0.3s ease;
}

.expand-recipe-item:last-child {
  margin-bottom: 0;
}

.expand-recipe-item:active {
  background: #FFF8F0;
}

.expand-recipe-name {
  font-size: 30rpx;
  font-weight: 600;
  color: #5D4037;
  flex: 1;
}

.expand-recipe-calories {
  font-size: 24rpx;
  color: #FF8C42;
  margin-right: 16rpx;
}

.expand-arrow {
  font-size: 32rpx;
  color: #CCCCCC;
}

.card-content {
  margin-bottom: 20rpx;
}

.preview-label {
  font-size: 26rpx;
  color: #998B7A;
}

.preview-names {
  font-size: 28rpx;
  color: #6D5C4B;
  margin-left: 10rpx;
}

.card-actions {
  text-align: right;
}

.action-btn.delete {
  display: inline-block;
  background: #FFF8F0;
  color: #FF8C42;
  padding: 12rpx 24rpx;
  border-radius: 20rpx;
  font-size: 26rpx;
  border: 1rpx solid #FFE0C8;
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 150rpx 40rpx;
}

.empty-icon {
  font-size: 140rpx;
  margin-bottom: 40rpx;
}

.empty-title {
  font-size: 40rpx;
  font-weight: 600;
  color: #5D4037;
  margin-bottom: 20rpx;
}

.empty-desc {
  font-size: 30rpx;
  color: #998B7A;
  margin-bottom: 50rpx;
}

.btn-primary {
  background: linear-gradient(135deg, #FF8C42, #FFA76D);
  color: #FFFFFF;
  border: none;
  border-radius: 56rpx;
  padding: 28rpx 64rpx;
  font-size: 32rpx;
  font-weight: 600;
  box-shadow: 0 8rpx 28rpx rgba(255, 140, 66, 0.4);
}
</style>
