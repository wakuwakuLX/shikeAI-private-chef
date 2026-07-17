<script>
export default {
  onLaunch: function() {
    console.log('App Launch')
  },
  onShow: function() {
    console.log('App Show')
  },
  onHide: function() {
    console.log('App Hide')
  }
}
</script>

<style>
page {
  background-color: #FFF8F0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}

.container {
  padding: 20rpx;
}

.card {
  background: #FFFFFF;
  border-radius: 20rpx;
  padding: 30rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 20rpx rgba(0, 0, 0, 0.05);
}

.btn-primary {
  background: linear-gradient(135deg, #FF8C42, #FFA76D);
  color: #FFFFFF;
  border: none;
  border-radius: 50rpx;
  padding: 24rpx 0;
  font-size: 32rpx;
  font-weight: 600;
}

.btn-primary:active {
  opacity: 0.8;
}

.section-title {
  font-size: 28rpx;
  font-weight: 600;
  color: #333333;
  margin-bottom: 20rpx;
}

.tag {
  display: inline-block;
  background: #FFF8F0;
  color: #FF8C42;
  padding: 12rpx 24rpx;
  border-radius: 30rpx;
  font-size: 24rpx;
  margin-right: 16rpx;
  margin-bottom: 16rpx;
  border: 2rpx solid #FFE0C8;
}

.tag.active {
  background: #FF8C42;
  color: #FFFFFF;
  border-color: #FF8C42;
}
</style>
