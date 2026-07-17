<template>
  <view class="detail-container">
    <view class="plan-header">
      <view class="header-bg"></view>
      <view class="plan-info">
        <text class="plan-title">📅 饮食计划</text>
        <text class="plan-desc">共 {{ dietPlan.length }} 天，{{ totalRecipes }} 道菜</text>
      </view>
    </view>

    <scroll-view class="plan-content" scroll-y>
      <view class="days-tabs">
        <view 
          v-for="day in dietPlan" 
          :key="day.day"
          :class="['day-tab', currentDay === day.day ? 'active' : '']"
          @click="currentDay = day.day"
        >
          <text>第{{ day.day }}天</text>
        </view>
      </view>

      <view v-if="currentPlan" class="day-content">
        <view class="meal-section">
          <view class="meal-header">
            <text class="meal-icon">🌅</text>
            <text class="meal-title">早餐</text>
          </view>
          <view 
            v-if="currentPlan.breakfast" 
            class="recipe-card"
            @click="viewRecipe(currentPlan.breakfast)"
          >
            <view class="recipe-name">{{ currentPlan.breakfast.name }}</view>
            <view class="recipe-calories">🔥 {{ currentPlan.breakfast.nutrition && currentPlan.breakfast.nutrition.calories || 0 }} kcal</view>
            <view class="recipe-ingredients">
              <text v-for="(item, idx) in currentPlan.breakfast.ingredients" :key="idx">{{ item.name }}</text>
            </view>
            <view class="view-detail">查看详情 →</view>
          </view>
        </view>

        <view class="meal-section">
          <view class="meal-header">
            <text class="meal-icon">☀️</text>
            <text class="meal-title">午餐</text>
          </view>
          <view 
            v-if="currentPlan.lunch" 
            class="recipe-card"
            @click="viewRecipe(currentPlan.lunch)"
          >
            <view class="recipe-name">{{ currentPlan.lunch.name }}</view>
            <view class="recipe-calories">🔥 {{ currentPlan.lunch.nutrition && currentPlan.lunch.nutrition.calories || 0 }} kcal</view>
            <view class="recipe-ingredients">
              <text v-for="(item, idx) in currentPlan.lunch.ingredients" :key="idx">{{ item.name }}</text>
            </view>
            <view class="view-detail">查看详情 →</view>
          </view>
        </view>

        <view class="meal-section">
          <view class="meal-header">
            <text class="meal-icon">🌙</text>
            <text class="meal-title">晚餐</text>
          </view>
          <view 
            v-if="currentPlan.dinner" 
            class="recipe-card"
            @click="viewRecipe(currentPlan.dinner)"
          >
            <view class="recipe-name">{{ currentPlan.dinner.name }}</view>
            <view class="recipe-calories">🔥 {{ currentPlan.dinner.nutrition && currentPlan.dinner.nutrition.calories || 0 }} kcal</view>
            <view class="recipe-ingredients">
              <text v-for="(item, idx) in currentPlan.dinner.ingredients" :key="idx">{{ item.name }}</text>
            </view>
            <view class="view-detail">查看详情 →</view>
          </view>
        </view>

        <view class="card summary-card">
          <view class="section-title">
            <text class="icon">📊</text>
            <text>今日营养总览</text>
          </view>
          <view class="nutrition-grid">
            <view class="nutrition-item">
              <text class="nutrition-value">{{ dayCalories }}</text>
              <text class="nutrition-label">总热量 (kcal)</text>
            </view>
            <view class="nutrition-item">
              <text class="nutrition-value">{{ dayProtein }}</text>
              <text class="nutrition-label">蛋白质 (g)</text>
            </view>
            <view class="nutrition-item">
              <text class="nutrition-value">{{ dayCarbs }}</text>
              <text class="nutrition-label">碳水 (g)</text>
            </view>
            <view class="nutrition-item">
              <text class="nutrition-value">{{ dayFat }}</text>
              <text class="nutrition-label">脂肪 (g)</text>
            </view>
          </view>
        </view>
      </view>

      <view v-if="responseText" class="card tips-card">
        <view class="section-title">
          <text class="icon">💡</text>
          <text>营养师建议</text>
        </view>
        <text class="tips-text">{{ responseText }}</text>
      </view>
    </scroll-view>

    <view class="action-bar">
      <button class="action-btn" @click="goBack">
        <text>返回</text>
      </button>
      <button class="action-btn primary" @click="viewAllRecipes">
        <text>查看全部菜谱</text>
      </button>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      dietPlan: [],
      allRecipes: [],
      currentDay: 1,
      responseText: ''
    }
  },
  computed: {
    currentPlan() {
      return this.dietPlan.find(day => day.day === this.currentDay)
    },
    totalRecipes() {
      return this.allRecipes.length
    },
    dayCalories() {
      let total = 0
      if (this.currentPlan) {
        if (this.currentPlan.breakfast?.nutrition) total += this.currentPlan.breakfast.nutrition.calories || 0
        if (this.currentPlan.lunch?.nutrition) total += this.currentPlan.lunch.nutrition.calories || 0
        if (this.currentPlan.dinner?.nutrition) total += this.currentPlan.dinner.nutrition.calories || 0
      }
      return total
    },
    dayProtein() {
      let total = 0
      if (this.currentPlan) {
        if (this.currentPlan.breakfast?.nutrition) total += this.currentPlan.breakfast.nutrition.protein || 0
        if (this.currentPlan.lunch?.nutrition) total += this.currentPlan.lunch.nutrition.protein || 0
        if (this.currentPlan.dinner?.nutrition) total += this.currentPlan.dinner.nutrition.protein || 0
      }
      return total
    },
    dayCarbs() {
      let total = 0
      if (this.currentPlan) {
        if (this.currentPlan.breakfast?.nutrition) total += this.currentPlan.breakfast.nutrition.carbs || 0
        if (this.currentPlan.lunch?.nutrition) total += this.currentPlan.lunch.nutrition.carbs || 0
        if (this.currentPlan.dinner?.nutrition) total += this.currentPlan.dinner.nutrition.carbs || 0
      }
      return total
    },
    dayFat() {
      let total = 0
      if (this.currentPlan) {
        if (this.currentPlan.breakfast?.nutrition) total += this.currentPlan.breakfast.nutrition.fat || 0
        if (this.currentPlan.lunch?.nutrition) total += this.currentPlan.lunch.nutrition.fat || 0
        if (this.currentPlan.dinner?.nutrition) total += this.currentPlan.dinner.nutrition.fat || 0
      }
      return total
    }
  },
  onLoad(options) {
    if (options.data) {
      try {
        const data = JSON.parse(decodeURIComponent(options.data))
        this.dietPlan = data.diet_plan || []
        this.allRecipes = data.recipes || []
        this.responseText = data.response_text || ''
        if (this.dietPlan.length > 0) {
          this.currentDay = this.dietPlan[0].day
        }
      } catch (e) {
        console.error('Parse diet plan data error', e)
      }
    }
  },
  methods: {
    viewRecipe(recipe) {
      uni.navigateTo({
        url: `/pages/recipe-detail/recipe-detail?data=${encodeURIComponent(JSON.stringify(recipe))}`
      })
    },
    goBack() {
      uni.navigateBack()
    },
    viewAllRecipes() {
      uni.showToast({ title: `共${this.allRecipes.length}道菜谱`, icon: 'none' })
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

.plan-header {
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

.plan-info {
  position: relative;
  z-index: 1;
}

.plan-title {
  font-size: 48rpx;
  font-weight: bold;
  color: #FFFFFF;
  display: block;
  margin-bottom: 12rpx;
  text-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.plan-desc {
  font-size: 28rpx;
  color: rgba(255, 255, 255, 0.9);
  display: block;
}

.days-tabs {
  display: flex;
  gap: 20rpx;
  padding: 24rpx;
  overflow-x: auto;
  white-space: nowrap;
}

.day-tab {
  background: #FFFFFF;
  padding: 18rpx 36rpx;
  border-radius: 44rpx;
  font-size: 30rpx;
  color: #6D5C4B;
  border: 2rpx solid #FFE0C8;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.day-tab.active {
  background: linear-gradient(135deg, #FF8C42, #FFA76D);
  color: #FFFFFF;
  border-color: #FF8C42;
  box-shadow: 0 4rpx 16rpx rgba(255, 140, 66, 0.3);
}

.day-content {
  padding: 0 24rpx;
}

.meal-section {
  margin-bottom: 28rpx;
}

.meal-header {
  display: flex;
  align-items: center;
  margin-bottom: 16rpx;
}

.meal-icon {
  font-size: 40rpx;
  margin-right: 12rpx;
}

.meal-title {
  font-size: 34rpx;
  font-weight: 600;
  color: #5D4037;
}

.recipe-card {
  background: #FFFFFF;
  border-radius: 24rpx;
  padding: 28rpx;
  box-shadow: 0 6rpx 24rpx rgba(255, 140, 66, 0.08);
  border: 1rpx solid rgba(255, 140, 66, 0.1);
  border-left: 6rpx solid #FF8C42;
}

.recipe-name {
  font-size: 34rpx;
  font-weight: 600;
  color: #5D4037;
  margin-bottom: 12rpx;
}

.recipe-calories {
  font-size: 26rpx;
  color: #FF8C42;
  font-weight: 500;
  margin-bottom: 16rpx;
}

.recipe-ingredients {
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
  margin-bottom: 16rpx;
}

.recipe-ingredients text {
  background: #FFF8F0;
  padding: 8rpx 20rpx;
  border-radius: 20rpx;
  font-size: 24rpx;
  color: #6D5C4B;
}

.view-detail {
  font-size: 26rpx;
  color: #FF8C42;
  text-align: right;
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

.tips-text {
  font-size: 30rpx;
  color: #6D5C4B;
  line-height: 1.7;
  background: linear-gradient(135deg, #FFF8F0, #FFF3E0);
  padding: 24rpx;
  border-radius: 20rpx;
  border-left: 6rpx solid #FF8C42;
}

.plan-content {
  flex: 1;
  padding-bottom: 150rpx;
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

.action-btn.primary {
  background: linear-gradient(135deg, #FF8C42, #FFA76D);
  color: #FFFFFF;
  border: none;
  box-shadow: 0 6rpx 24rpx rgba(255, 140, 66, 0.4);
}
</style>