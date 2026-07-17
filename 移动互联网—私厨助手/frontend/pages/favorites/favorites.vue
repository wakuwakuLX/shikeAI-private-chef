<template>
  <view class="container">
    <view class="page-header">
      <text class="page-title">❤️ 我的收藏</text>
      <text class="page-desc">精心收藏的美味菜谱</text>
    </view>

    <view v-if="favorites.length > 0" class="favorites-list">
      <view 
        v-for="(favorite, index) in favorites" 
        :key="index" 
        class="favorite-card"
        @click="viewRecipe(favorite)"
      >
        <view class="card-content">
          <text class="recipe-name">{{ favorite.name }}</text>
          <view class="recipe-meta">
            <text class="calories">🔥 {{ favorite.nutrition && favorite.nutrition.calories || 0 }} kcal</text>
            <text class="protein">🥩 {{ favorite.nutrition && favorite.nutrition.protein || 0 }}g 蛋白质</text>
          </view>
          <text class="suitable">{{ favorite.suitable_for }}</text>
        </view>
        <view class="card-actions">
          <view class="action-btn delete" @click.stop="removeFavorite(favorite)">
            <text>删除</text>
          </view>
        </view>
      </view>
    </view>

    <view v-else class="empty-state">
      <text class="empty-icon">📭</text>
      <text class="empty-title">暂无收藏</text>
      <text class="empty-desc">快去发现美味菜谱并收藏吧</text>
      <button class="btn-primary" @click="goHome">
        <text>去生成菜谱</text>
      </button>
    </view>
  </view>
</template>

<script>
import { getLocalFavorites, removeLocalFavorite } from '@/utils/storage'

export default {
  data() {
    return {
      favorites: []
    }
  },
  onShow() {
    this.loadFavorites()
  },
  methods: {
    loadFavorites() {
      this.favorites = getLocalFavorites()
    },
    viewRecipe(recipe) {
      uni.navigateTo({
        url: `/pages/recipe-detail/recipe-detail?data=${encodeURIComponent(JSON.stringify(recipe))}`
      })
    },
    removeFavorite(recipe) {
      uni.showModal({
        title: '确认删除',
        content: `确定要删除「${recipe.name}」吗？`,
        success: (res) => {
          if (res.confirm) {
            removeLocalFavorite(recipe.id)
            this.loadFavorites()
            uni.showToast({ title: '已删除', icon: 'none' })
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

.favorites-list {
  padding: 24rpx;
}

.favorite-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #FFFFFF;
  padding: 28rpx 32rpx;
  border-radius: 24rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 6rpx 24rpx rgba(255, 140, 66, 0.08);
  border: 1rpx solid rgba(255, 140, 66, 0.1);
  transition: all 0.3s ease;
}

.favorite-card:active {
  transform: scale(0.98);
}

.card-content {
  flex: 1;
}

.recipe-name {
  font-size: 34rpx;
  font-weight: 600;
  color: #5D4037;
  display: block;
}

.recipe-meta {
  display: flex;
  gap: 24rpx;
  margin-top: 14rpx;
}

.calories {
  font-size: 26rpx;
  color: #FF8C42;
  font-weight: 500;
}

.protein {
  font-size: 26rpx;
  color: #6D5C4B;
}

.suitable {
  font-size: 26rpx;
  color: #998B7A;
  margin-top: 10rpx;
  display: block;
}

.card-actions {
  margin-left: 24rpx;
}

.action-btn.delete {
  background: #FFF8F0;
  color: #FF8C42;
  padding: 14rpx 28rpx;
  border-radius: 24rpx;
  font-size: 28rpx;
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
