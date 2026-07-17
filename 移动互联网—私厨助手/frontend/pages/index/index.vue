<template>
  <view class="container">
    <view class="header">
      <view class="logo">
        <text class="logo-icon">🍳</text>
        <text class="logo-text">食刻AI</text>
      </view>
      <text class="header-desc">您的私人智能营养师</text>
    </view>

    <view class="card ingredients-card">
      <view class="section-title">
        <text class="icon">🥬</text>
        <text>现有食材</text>
      </view>
      <view class="input-group">
        <input 
          v-model="ingredientsInput" 
          placeholder="输入食材，用逗号分隔" 
          class="ingredients-input"
          @confirm="addIngredient"
        />
        <button class="add-btn" @click="addIngredient">添加</button>
      </view>
      <view class="tags-container" v-if="ingredients.length > 0">
        <view 
          v-for="(item, index) in ingredients" 
          :key="index" 
          class="tag active"
          @click="removeIngredient(index)"
        >
          {{ item }}
          <text class="tag-close">×</text>
        </view>
      </view>
    </view>

    <view class="card">
      <view class="section-title">
        <text class="icon">🚫</text>
        <text>忌口食物</text>
      </view>
      <view class="options-grid">
        <view 
          v-for="item in dietaryOptions" 
          :key="item.value"
          :class="['option-item', dietaryRestrictions.includes(item.value) ? 'active' : '']"
          @click="toggleOption('dietaryRestrictions', item.value)"
        >
          <text>{{ item.label }}</text>
        </view>
      </view>
    </view>

    <view class="card">
      <view class="section-title">
        <text class="icon">😋</text>
        <text>口味偏好</text>
      </view>
      <view class="options-grid">
        <view 
          v-for="item in tasteOptions" 
          :key="item.value"
          :class="['option-item', tastePreferences.includes(item.value) ? 'active' : '']"
          @click="toggleOption('tastePreferences', item.value)"
        >
          <text>{{ item.label }}</text>
        </view>
      </view>
    </view>

    <view class="card">
      <view class="section-title">
        <text class="icon">🎯</text>
        <text>饮食目标</text>
      </view>
      <view class="options-grid">
        <view 
          v-for="item in goalOptions" 
          :key="item.value"
          :class="['option-item', goals.includes(item.value) ? 'active' : '']"
          @click="toggleOption('goals', item.value)"
        >
          <text>{{ item.label }}</text>
        </view>
      </view>
    </view>

    <view class="card">
      <view class="section-title">
        <text class="icon">💬</text>
        <text>额外要求</text>
      </view>
      <textarea 
        v-model="message" 
        placeholder="比如：少油少盐、适合儿童、无辣..." 
        class="message-textarea"
      />
    </view>

    <view class="action-area">
      <button class="btn-primary" @click="generateRecipes" :loading="loading">
        <text>{{ loading ? '正在生成...' : '生成菜谱' }}</text>
      </button>
      <button class="btn-secondary" @click="goToChat">
        <text>AI对话</text>
      </button>
    </view>

    <view class="recent-recipes" v-if="recentRecipes.length > 0">
      <view class="section-title">
        <text class="icon">📋</text>
        <text>最近生成</text>
        <view v-if="lastResponse && lastResponse.diet_plan" class="view-plan-btn" @click="viewDietPlan">
          <text>查看完整计划 →</text>
        </view>
      </view>
      <view 
        v-for="recipe in recentRecipes" 
        :key="recipe.id" 
        class="recipe-card"
        @click="viewRecipe(recipe)"
      >
        <view class="recipe-info">
          <text class="recipe-name">{{ recipe.name }}</text>
          <text class="recipe-calories">🔥 {{ recipe.nutrition && recipe.nutrition.calories || 0 }} kcal</text>
        </view>
        <view class="recipe-arrow">→</view>
      </view>
    </view>
  </view>
</template>

<script>
import { generateRecipes } from '@/utils/api'
import { saveLocalHistory, getLocalHistory } from '@/utils/storage'

