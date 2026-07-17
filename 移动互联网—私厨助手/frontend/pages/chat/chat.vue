<template>
  <view class="chat-container">
    <view class="chat-header">
      <view class="back-btn" @click="goBack">
        <text>←</text>
      </view>
      <text class="chat-title">AI对话</text>
      <view class="clear-btn" @click="clearChat">
        <text>清空</text>
      </view>
    </view>

    <scroll-view class="chat-messages" scroll-y :scroll-top="scrollTop">
      <view 
        v-for="(message, index) in messages" 
        :key="index" 
        :class="['message-item', message.role === 'user' ? 'user' : 'ai']"
      >
        <view class="avatar">
          <text>{{ message.role === 'user' ? '👤' : '🤖' }}</text>
        </view>
        <view class="message-content">
          <text class="text">{{ message.content }}</text>
          <view v-if="message.dietPlan && message.dietPlan.length > 0" class="diet-plan-preview">
            <view v-for="day in message.dietPlan" :key="day.day" class="day-section">
              <text class="day-title">第{{ day.day }}天</text>
              <view v-if="day.breakfast" class="meal-item" @click="viewRecipe(day.breakfast)">
                <text class="meal-icon">🌅</text>
                <view class="meal-info">
                  <text class="meal-name">{{ day.breakfast.name }}</text>
                  <text class="meal-calories">🔥 {{ day.breakfast.nutrition && day.breakfast.nutrition.calories || 0 }} kcal</text>
                </view>
              </view>
              <view v-if="day.lunch" class="meal-item" @click="viewRecipe(day.lunch)">
                <text class="meal-icon">☀️</text>
                <view class="meal-info">
                  <text class="meal-name">{{ day.lunch.name }}</text>
                  <text class="meal-calories">🔥 {{ day.lunch.nutrition && day.lunch.nutrition.calories || 0 }} kcal</text>
                </view>
              </view>
              <view v-if="day.dinner" class="meal-item" @click="viewRecipe(day.dinner)">
                <text class="meal-icon">🌙</text>
                <view class="meal-info">
                  <text class="meal-name">{{ day.dinner.name }}</text>
                  <text class="meal-calories">🔥 {{ day.dinner.nutrition && day.dinner.nutrition.calories || 0 }} kcal</text>
                </view>
              </view>
            </view>
          </view>
          <view v-else-if="message.recipes && message.recipes.length > 0" class="recipes-preview">
            <view 
              v-for="recipe in message.recipes" 
              :key="recipe.id" 
              class="recipe-card"
              @click="viewRecipe(recipe)"
            >
              <text class="recipe-name">{{ recipe.name }}</text>
              <text class="recipe-calories">🔥 {{ recipe.nutrition && recipe.nutrition.calories || 0 }} kcal</text>
            </view>
          </view>
        </view>
      </view>
      <view v-if="loading" class="loading-item">
        <view class="loading-dots">
          <view class="dot"></view>
          <view class="dot"></view>
          <view class="dot"></view>
        </view>
        <text class="loading-text">AI正在思考...</text>
      </view>
    </scroll-view>

    <view class="chat-input-area">
      <input 
        v-model="inputMessage" 
        placeholder="输入您的需求..." 
        class="chat-input"
        @confirm="sendMessage"
      />
      <button class="send-btn" @click="sendMessage" :disabled="!inputMessage.trim()">
        <text>发送</text>
      </button>
    </view>
  </view>
</template>

<script>
import { generateRecipes } from '@/utils/api'
import { saveLocalHistory } from '@/utils/storage'

export default {
  data() {
    return {
      messages: [
        {
          role: 'ai',
          content: '您好！我是您的私人营养师AI助手。请问您有什么食材？有什么忌口或口味偏好吗？我可以帮您生成美味又健康的菜谱。'
        }
      ],
      inputMessage: '',
      loading: false,
      scrollTop: 0,
      conversationId: ''
    }
  },
  methods: {
    async sendMessage() {
      if (!this.inputMessage.trim()) return

      const userMessage = this.inputMessage.trim()
      this.inputMessage = ''
      
      this.messages.push({ role: 'user', content: userMessage })
      this.scrollToBottom()

      this.loading = true
      try {
        const goals = []
        if (userMessage.includes('饮食计划') || userMessage.includes('三餐') || userMessage.includes('一周') || userMessage.includes('计划')) {
          goals.push('饮食计划')
        }
        if (userMessage.includes('减脂') || userMessage.includes('减肥')) {
          goals.push('减脂')
        }
        if (userMessage.includes('增肌') || userMessage.includes('健身')) {
          goals.push('增肌')
        }
        if (userMessage.includes('素食') || userMessage.includes('素菜')) {
          goals.push('素食')
        }

        const response = await generateRecipes({
          ingredients: [],
          dietary_restrictions: [],
          taste_preferences: [],
          goals: goals,
          message: userMessage
        })

        let responseContent = response.response_text || '已为您生成菜谱'
        const recipes = response.recipes || []
        const dietPlan = response.diet_plan || []
        
        if (recipes.length > 0) {
          saveLocalHistory({
            id: Date.now().toString(),
            title: `对话 - ${userMessage.slice(0, 20)}`,
            content: JSON.stringify(response),
            created_at: new Date().toISOString()
          })
        }

        this.messages.push({
          role: 'ai',
          content: responseContent,
          recipes: recipes,
          dietPlan: dietPlan
        })

      } catch (error) {
        this.messages.push({
          role: 'ai',
          content: '抱歉，网络连接失败，请稍后再试。'
        })
      } finally {
        this.loading = false
        this.scrollToBottom()
      }
    },
    scrollToBottom() {
      setTimeout(() => {
        this.scrollTop = 99999
      }, 100)
    },
    viewRecipe(recipe) {
      uni.navigateTo({
        url: `/pages/recipe-detail/recipe-detail?data=${encodeURIComponent(JSON.stringify(recipe))}`
      })
    },
    clearChat() {
      uni.showModal({
        title: '确认清空',
        content: '确定要清空所有对话记录吗？',
        success: (res) => {
          if (res.confirm) {
            this.messages = [
              {
                role: 'ai',
                content: '您好！我是您的私人营养师AI助手。请问您有什么食材？有什么忌口或口味偏好吗？'
              }
            ]
          }
        }
      })
    },
    goBack() {
      uni.navigateBack()
    }
  }
}
</script>

