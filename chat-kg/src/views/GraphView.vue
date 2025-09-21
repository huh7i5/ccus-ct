<template>
  <div class="graph-container">
    <div id="graph-main" ref="chartRef"></div>
    <div id="graph-info" v-if="state.showInfo && state.nodeInfo.length > 0">
      <div class="search-area">
        <input type="text" v-model="state.searchText" placeholder="输入关键词搜索" />
      </div>
      <div class="node-info">
        <div class="node-card" v-for="(sent, idx) in state.nodeInfo" :key="idx">
          <div class="node-sent" v-html="sent"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'

const chartRef = ref(null)
const state = reactive({
  graph: {},
  searchText: '',
  showInfo: true,
  nodeInfo: []
})

let myChart;

const fetchWebkitDepData = () => {
  axios.get('/api/graph')
    .then(response => {
      const webkitDep = response.data.data
      state.graph = webkitDep
      myChart.hideLoading()

      // 创建节点名称到ID的映射
      const nameToIdMap = {}
      webkitDep.nodes.forEach(function (node, idx) {
        node.id = idx
        nameToIdMap[node.name] = idx  // 记录名称到ID的映射
        node.label = {
          show: true,
          position: 'right',
          formatter: function(params) {
            // 截断过长的节点名称
            const name = params.data.name || ''
            return name.length > 15 ? name.substring(0, 15) + '...' : name
          },
          fontSize: 10,
          color: '#333'
        }
        // 调整节点大小，根据节点重要性，但保持适中
        node.symbolSize = Math.min(Math.max(15, Math.sqrt((node.name?.length || 5)) * 3), 35)
        // 添加节点样式
        node.itemStyle = {
          color: node.category === 0 ? '#5470c6' : '#91cc75',
          borderColor: '#fff',
          borderWidth: 1
        }
      })

      // 处理连线，将节点名称转换为ID
      webkitDep.links.forEach(function (link) {
        link.source = nameToIdMap[link.source] ?? link.source
        link.target = nameToIdMap[link.target] ?? link.target
      })

      console.log('图谱数据:', {
        节点数量: webkitDep.nodes.length,
        连线数量: webkitDep.links.length,
        前3个节点: webkitDep.nodes.slice(0, 3).map(n => ({id: n.id, name: n.name})),
        前3条连线: webkitDep.links.slice(0, 3)
      })

      const option = {
        tooltip: {
          show: true,
          showContent: true,
          trigger: 'item',
          triggerOn: 'mousemove',
          alwaysShowContent: false,
          showDelay: 0,
          hideDelay: 200,
          enterable: false,
          position: 'top',
          confine: true,
          formatter: function(params) {
            if (params.dataType === 'node') {
              // 节点悬停显示完整名称
              return `<div style="max-width: 200px; word-wrap: break-word;">
                        <strong>节点:</strong> ${params.data.name}<br/>
                        <strong>类别:</strong> ${params.data.category === 0 ? '实体1' : '实体2'}
                      </div>`
            } else if (params.dataType === 'edge') {
              // 边悬停显示关系信息
              return `<div style="max-width: 200px; word-wrap: break-word;">
                        <strong>关系:</strong> ${params.data.value || params.data.name}<br/>
                        <strong>源节点:</strong> ${webkitDep.nodes[params.data.source]?.name || params.data.source}<br/>
                        <strong>目标节点:</strong> ${webkitDep.nodes[params.data.target]?.name || params.data.target}
                      </div>`
            }
            return ''
          }
        },
        series: [
          {
            type: 'graph',
            layout: 'force',
            animation: false,
            label: {
              position: 'right',
              formatter: '{b}'
            },
            draggable: true,
            data: webkitDep.nodes,
            modularity: true, // 开启社区划分
            categories: webkitDep.categories,
            force: {
              edgeLength: 120,       // 进一步增加边长
              repulsion: 300,        // 增加斥力，处理更多节点
              gravity: 0.05,         // 进一步减少重力
              layoutAnimation: true,
              friction: 0.6          // 添加摩擦力，让布局更稳定
            },
            lineStyle: {
              color: '#aaa',
              width: 1,
              curveness: 0.2,
              opacity: 0.7
            },
            edgeLabel: {
              show: false,  // 默认不显示关系标签
              fontSize: 10,
              color: '#666',
              formatter: '{c}'
            },
            links: webkitDep.links,
            roam: true, // 开启鼠标缩放和平移漫游
            emphasis: {
              focus: 'adjacency' // 高亮显示鼠标移入节点的邻接节点
            },
          }
        ],
        // animationDuration: 1500, // 初始动画的时长
        // animationEasingUpdate: 'quinticInOut', // 数据更新动画的缓动效果
      }
      myChart.setOption(option)
    })
    .catch(error => {
      console.error('Failed to load graph data:', error)
      myChart.hideLoading()
      // 显示空图谱或错误信息
      myChart.setOption({
        title: {
          text: '图谱加载失败',
          left: 'center',
          top: 'center'
        }
      })
    })
}

