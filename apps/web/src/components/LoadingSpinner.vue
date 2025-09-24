<template>
  <div class="loading-spinner" v-if="visible">
    <div class="spinner-overlay" v-if="overlay"></div>
    <div class="spinner-container">
      <el-icon class="spinner-icon" :size="size">
        <Loading />
      </el-icon>
      <p v-if="text" class="spinner-text">{{ text }}</p>
    </div>
  </div>
</template>

<script>
import { Loading } from '@element-plus/icons-vue'

export default {
  name: 'LoadingSpinner',
  components: {
    Loading
  },
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    text: {
      type: String,
      default: ''
    },
    size: {
      type: Number,
      default: 40
    },
    overlay: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.loading-spinner {
  position: relative;
}

.spinner-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

.spinner-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  z-index: 1001;
}

.spinner-icon {
  animation: spin 1s linear infinite;
  color: #409EFF;
}

.spinner-text {
  margin: 0;
  color: #606266;
  font-size: 14px;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>
