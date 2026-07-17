<template>
  <view class="detail-container">
    <view class="recipe-header">
      <view class="header-bg"></view>
      <view class="recipe-info">
        <text class="recipe-title">{{ recipe.name }}</text>
        <view class="recipe-tags">
          <view class="tag">{{ recipe.suitable_for }}</view>
        </view>
      </view>
    </view>

    <scroll-view class="recipe-content" scroll-y>
      <view class="card nutrition-card">
        <view class="section-title">
          <text class="icon">🔥</text>
          <text>营养分析</text>
        </view>
        <view class="nutrition-grid">
          <view class="nutrition-item">
            <text class="nutrition-value">{{ recipe.nutrition && recipe.nutrition.calories || 0 }}</text>
            <text class="nutrition-label">热量 (kcal)</text>
          </view>
          <view class="nutrition-item">
            <text class="nutrition-value">{{ recipe.nutrition && recipe.nutrition.protein || 0 }}</text>
            <text class="nutrition-label">蛋白质 (g)</text>
          </view>
          <view class="nutrition-item">
            <text class="nutrition-value">{{ recipe.nutrition && recipe.nutrition.carbs || 0 }}</text>
            <text class="nutrition-label">碳水 (g)</text>
          </view>
          <view class="nutrition-item">
            <text class="nutrition-value">{{ recipe.nutrition && recipe.nutrition.fat || 0 }}</text>
            <text class="nutrition-label">脂肪 (g)</text>
          </view>
        </view>
      </view>

      <view class="card">
        <view class="section-title">
          <text class="icon">🥗</text>
          <text>食材清单</text>
        </view>
        <view class="ingredients-list">
          <view 
            v-for="(item, index) in recipe.ingredients" 
            :key="index" 
            class="ingredient-item"
          >
            <text class="ingredient-name">{{ item.name }}</text>
            <text class="ingredient-amount">{{ item.amount }}</text>
          </view>
        </view>
      </view>

      <view class="card">
        <view class="section-title">
          <text class="icon">👩🍳</text>
          <text>烹饪步骤</text>
        </view>
        <view class="steps-list">
          <view 
            v-for="(step, index) in recipe.steps" 
            :key="index" 
            class="step-item"
          >
            <view class="step-number">{{ step.step || index + 1 }}</view>
            <text class="step-description">{{ step.description }}</text>
          </view>
        </view>
      </view>

      <view class="card">
        <view class="section-title">
          <text class="icon">💡</text>
          <text>烹饪小贴士</text>
        </view>
        <text class="tips-text">{{ recipe.tips }}</text>
      </view>
    </scroll-view>

    <view class="action-bar">
      <button 
        :class="['action-btn', isFavorite ? 'favorited' : '']" 
        @click="toggleFavorite"
      >
        <text>{{ isFavorite ? '❤️ 已收藏' : '🤍 收藏' }}</text>
      </button>
      <button class="action-btn primary" @click="shareRecipe">
        <text>分享</text>
      </button>
    </view>
  </view>
</template>

<script>
import { saveLocalFavorite, removeLocalFavorite, isLocalFavorite } from '@/utils/storage'

export default {
  data() {
    return {
      recipe: {},
      isFavorite: false
    }
  },
  onLoad(options) {
    if (options.data) {
      try {
        this.recipe = JSON.parse(decodeURIComponent(options.data))
        this.checkFavorite()
      } catch (e) {
        console.error('Parse recipe data error', e)
      }
    }
  },
  methods: {
    checkFavorite() {
      if (this.recipe.id) {
        this.isFavorite = isLocalFavorite(this.recipe.id)
      }
    },
    toggleFavorite() {
      if (!this.recipe.id) return

      if (this.isFavorite) {
        removeLocalFavorite(this.recipe.id)
        this.isFavorite = false
        uni.showToast({ title: '已取消收藏', icon: 'none' })
      } else {
        saveLocalFavorite(this.recipe)
        this.isFavorite = true
        uni.showToast({ title: '已加入收藏', icon: 'success' })
      }
    },
    shareRecipe() {
      uni.showToast({ title: '分享功能开发中', icon: 'none' })
    }
  }
}
</script>

<style scoped>
.detail-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #FFF8F0;
}