const getNeighborNodes = (node) => {
  const nodes = []
  // 遍历所有的边，找到与当前节点相连的节点
  state.graph.links.forEach(function (link) {
    if (link.source === node.id || link.target === node.id) {
      nodes.push(state.graph.nodes[link.source])
      nodes.push(state.graph.nodes[link.target])
    }
  })

  // 去除当前节点
  nodes.forEach(function (item, index) {
    if (item.id === node.id) {
      nodes.splice(index, 1)
    }
  })

  return nodes
}

const colorfulSents = (node, nerborNodes, sents) => {
  const nerborNodeNames = nerborNodes.map((item) => item.name)
  console.log(nerborNodeNames)
  const colorfulSents = sents.map((sent) => {
    sent = sent.replace(node.name, `<span style="color: #47c640">${node.name}</span>`)
    nerborNodeNames.forEach((name) => {
      sent = sent.replace(name, `<span style="color: #df2024">${name}</span>`)
    })
    return sent
  })
  return colorfulSents
}

const clickNode = (param) => {
  console.log('点击了', param)

  if (param.dataType === 'node' && param.data) {
    state.showInfo = true

    // 检查数据结构，避免undefined错误
    if (param.data.lines && state.graph.sents) {
      const sents = param.data.lines.map((item) => state.graph.sents[item])
      const nerborNodes = getNeighborNodes(param.data)
      state.nodeInfo = colorfulSents(param.data, nerborNodes, sents)
    } else {
      // 如果没有句子数据，显示节点基本信息
      state.nodeInfo = [
        `节点名称: ${param.data.name || '未知'}`,
        `节点类别: ${param.data.category || '未知'}`,
        `节点ID: ${param.data.id || '未知'}`
      ]
    }
  }
}

onMounted(() => {
  myChart = echarts.init(chartRef.value)
  myChart.showLoading()
  fetchWebkitDepData()
  myChart.on('click', clickNode)
})
</script>

<style lang="less" scoped>
.graph-container {
  display: flex;
  flex-direction: row;
  max-width: 100%;
  height: calc(100vh - 200px);
  gap: 20px;
}

#graph-main,
#graph-info {
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  height: 100%;
  background: #f5f5f5;
  border-radius: 8px;
}

#graph-main {
  width: 100%;
}

#graph-info {
  width: 400px;
  padding: 2rem 1rem;
  overflow: scroll;

  .search-area {
    // 优化 input 和 button 的样式
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 40px;
    margin-bottom: 1rem;

    input {
      flex: 1;
      width: 100%;
      padding: 0.5rem 1rem;
      background-color: #fff;
      border: none;
      border-radius: 8px;
      // box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.1), 0 1px 2px rgba(0, 0, 0, 0.1);
      font-size: 0.8rem;
      margin: 1rem 1rem;
      color: #111111;
      line-height: 22px;
      font-variation-settings: 'wght' 400, 'opsz' 10.5;
      transition: all 0.3s;
    }

    input:focus {
      outline: 2px solid #999;
    }

    // place holder
    input::-webkit-input-placeholder {
      color: #999999;
    }
  }
}

#graph-info,
.node-info {
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  overflow: scroll;

  // 隐藏滚动条
  &::-webkit-scrollbar {
    display: none;
  }
}

.node-info {
  display: flex;
  flex-direction: column;
  justify-content: start;
  align-items: center;
  width: 100%;
  height: 100%;
  overflow: scroll;
}

#graph-info .node-sent {
  margin: 1rem 0;
  padding: 1rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 0 0 1px rgba(0, 0, 0, 0.05);
  font-size: 0.8rem;
  color: #111111;
  line-height: 22px;
  font-variation-settings: 'wght' 400, 'opsz' 10.5;
  transition: all 0.3s;
}
</style>