<style scoped>
.chat-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: #FFF8F0;
}

.chat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20rpx 30rpx;
  background: linear-gradient(135deg, #FF8C42, #FFA76D);
  color: #FFFFFF;
}

.back-btn {
  font-size: 40rpx;
  padding: 10rpx;
}

.chat-title {
  font-size: 34rpx;
  font-weight: 600;
}

.clear-btn {
  font-size: 28rpx;
  padding: 10rpx 20rpx;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 20rpx;
}

.chat-messages {
  flex: 1;
  padding: 20rpx;
}

.message-item {
  display: flex;
  margin-bottom: 24rpx;
}

.message-item.user {
  flex-direction: row-reverse;
}

.avatar {
  width: 72rpx;
  height: 72rpx;
  border-radius: 50%;
  background: #FFFFFF;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 36rpx;
  flex-shrink: 0;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.1);
}

.message-item.user .avatar {
  background: #FF8C42;
}

.message-content {
  max-width: 70%;
  margin: 0 16rpx;
}

.message-item.user .message-content {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.text {
  background: #FFFFFF;
  padding: 20rpx 28rpx;
  border-radius: 24rpx;
  font-size: 28rpx;
  color: #333333;
  line-height: 1.6;
  display: inline-block;
  box-shadow: 0 2rpx 10rpx rgba(0, 0, 0, 0.05);
}

.message-item.user .text {
  background: linear-gradient(135deg, #FF8C42, #FFA76D);
  color: #FFFFFF;
}

.diet-plan-preview {
  margin-top: 16rpx;
}

.day-section {
  background: #FFFFFF;
  border-radius: 16rpx;
  padding: 20rpx;
  margin-bottom: 12rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.day-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #FF8C42;
  margin-bottom: 16rpx;
  display: block;
}

.meal-item {
  display: flex;
  align-items: center;
  padding: 16rpx;
  background: #FFF8F0;
  border-radius: 12rpx;
  margin-bottom: 12rpx;
  border: 1rpx solid #FFE0C8;
}

.meal-item:last-child {
  margin-bottom: 0;
}

.meal-icon {
  font-size: 36rpx;
  margin-right: 16rpx;
}

.meal-info {
  flex: 1;
}

.meal-name {
  font-size: 28rpx;
  font-weight: 600;
  color: #5D4037;
  display: block;
}

.meal-calories {
  font-size: 24rpx;
  color: #FF8C42;
  margin-top: 8rpx;
  display: block;
}

.recipes-preview {
  margin-top: 16rpx;
}

.recipe-card {
  background: #FFFFFF;
  padding: 20rpx 24rpx;
  border-radius: 16rpx;
  margin-bottom: 12rpx;
  box-shadow: 0 2rpx 8rpx rgba(0, 0, 0, 0.05);
}

.message-item.user .recipe-card {
  background: #FFF8F0;
}

.recipe-name {
  font-size: 28rpx;
  font-weight: 600;
  color: #333333;
}

.message-item.user .recipe-name {
  color: #FF8C42;
}

.recipe-calories {
  font-size: 24rpx;
  color: #FF8C42;
  margin-top: 8rpx;
  display: block;
}

.message-item.user .recipe-calories {
  color: #FFA76D;
}

.loading-item {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.loading-dots {
  display: flex;
  gap: 12rpx;
  margin-bottom: 8rpx;
}

.dot {
  width: 16rpx;
  height: 16rpx;
  background: #CCCCCC;
  border-radius: 50%;
  animation: loading 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes loading {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

.loading-text {
  font-size: 24rpx;
  color: #999999;
}

.chat-input-area {
  display: flex;
  gap: 16rpx;
  padding: 20rpx;
  background: #FFFFFF;
  border-top: 2rpx solid #F0F0F0;
}

.chat-input {
  flex: 1;
  background: #F8F8F8;
  border-radius: 40rpx;
  padding: 20rpx 30rpx;
  font-size: 28rpx;
}

.send-btn {
  background: linear-gradient(135deg, #FF8C42, #FFA76D);
  color: #FFFFFF;
  border: none;
  border-radius: 40rpx;
  padding: 0 40rpx;
  font-size: 28rpx;
  font-weight: 600;
}

.send-btn:disabled {
  opacity: 0.5;
}
</style>