export default {
  data() {
    return {
      ingredients: [],
      ingredientsInput: '',
      dietaryRestrictions: [],
      tastePreferences: [],
      goals: [],
      message: '',
      loading: false,
      recentRecipes: [],
      lastResponse: null,
      dietaryOptions: [
        { label: '无忌口', value: '无' },
        { label: '海鲜', value: '海鲜' },
        { label: '牛羊肉', value: '牛羊肉' },
        { label: '辣', value: '辣' },
        { label: '糖', value: '糖' },
        { label: '乳制品', value: '乳制品' },
        { label: '坚果', value: '坚果' }
      ],
      tasteOptions: [
        { label: '清淡', value: '清淡' },
        { label: '酸辣', value: '酸辣' },
        { label: '甜口', value: '甜口' },
        { label: '咸香', value: '咸香' },
        { label: '微辣', value: '微辣' },
        { label: '酱香', value: '酱香' },
        { label: '油炸', value: '油炸' }
      ],
      goalOptions: [
        { label: '普通', value: '普通' },
        { label: '减脂', value: '减脂' },
        { label: '控糖', value: '控糖' },
        { label: '增肌', value: '增肌' },
        { label: '儿童餐', value: '儿童餐' },
        { label: '素食', value: '素食' },
        { label: '饮食计划', value: '饮食计划' }
      ]
    }
  },
  onLoad() {
    this.loadRecentRecipes()
  },
  methods: {
    addIngredient() {
      if (this.ingredientsInput.trim()) {
        const items = this.ingredientsInput.split(/[,，、\s]+/).filter(i => i.trim())
        items.forEach(item => {
          if (!this.ingredients.includes(item.trim())) {
            this.ingredients.push(item.trim())
          }
        })
        this.ingredientsInput = ''
      }
    },
    removeIngredient(index) {
      this.ingredients.splice(index, 1)
    },
    toggleOption(field, value) {
      if (value === '无') {
        this[field] = []
        return
      }
      const index = this[field].indexOf(value)
      if (index === -1) {
        this[field].push(value)
      } else {
        this[field].splice(index, 1)
      }
    },
    async generateRecipes() {
      if (this.ingredients.length === 0) {
        uni.showToast({ title: '请至少输入一种食材', icon: 'none' })
        return
      }

      this.loading = true
      if (this.goals.includes('饮食计划')) {
        uni.showLoading({ title: '正在生成饮食计划，请耐心等待...', mask: true })
      }
      try {
        const response = await generateRecipes({
          ingredients: this.ingredients,
          dietary_restrictions: this.dietaryRestrictions,
          taste_preferences: this.tastePreferences,
          goals: this.goals,
          message: this.message
        })

        if (response.recipes && response.recipes.length > 0) {
          saveLocalHistory({
            id: Date.now().toString(),
            title: `菜谱 - ${this.ingredients.join(', ')}`,
            content: JSON.stringify(response),
            created_at: new Date().toISOString()
          })
          this.recentRecipes = response.recipes
          this.lastResponse = response
          uni.showToast({ title: `成功生成${response.recipes.length}道菜谱`, icon: 'success' })
        } else {
          uni.showToast({ title: response.response_text || '生成失败', icon: 'none' })
        }
      } catch (error) {
        console.error('Generate recipes error:', error)
        const errorMsg = error.detail || error.message || '网络请求失败'
        uni.showToast({ title: errorMsg, icon: 'none', duration: 3000 })
      } finally {
        this.loading = false
        uni.hideLoading()
      }
    },
    loadRecentRecipes() {
      const history = getLocalHistory()
      history.forEach(item => {
        try {
          const data = JSON.parse(item.content)
          let recipes = []
          if (data.recipes && Array.isArray(data.recipes)) {
            recipes = data.recipes
          } else if (Array.isArray(data)) {
            recipes = data
          }
          if (recipes.length > 0) {
            this.recentRecipes.push(...recipes.slice(0, 3))
          }
        } catch (e) {
          console.error('Parse history error', e)
        }
      })
      this.recentRecipes = this.recentRecipes.slice(0, 5)
    },
    viewRecipe(recipe) {
      uni.navigateTo({
        url: `/pages/recipe-detail/recipe-detail?data=${encodeURIComponent(JSON.stringify(recipe))}`
      })
    },
    viewDietPlan() {
      if (this.lastResponse) {
        uni.navigateTo({
          url: `/pages/diet-plan-detail/diet-plan-detail?data=${encodeURIComponent(JSON.stringify(this.lastResponse))}`
        })
      }
    },
    goToChat() {
      uni.navigateTo({
        url: '/pages/chat/chat'
      })
    }
  }
}
</script>

<style scoped>
.container {
  padding: 20rpx;
  padding-bottom: 180rpx;
  background: #FFF8F0;
  min-height: 100vh;
}

