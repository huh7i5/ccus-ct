<script setup>
import { KeepAlive } from 'vue'
import { RouterLink, RouterView, useRoute } from 'vue-router'

// 打印当前页面的路由信息，使用 vue3 的 setup composition API
const route = useRoute()
console.log(route)



</script>

<template>
  <div class="app-container">
    <header class="header">
      <div class="logo">
        <h1>🌱 CCUS知识图谱系统</h1>
        <p>碳捕集利用与封存技术智能问答平台</p>
      </div>
      <nav class="nav">
        <RouterLink to="/" class="nav-item" active-class="active">🏠 主页</RouterLink>
        <RouterLink to="/chat" class="nav-item" active-class="active">💬 智能问答</RouterLink>
        <RouterLink to="/kg" class="nav-item" active-class="active">🔗 知识图谱</RouterLink>
        <RouterLink to="/about" class="nav-item" active-class="active">ℹ️ 关于</RouterLink>
      </nav>
    </header>

    <main class="main-content">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </main>

    <footer class="footer">
      <p>© 2025 CCUS知识图谱系统 | 基于ChatGLM-6B + 知识图谱技术</p>
    </footer>
  </div>
</template>

<style lang="less" scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 95, 119, 0.1);
  padding: 20px 0;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
}

.logo {
  text-align: center;
  margin-bottom: 20px;

  h1 {
    margin: 0;
    color: #005f77;
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(135deg, #005f77, #00a8cc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  p {
    margin: 8px 0 0 0;
    color: #666;
    font-size: 1.1rem;
  }
}

.nav {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
}

.nav-item {
  padding: 12px 24px;
  border: 2px solid transparent;
  border-radius: 25px;
  background: rgba(255, 255, 255, 0.8);
  color: #333;
  font-size: 16px;
  font-weight: 500;
  transition: all 0.3s ease;
  text-decoration: none;
  position: relative;
  overflow: hidden;
}

.nav-item:hover {
  background: rgba(0, 95, 119, 0.1);
  border-color: #005f77;
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(0, 95, 119, 0.2);
}

.nav-item.active {
  background: linear-gradient(135deg, #005f77, #00a8cc);
  color: white;
  border-color: #005f77;
  box-shadow: 0 4px 20px rgba(0, 95, 119, 0.3);
}

.main-content {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.footer {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(0, 95, 119, 0.1);
  text-align: center;
  padding: 20px;
  color: #666;
  font-size: 14px;
}
</style>
