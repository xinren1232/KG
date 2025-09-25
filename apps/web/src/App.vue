<template>
  <div id="app">
    <el-container>
      <!-- 顶部导航 -->
      <el-header>
        <div class="header-content">
          <h1 class="title">📱 质量知识图谱助手</h1>
          <el-menu
            :default-active="$route.path"
            mode="horizontal"
            router
            class="nav-menu"
          >
            <el-menu-item index="/">
              <el-icon><House /></el-icon>
              首页
            </el-menu-item>
            <el-menu-item index="/extract">
              <el-icon><Document /></el-icon>
              文档解析
            </el-menu-item>
            <el-menu-item index="/graph">
              <el-icon><Share /></el-icon>
              知识图谱
            </el-menu-item>
            <el-menu-item index="/dictionary">
              <el-icon><Collection /></el-icon>
              词典管理
            </el-menu-item>
            <el-menu-item index="/governance">
              <el-icon><Setting /></el-icon>
              数据治理
            </el-menu-item>


          </el-menu>
        </div>
      </el-header>

      <!-- 主内容区 -->
      <el-main>
        <router-view />
      </el-main>

      <!-- 底部 -->
      <el-footer>
        <div class="footer-content">
          <p>&copy; 2024 质量知识图谱助手 - 手机研发质量部门</p>
        </div>
      </el-footer>
    </el-container>
  </div>
</template>

<script>
import { House, Document, Share, Collection, Setting } from '@element-plus/icons-vue'

export default {
  name: 'App',
  components: {
    House,
    Document,
    Share,
    Collection,
    Setting
  }
}
</script>

<style>
#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
  min-height: 100vh;
}

.el-header {
  background-color: #409EFF;
  color: white;
  padding: 0;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 100%;
  padding: 0 20px;
}

.title {
  margin: 0;
  font-size: 24px;
  font-weight: bold;
}

.nav-menu {
  background-color: transparent;
  border: none;
  flex: 1;
  display: flex;
  justify-content: flex-end;
}

.nav-menu .el-menu-item {
  color: white;
  border-bottom: 2px solid transparent;
  white-space: nowrap;
  min-width: auto;
}

.nav-menu .el-menu-item:hover,
.nav-menu .el-menu-item.is-active {
  background-color: rgba(255, 255, 255, 0.1);
  border-bottom-color: white;
  color: white;
}

.el-main {
  padding: 20px;
  min-height: calc(100vh - 120px);
}

.el-footer {
  background-color: #f5f5f5;
  border-top: 1px solid #e4e7ed;
}

.footer-content {
  text-align: center;
  color: #909399;
  line-height: 60px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    height: auto;
    padding: 10px;
  }

  .title {
    font-size: 20px;
    margin-bottom: 10px;
  }

  .nav-menu {
    width: 100%;
    justify-content: center;
  }

  .nav-menu .el-menu-item {
    font-size: 14px;
    padding: 0 10px;
  }
}

@media (max-width: 1200px) {
  .nav-menu .el-menu-item {
    padding: 0 15px;
    font-size: 14px;
  }
}
</style>
