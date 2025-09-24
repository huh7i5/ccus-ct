<template>
  <div class="about">
    <h2>项目简介</h2>
    <p>
      欢迎访问我的 CCUS（碳捕获、利用与封存）知识图谱问答系统！本项目旨在构建一个关于 CCUS 领域的专业知识库，为关注“双碳”目标、气候变化及相关技术的用户提供一个方便、快捷的知识探索平台。通过整合海量的 CCUS 项目、技术、政策及实体数据，并利用强大的知识图谱和自然语言问答技术，我希望能为您提供关于 CCUS 领域的深入见解和独特体验。
    </p>
    <img src="/about.png" alt="CCUS Project Showcase">
    <h2>功能与特点</h2>
    <p>
      <strong>基于知识图谱的 CCUS 信息检索：</strong> 您可以便捷地查询全球及中国的CCUS项目、关键技术（如化学吸收法、膜分离法）、相关企业（如中国海油、国家能源集团）、封存地点等实体，并获取它们之间的关联信息。
    </p>
    <p>
      <strong>CCUS 领域智能问答系统：</strong> 本网站提供了强大的自然语言问答功能。您可以直接用自然语言提问，例如“中国最大的海上碳封存项目是哪个？”或者“化学吸收法的捕集效率一般是多少？”，系统将为您提供精确、全面的答案。
    </p>
    <p>
      <strong>多模态信息展示：</strong> 为了提供更丰富的信息，我整合了多种数据来源，包括文字、图表和项目图片，未来还会加入技术流程视频，为您提供更加生动、直观的内容展示。
    </p>
    <p>
      <strong>专业的 CCUS 知识库：</strong> 本项目的知识图谱和问答系统专注于 CCUS 全产业链，覆盖了从碳捕集、运输到地质封存或资源化利用的各个环节，并会持续更新，确保您获取到最新、最准确的领域知识。
    </p>
     <h2>使用方法</h2>
    <p>
      <strong>首页搜索框：</strong> 在网站首页，输入您感兴趣的 CCUS 关键词，如“恩平15-1油田”、“化学吸收法”或一个问题，然后点击搜索。搜索结果将以知识图谱和信息卡片的形式展示。
    </p>
    <p>
      <strong>多维度筛选：</strong> 在对话页面，您可以通过多轮对话来缩小搜索范围。例如，您可以根据“项目地点”、“技术类型”、“所属公司”等维度进行筛选，以快速定位目标信息。
    </p>
    <p>
      <strong>问答功能：</strong> 在问答页面直接输入关于 CCUS 的问题，系统将基于知识图谱和预训练语言模型生成详细答案。您还可以追问更多细节，进行多轮互动。
    </p>
    <p>
      <strong>知识图谱可视化：</strong> 在知识图谱页面，您可以直观地看到 CCUS 实体间的复杂关系，例如某个发电厂采用了哪种捕集技术、其捕集的二氧化碳被运往哪个油田进行封存等。您可以缩放、平移图谱，并点击节点查看详情。
    </p>
    <p>
      <strong>用户反馈：</strong> 如果您在使用过程中发现任何问题或有改进建议，欢迎通过反馈功能告知我。您的建议对我持续优化网站至关重要。
    </p>
    <p>
      <strong>实体关联探索：</strong> 点击搜索结果中的任一实体（如“胜利油田”），图谱将高亮显示其所有关联节点，助您快速了解该实体的基本信息、相关项目和技术等。
    </p>
    <p>
      <strong>个性化推荐：</strong> 根据您的浏览和搜索历史，网站会为您推荐相关的 CCUS 项目或前沿技术。您可以在首页或推荐页面查看这些内容。（即将上线）
    </p>
    <h2>技术背景</h2>
    <p>
      <strong>大规模预训练语言模型：</strong> 本网站使用基于 ChatGLM 的 62 亿参数的大规模预训练语言模型作为问答生成核心。该模型能出色地理解 CCUS 领域的专业术语和复杂问题，生成流畅、准确的回答。
    </p>
    <p>
      <strong>CCUS 领域知识图谱：</strong> 我利用先进的数据处理和图谱构建技术，从大量 CCUS 相关的研究报告、新闻资讯和项目资料中提取信息，构建了一个包含项目、技术、地点、公司、产能、投资额等多种实体和关系的结构化知识图谱。
    </p>
    <p>
      <strong>知识图谱补全：</strong> 为了确保 CCUS 知识图谱的完整性，我采用了知识图谱补全技术，自动推断并补充实体间可能存在的潜在关系，提高了知识覆盖率。
    </p>
    <p>
      <strong>统一信息抽取模型（UIE）：</strong> 我开发了一个基于深度学习的统一信息抽取模型，专门用于从非结构化的 CCUS 文本中自动抽取关键信息（如项目捕集能力、投资金额、技术效率等），实现知识库的自动化构建与更新。
    </p>
    <p>
      <strong>外部知识检索：</strong> 除了自身的知识图谱，系统还具备外部知识检索能力，可从权威来源（如国际能源署IEA、全球碳捕集与封存研究院GCCSI等）获取补充信息，提供更全面的答案。
    </p>
    <p>
      <strong>多模态信息与可视化：</strong> 本网站整合了文字、图片等数据，并使用 Echarts 进行数据可视化，将复杂的 CCUS 项目关系和产业链条以直观的图表和图谱形式呈现给用户。
    </p>
    <p>
      <strong>前后端分离的网站架构：</strong> 本网站采用前后端分离的方式搭建，前端部分使用 Vue3 框架及相关开源组件，后端部分采用 Flask 框架，确保了网站的良好性能和用户体验。
    </p>
    <p>
      通过以上技术的深度结合，我的 CCUS 知识图谱检索与问答网站致力于为用户提供高质量、个性化的 CCUS 领域知识服务。
    </p>
  </div>
</template>

<style lang="less" scoped>
.about {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #333;
  width: 80%;
  max-width: 800px;
  min-height: calc(100vh - 200px);
  margin: 0 auto;
  margin-top: 40px;
  // text-align: center;
  font-family: 'HarmonyOS Sans SC', 'Noto Sans SC', 'Source Han Sans SC', 'PingFang SC', 'Microsoft YaHei', 'WenQuanYi Micro Hei', 'WenQuanYi Zen Hei', 'ST Heiti', 'SimHei', 'WenQuanYi Zen Hei Sharp', 'Droid Sans Fallback', 'Droi';
}

img.logo {
  width: 300px;
  // height: 100px;
  margin: 2rem auto;
}

img {
  max-width: 100%;
  margin: 1rem auto;
  object-fit: contain;
  border-radius: 8px;
}

h2 {
  width: 100%;
  font-size: 1.2rem;
  line-height: 1.2rem;
  margin: 1em 0;
  border-left: 5px solid #005f77;
  padding-left: 0.8em;
}

p {
  font-size: 1rem;
  line-height: 1.8em;
  margin: 0.5em 0;
}


footer {
  margin-top: auto;
  text-align: center;
  font-size: 0.8em;
  color: #999;

  a {
    color: #999;
  }
}

</style>