.header {
  text-align: center;
  padding: 50rpx 40rpx;
  background: linear-gradient(135deg, #FF8C42, #FFA76D);
  border-radius: 30rpx;
  margin-bottom: 30rpx;
  color: #FFFFFF;
  position: relative;
  overflow: hidden;
  box-shadow: 0 10rpx 40rpx rgba(255, 140, 66, 0.3);
}

.header::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -20%;
  width: 200rpx;
  height: 200rpx;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.header::after {
  content: '';
  position: absolute;
  bottom: -30%;
  left: -10%;
  width: 150rpx;
  height: 150rpx;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
}

.logo {
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 10rpx;
  position: relative;
  z-index: 1;
}

.logo-icon {
  font-size: 72rpx;
  margin-right: 16rpx;
}

.logo-text {
  font-size: 52rpx;
  font-weight: bold;
  text-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.header-desc {
  font-size: 28rpx;
  opacity: 0.95;
  position: relative;
  z-index: 1;
}

.card {
  background: #FFFFFF;
  border-radius: 24rpx;
  padding: 32rpx;
  margin-bottom: 24rpx;
  box-shadow: 0 6rpx 24rpx rgba(255, 140, 66, 0.08);
  border: 1rpx solid rgba(255, 140, 66, 0.1);
  position: relative;
  overflow: hidden;
}

.card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6rpx;
  background: linear-gradient(90deg, #FF8C42, #FFB377, #FF8C42);
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

.input-group {
  display: flex;
  gap: 20rpx;
}

.ingredients-input {
  flex: 1;
  background: #FFF8F0;
  border: 2rpx solid #FFE0C8;
  border-radius: 44rpx;
  padding: 24rpx 32rpx;
  font-size: 30rpx;
  color: #5D4037;
}

.ingredients-input::placeholder {
  color: #C4A77D;
}

.add-btn {
  background: linear-gradient(135deg, #FF8C42, #FFA76D);
  color: #FFFFFF;
  border-radius: 44rpx;
  padding: 0 36rpx;
  font-size: 30rpx;
  font-weight: 600;
  border: none;
  box-shadow: 0 6rpx 20rpx rgba(255, 140, 66, 0.4);
}

.tags-container {
  margin-top: 24rpx;
}

.tag {
  display: inline-flex;
  align-items: center;
  background: #FFF8F0;
  color: #FF8C42;
  padding: 14rpx 28rpx;
  border-radius: 36rpx;
  font-size: 28rpx;
  margin-right: 16rpx;
  margin-bottom: 16rpx;
  border: 2rpx solid #FFE0C8;
  transition: all 0.3s ease;
}

.tag.active {
  background: linear-gradient(135deg, #FF8C42, #FFA76D);
  color: #FFFFFF;
  border-color: #FF8C42;
  box-shadow: 0 4rpx 16rpx rgba(255, 140, 66, 0.3);
}

.tag-close {
  margin-left: 8rpx;
  font-size: 30rpx;
}

.options-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20rpx;
}

.option-item {
  background: #FFF8F0;
  padding: 22rpx 36rpx;
  border-radius: 44rpx;
  font-size: 28rpx;
  color: #6D5C4B;
  border: 2rpx solid transparent;
  transition: all 0.3s ease;
}

.option-item.active {
  background: linear-gradient(135deg, #FFF8F0, #FFEDE0);
  color: #FF8C42;
  border-color: #FF8C42;
  box-shadow: 0 4rpx 16rpx rgba(255, 140, 66, 0.2);
}

.message-textarea {
  width: 100%;
  height: 180rpx;
  background: #FFF8F0;
  border: 2rpx solid #FFE0C8;
  border-radius: 24rpx;
  padding: 24rpx;
  font-size: 30rpx;
  color: #5D4037;
}

.message-textarea::placeholder {
  color: #C4A77D;
}

.action-area {
  display: flex;
  gap: 24rpx;
  margin-top: 36rpx;
}

.btn-primary {
  flex: 1;
  background: linear-gradient(135deg, #FF8C42, #FFA76D);
  color: #FFFFFF;
  border: none;
  border-radius: 56rpx;
  padding: 32rpx 0;
  font-size: 34rpx;
  font-weight: 600;
  box-shadow: 0 8rpx 28rpx rgba(255, 140, 66, 0.4);
}

.btn-secondary {
  flex: 1;
  background: #FFFFFF;
  color: #FF8C42;
  border: 2rpx solid #FF8C42;
  border-radius: 56rpx;
  padding: 32rpx 0;
  font-size: 34rpx;
  font-weight: 600;
}

.recent-recipes {
  margin-top: 40rpx;
}

.section-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.view-plan-btn {
  font-size: 26rpx;
  color: #FF8C42;
  background: rgba(255, 140, 66, 0.1);
  padding: 10rpx 20rpx;
  border-radius: 20rpx;
}

.recipe-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #FFFFFF;
  padding: 28rpx 32rpx;
  border-radius: 20rpx;
  margin-bottom: 16rpx;
  box-shadow: 0 4rpx 16rpx rgba(255, 140, 66, 0.08);
  border-left: 6rpx solid #FF8C42;
  transition: all 0.3s ease;
}

.recipe-card:active {
  transform: scale(0.98);
}

.recipe-info {
  flex: 1;
}

.recipe-name {
  font-size: 32rpx;
  font-weight: 600;
  color: #5D4037;
  display: block;
}

.recipe-calories {
  font-size: 28rpx;
  color: #FF8C42;
  font-weight: 500;
}

.recipe-arrow {
  font-size: 36rpx;
  color: #CCCCCC;
}
</style>
