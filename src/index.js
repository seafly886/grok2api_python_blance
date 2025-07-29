import { Container, getContainer } from "@cloudflare/containers";

// 自定义容器类
export class GrokContainer extends Container {
  defaultPort = 8698;   // 必须与 Dockerfile EXPOSE 端口一致
  sleepAfter = "15m";   // 空闲15分钟后休眠
}

// Worker 请求处理器
export default {
  async fetch(request, env) {
    try {
      const container = getContainer(env.GROK_CONTAINER);
      return container.fetch(request);
    } catch (error) {
      return new Response(`Container error: ${error.message}`, { status: 500 });
    }
  }
};