.recipe-header {
  position: relative;
  padding: 50rpx 32rpx;
  background: linear-gradient(135deg, #FF8C42, #FFA76D);
  overflow: hidden;
  box-shadow: 0 10rpx 40rpx rgba(255, 140, 66, 0.3);
}

.header-bg {
  position: absolute;
  top: -30rpx;
  right: -80rpx;
  width: 350rpx;
  height: 350rpx;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 50%;
}

.recipe-info {
  position: relative;
  z-index: 1;
}

.recipe-title {
  font-size: 48rpx;
  font-weight: bold;
  color: #FFFFFF;
  display: block;
  margin-bottom: 20rpx;
  text-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.recipe-tags {
  display: flex;
  gap: 16rpx;
}

.tag {
  background: rgba(255, 255, 255, 0.25);
  color: #FFFFFF;
  padding: 10rpx 24rpx;
  border-radius: 24rpx;
  font-size: 26rpx;
}

.recipe-content {
  flex: 1;
  padding: 24rpx;
  padding-bottom: 150rpx;
}

.card {
  background: #FFFFFF;
  border-radius: 24rpx;
  padding: 32rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 6rpx 24rpx rgba(255, 140, 66, 0.08);
  border: 1rpx solid rgba(255, 140, 66, 0.1);
}

.section-title {
  display: flex;
  align-items: center;
  font-size: 34rpx;
  font-weight: 600;
  color: #5D4037;
  margin-bottom: 28rpx;
}

.icon {
  font-size: 40rpx;
  margin-right: 16rpx;
}

.nutrition-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
}

.nutrition-item {
  flex: 1;
  min-width: 150rpx;
  background: linear-gradient(135deg, #FFF8F0, #FFEDE0);
  border-radius: 20rpx;
  padding: 28rpx 20rpx;
  text-align: center;
  border: 1rpx solid #FFE0C8;
}

.nutrition-value {
  font-size: 44rpx;
  font-weight: bold;
  color: #FF8C42;
  display: block;
}

.nutrition-label {
  font-size: 26rpx;
  color: #6D5C4B;
  margin-top: 10rpx;
  display: block;
}

.ingredients-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
}

.ingredient-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  background: #FFF8F0;
  padding: 24rpx 36rpx;
  border-radius: 20rpx;
  min-width: 160rpx;
  border: 1rpx solid #FFE0C8;
}

.ingredient-name {
  font-size: 30rpx;
  font-weight: 600;
  color: #5D4037;
}

.ingredient-amount {
  font-size: 26rpx;
  color: #998B7A;
  margin-top: 10rpx;
}

.steps-list {
  display: flex;
  flex-direction: column;
  gap: 28rpx;
}

.step-item {
  display: flex;
  gap: 24rpx;
}

.step-number {
  width: 64rpx;
  height: 64rpx;
  background: linear-gradient(135deg, #FF8C42, #FFA76D);
  color: #FFFFFF;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30rpx;
  font-weight: bold;
  flex-shrink: 0;
  box-shadow: 0 4rpx 16rpx rgba(255, 140, 66, 0.3);
}

.step-description {
  font-size: 30rpx;
  color: #5D4037;
  line-height: 1.7;
  padding-top: 10rpx;
}

.tips-text {
  font-size: 30rpx;
  color: #6D5C4B;
  line-height: 1.7;
  background: linear-gradient(135deg, #FFF8F0, #FFF3E0);
  padding: 24rpx;
  border-radius: 20rpx;
  border-left: 6rpx solid #FF8C42;
}

.action-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  gap: 24rpx;
  padding: 24rpx 32rpx;
  padding-bottom: calc(24rpx + env(safe-area-inset-bottom));
  background: #FFFFFF;
  box-shadow: 0 -6rpx 24rpx rgba(255, 140, 66, 0.1);
}

.action-btn {
  flex: 1;
  background: #FFF8F0;
  color: #5D4037;
  border: 2rpx solid #FFE0C8;
  border-radius: 56rpx;
  padding: 28rpx 0;
  font-size: 32rpx;
  font-weight: 600;
}

.action-btn.favorited {
  background: linear-gradient(135deg, #FFF8F0, #FFEDE0);
  color: #FF8C42;
  border-color: #FF8C42;
}

.action-btn.primary {
  background: linear-gradient(135deg, #FF8C42, #FFA76D);
  color: #FFFFFF;
  border: none;
  box-shadow: 0 6rpx 24rpx rgba(255, 140, 66, 0.4);
}
</style>
