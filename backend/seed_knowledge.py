"""
编程知识种子脚本 - 为 RAG 系统填充 Java 全栈及其他编程知识
Usage: cd backend && python seed_knowledge.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.db.sqlite import SessionLocal, engine, Base
from app.services.knowledge import knowledge_service

Base.metadata.create_all(bind=engine)

KNOWLEDGE_ITEMS = [
    # ==================== Java 核心 ====================
    {
        "title": "Java 集合框架概览",
        "content_type": "markdown",
        "category": "Java",
        "tags": ["java", "collections", "基础"],
        "content": """# Java 集合框架

## 主要接口
- **Collection**: List, Set, Queue 的父接口
- **Map**: 键值对映射，独立于 Collection 体系

## List 实现
| 实现类 | 底层结构 | 线程安全 | 特点 |
|--------|----------|----------|------|
| ArrayList | 动态数组 | 否 | 随机访问 O(1)，插入删除 O(n) |
| LinkedList | 双向链表 | 否 | 随机访问 O(n)，插入删除 O(1) |
| Vector | 动态数组 | 是 | 已过时，不推荐使用 |
| CopyOnWriteArrayList | 写时复制数组 | 是 | 读多写少场景 |

## Set 实现
| 实现类 | 底层结构 | 是否有序 | 是否允许null |
|--------|----------|----------|-------------|
| HashSet | HashMap | 无序 | 允许1个 |
| LinkedHashSet | LinkedHashMap | 插入序 | 允许1个 |
| TreeSet | 红黑树 | 自然排序 | 不允许 |

## Map 实现
| 实现类 | 底层结构 | 线程安全 | 有序性 |
|--------|----------|----------|--------|
| HashMap | 数组+链表+红黑树 | 否 | 无序 |
| LinkedHashMap | 双向链表+HashMap | 否 | 插入/访问序 |
| TreeMap | 红黑树 | 否 | key排序 |
| ConcurrentHashMap | 分段锁/Node数组 | 是 | 无序 |

## 常见面试要点
1. HashMap 默认容量16，负载因子0.75，链表长度>=8转红黑树
2. HashSet 底层就是 HashMap，value 固定为 PRESENT 常量
3. fail-fast 机制：遍历时修改集合会抛 ConcurrentModificationException
4. fail-safe 机制：java.util.concurrent 包下的集合支持并发修改"""
    },
    {
        "title": "Java 多线程与并发编程",
        "content_type": "markdown",
        "category": "Java",
        "tags": ["java", "concurrency", "多线程", "并发"],
        "content": """# Java 多线程与并发编程

## 线程创建方式
1. **继承 Thread 类**: 重写 run() 方法
2. **实现 Runnable 接口**: 推荐，支持多继承
3. **实现 Callable 接口**: 支持返回值和异常
4. **线程池**: 通过 ExecutorService 管理

## 线程池核心参数
```java
ThreadPoolExecutor(
    int corePoolSize,        // 核心线程数
    int maximumPoolSize,     // 最大线程数
    long keepAliveTime,      // 空闲线程存活时间
    TimeUnit unit,           // 时间单位
    BlockingQueue<Runnable> workQueue,  // 任务队列
    ThreadFactory threadFactory,         // 线程工厂
    RejectedExecutionHandler handler     // 拒绝策略
)
```

## 四种拒绝策略
- AbortPolicy: 抛出 RejectedExecutionException（默认）
- CallerRunsPolicy: 由提交任务的线程执行
- DiscardPolicy: 静默丢弃
- DiscardOldestPolicy: 丢弃队列最老的任务

## synchronized vs ReentrantLock
| 特性 | synchronized | ReentrantLock |
|------|-------------|---------------|
| 释放锁 | 自动 | 手动 unlock() |
| 可中断 | 不可 | lockInterruptibly() |
| 超时 | 不支持 | tryLock(timeout) |
| 公平锁 | 不支持 | new ReentrantLock(true) |
| 条件变量 | wait/notify | Condition |

## volatile 关键字
- 保证可见性：修改立即刷新到主内存
- 禁止指令重排序
- 不保证原子性：i++ 仍需加锁

## JUC 常用工具类
- CountDownLatch: 倒计数门闩，等待N个任务完成
- CyclicBarrier: 循环屏障，N个线程互相等待
- Semaphore: 信号量，控制并发访问数
- CompletableFuture: 异步编程，支持链式调用"""
    },
    {
        "title": "JVM 内存模型与垃圾回收",
        "content_type": "markdown",
        "category": "Java",
        "tags": ["java", "jvm", "gc", "内存"],
        "content": """# JVM 内存模型与垃圾回收

## JVM 内存区域
1. **堆 (Heap)**: 对象实例，GC 主要区域
   - 新生代: Eden + Survivor(From/To)，默认比例 8:1:1
   - 老年代: 长期存活对象
2. **方法区/元空间 (Metaspace)**: 类信息、常量池、静态变量
3. **虚拟机栈**: 线程私有，每个方法对应一个栈帧
4. **本地方法栈**: Native 方法
5. **程序计数器**: 当前执行指令地址

## 垃圾回收算法
- **标记-清除**: 产生内存碎片
- **标记-整理**: 无碎片但需移动对象
- **复制算法**: 新生代使用，空间换时间
- **分代收集**: 新生代用复制，老年代用标记整理

## 常见垃圾收集器
| 收集器 | 区域 | 算法 | 特点 |
|--------|------|------|------|
| Serial | 新生代 | 复制 | 单线程，STW |
| ParNew | 新生代 | 复制 | 多线程版Serial |
| Parallel Scavenge | 新生代 | 复制 | 吞吐量优先 |
| CMS | 老年代 | 标记清除 | 低延迟 |
| G1 | 全堆 | 分区 | JDK9默认 |
| ZGC | 全堆 | 染色指针 | 超低延迟 |

## JVM 调优参数
```
-Xms: 初始堆大小
-Xmx: 最大堆大小
-Xmn: 新生代大小
-XX:MetaspaceSize: 元空间初始大小
-XX:+UseG1GC: 使用G1收集器
-XX:MaxGCPauseMillis: 最大GC停顿时间
-XX:+HeapDumpOnOutOfMemoryError: OOM时dump堆
```

## 对象存活判定
- 引用计数法: 有循环引用问题
- 可达性分析: 从GC Roots出发，不可达即为垃圾
- GC Roots: 虚拟机栈引用、静态变量、常量、JNI引用"""
    },
    {
        "title": "Spring Boot 自动配置原理",
        "content_type": "markdown",
        "category": "Java",
        "tags": ["java", "spring", "springboot", "自动配置"],
        "content": """# Spring Boot 自动配置原理

## 启动流程
1. `@SpringBootApplication` = `@SpringBootConfiguration` + `@EnableAutoConfiguration` + `@ComponentScan`
2. `@EnableAutoConfiguration` 通过 `@Import(AutoConfigurationImportSelector)` 触发自动配置
3. AutoConfigurationImportSelector 读取 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports`
4. 结合 `@ConditionalOnClass`、`@ConditionalOnBean` 等条件注解过滤配置类

## 核心条件注解
| 注解 | 含义 |
|------|------|
| @ConditionalOnClass | classpath 存在指定类 |
| @ConditionalOnMissingBean | 容器中不存在指定 Bean |
| @ConditionalOnProperty | 配置属性满足条件 |
| @ConditionalOnWebApplication | 是 Web 应用 |

## 自定义 Starter 步骤
1. 创建 `xxx-spring-boot-autoconfigure` 模块
2. 编写自动配置类 + `@Configuration` + 条件注解
3. 编写 `XxxProperties` + `@ConfigurationProperties`
4. 在 `META-INF/spring/org.springframework.boot.autoconfigure.AutoConfiguration.imports` 中注册
5. 创建 `xxx-spring-boot-starter` 模块，依赖 autoconfigure 模块

## 配置加载顺序
1. 命令行参数
2. JNDI 属性
3. Java 系统属性
4. 操作系统环境变量
5. application-{profile}.yml
6. application.yml
7. @PropertySource
8. 默认属性

## 常用注解速查
- `@RestController` = `@Controller` + `@ResponseBody`
- `@PathVariable`: URL 路径变量
- `@RequestParam`: 查询参数
- `@RequestBody`: 请求体 JSON
- `@Transactional`: 事务管理
- `@Cacheable`: 缓存
- `@Async`: 异步执行"""
    },
    {
        "title": "Spring Cloud 微服务架构",
        "content_type": "markdown",
        "category": "Java",
        "tags": ["java", "spring", "springcloud", "微服务"],
        "content": """# Spring Cloud 微服务架构

## 核心组件
1. **服务注册与发现**: Nacos / Eureka / Consul
2. **配置中心**: Nacos Config / Apollo / Spring Cloud Config
3. **服务调用**: OpenFeign / RestTemplate
4. **负载均衡**: Spring Cloud LoadBalancer / Ribbon
5. **熔断降级**: Sentinel / Resilience4j / Hystrix(已停更)
6. **网关**: Spring Cloud Gateway / Zuul
7. **链路追踪**: Micrometer Tracing + Zipkin / SkyWalking

## Nacos 使用要点
```yaml
# bootstrap.yml
spring:
  cloud:
    nacos:
      discovery:
        server-addr: localhost:8848
      config:
        server-addr: localhost:8848
        file-extension: yml
```

## OpenFeign 声明式调用
```java
@FeignClient(name = "user-service", fallback = UserFallback.class)
public interface UserClient {
    @GetMapping("/user/{id}")
    User getUser(@PathVariable Long id);
}
```

## Sentinel 熔断规则
- 慢调用比例：响应时间 > 阈值的比例超过阈值则熔断
- 异常比例：异常比例超过阈值则熔断
- 异常数：异常数超过阈值则熔断

## Gateway 路由配置
```yaml
spring:
  cloud:
    gateway:
      routes:
        - id: user-service
          uri: lb://user-service
          predicates:
            - Path=/api/user/**
          filters:
            - StripPrefix=1
```

## 微服务设计原则
- 单一职责：每个服务只负责一个业务领域
- 服务自治：独立部署、独立数据库
- 轻量通信：REST / gRPC / 消息队列
- 接口幂等：防止重复提交"""
    },
    {
        "title": "MySQL 索引优化与查询调优",
        "content_type": "markdown",
        "category": "数据库",
        "tags": ["mysql", "索引", "优化", "sql"],
        "content": """# MySQL 索引优化与查询调优

## 索引类型
- **B+Tree 索引**: InnoDB 默认，适合范围查询
- **Hash 索引**: Memory 引擎，等值查询 O(1)
- **全文索引**: FULLTEXT，适合文本搜索
- **空间索引**: R-Tree，GIS 数据

## 聚簇索引 vs 非聚簇索引
- 聚簇索引：叶子节点存储完整行数据，InnoDB 主键索引
- 非聚簇索引（二级索引）：叶子节点存储主键值，需要回表
- 覆盖索引：查询字段全在索引中，无需回表

## 索引失效场景
1. 对索引列使用函数或计算
2. 隐式类型转换（varchar 列用 int 查询）
3. LIKE '%xxx' 左模糊
4. OR 连接非索引列
5. 不满足最左前缀原则
6. 使用 != 或 NOT IN
7. IS NULL / IS NOT NULL（取决于数据分布）

## EXPLAIN 关键字段
| 字段 | 含义 |
|------|------|
| type | 访问类型：ALL < index < range < ref < eq_ref < const |
| key | 实际使用的索引 |
| rows | 预估扫描行数 |
| Extra | Using index(覆盖索引)、Using filesort(文件排序)、Using temporary(临时表) |

## SQL 优化技巧
1. 小表驱动大表：EXISTS vs IN 选择
2. 分页优化：延迟关联 `SELECT * FROM t INNER JOIN (SELECT id FROM t LIMIT 100000,10) tmp ON t.id = tmp.id`
3. 批量插入代替逐条插入
4. 合理使用联合索引，避免冗余索引
5. COUNT(*) vs COUNT(1) vs COUNT(col)：前两者等价且最优"""
    },
    {
        "title": "Redis 数据结构与应用场景",
        "content_type": "markdown",
        "category": "数据库",
        "tags": ["redis", "缓存", "nosql"],
        "content": """# Redis 数据结构与应用场景

## 五大基本数据类型
| 类型 | 底层实现 | 典型场景 |
|------|----------|----------|
| String | SDS | 缓存、计数器、分布式锁 |
| List | 双向链表/压缩列表 | 消息队列、最新列表 |
| Hash | 哈希表/压缩列表 | 对象存储、购物车 |
| Set | 哈希表/整数集合 | 标签、共同好友 |
| ZSet | 跳表+哈希表 | 排行榜、延迟队列 |

## 高级数据类型
- **Bitmap**: 用户签到、在线状态
- **HyperLogLog**: UV 统计（误差 0.81%）
- **GeoSpatial**: 附近的人、距离计算
- **Stream**: 消息队列（Redis 5.0+）

## 缓存三大问题
1. **缓存穿透**: 查询不存在的数据 → 布隆过滤器 / 缓存空值
2. **缓存击穿**: 热点key过期 → 互斥锁 / 永不过期
3. **缓存雪崩**: 大量key同时过期 → 随机过期时间 / 多级缓存

## 分布式锁实现
```lua
-- 加锁（原子操作）
SET lock_key unique_value NX PX 30000

-- 释放锁（Lua 脚本保证原子性）
if redis.call('get', KEYS[1]) == ARGV[1] then
    return redis.call('del', KEYS[1])
else
    return 0
end
```

## 持久化机制
- **RDB**: 定时快照，恢复快但可能丢数据
- **AOF**: 追加写命令，数据安全但文件大
- **混合持久化**: RDB+AOF，Redis 4.0+ 推荐

## Redis Cluster
- 16384 个 slot 分布在多个节点
- 每个节点负责一部分 slot
- 支持自动故障转移"""
    },
    {
        "title": "MySQL 事务与锁机制",
        "content_type": "markdown",
        "category": "数据库",
        "tags": ["mysql", "事务", "锁", "mvcc"],
        "content": """# MySQL 事务与锁机制

## ACID 特性
- **Atomicity 原子性**: undo log 实现回滚
- **Consistency 一致性**: 由其他三个特性保证
- **Isolation 隔离性**: MVCC + 锁机制
- **Durability 持久性**: redo log 保证

## 四种隔离级别
| 隔离级别 | 脏读 | 不可重复读 | 幻读 |
|----------|------|-----------|------|
| READ UNCOMMITTED | ✓ | ✓ | ✓ |
| READ COMMITTED | ✗ | ✓ | ✓ |
| REPEATABLE READ (默认) | ✗ | ✗ | ✗(InnoDB通过间隙锁解决) |
| SERIALIZABLE | ✗ | ✗ | ✗ |

## InnoDB 锁类型
- **共享锁 (S)**: SELECT ... LOCK IN SHARE MODE
- **排他锁 (X)**: SELECT ... FOR UPDATE / INSERT / UPDATE / DELETE
- **意向锁**: 表级锁，表明事务意图加行级S/X锁
- **记录锁**: 锁定索引记录
- **间隙锁 (Gap Lock)**: 锁定索引记录之间的间隙
- **临键锁 (Next-Key Lock)**: 记录锁 + 间隙锁，InnoDB 默认

## MVCC 实现原理
- 每行数据隐藏字段：DB_TRX_ID（事务ID）、DB_ROLL_PTR（回滚指针）
- undo log 构成版本链
- ReadView 快照判断数据可见性
- RC 每次 SELECT 创建新 ReadView
- RR 只在事务第一次 SELECT 创建 ReadView

## 死锁处理
1. 等待超时：innodb_lock_wait_timeout（默认50秒）
2. 死锁检测：innodb_deadlock_detect = ON
3. 预防：固定加锁顺序、减小事务粒度、使用低隔离级别"""
    },
    # ==================== 前端 ====================
    {
        "title": "React Hooks 核心用法",
        "content_type": "markdown",
        "category": "前端",
        "tags": ["react", "hooks", "javascript", "前端"],
        "content": """# React Hooks 核心用法

## useState
```jsx
const [state, setState] = useState(initialState);
// 函数式更新（避免闭包陷阱）
setState(prev => prev + 1);
```

## useEffect
```jsx
useEffect(() => {
  // 副作用逻辑
  return () => {
    // 清理函数
  };
}, [dependencies]); // 依赖数组
```
- 空数组 `[]`: 仅 mount 时执行
- 无数组: 每次渲染执行
- 有依赖: 依赖变化时执行

## useCallback & useMemo
```jsx
// useCallback: 缓存函数引用
const memoizedFn = useCallback(() => {
  doSomething(a, b);
}, [a, b]);

// useMemo: 缓存计算结果
const memoizedValue = useMemo(() => {
  return computeExpensiveValue(a, b);
}, [a, b]);
```

## useRef
```jsx
const ref = useRef(initialValue);
// ref.current 可变，不触发重新渲染
// 常用场景：DOM 引用、定时器ID、前一个值
```

## 自定义 Hook 规则
1. 函数名以 `use` 开头
2. 只在顶层调用，不在条件/循环中
3. 只在 React 函数组件或其他 Hook 中调用
4. 可以返回任意值

## 常用自定义 Hook 模式
- `useDebounce`: 防抖值
- `useLocalStorage`: 本地存储同步
- `useFetch`: 数据请求
- `useMediaQuery`: 响应式断点
- `usePrevious`: 前一个值"""
    },
    {
        "title": "Next.js App Router 核心概念",
        "content_type": "markdown",
        "category": "前端",
        "tags": ["nextjs", "react", "ssr", "前端"],
        "content": """# Next.js App Router 核心概念

## 服务端组件 vs 客户端组件
- 默认所有组件都是**服务端组件**
- 添加 `'use client'` 声明为客户端组件
- 服务端组件不能使用 useState、useEffect 等 Hook
- 服务端组件可以直接访问数据库、文件系统

## 特殊文件约定
| 文件名 | 作用 |
|--------|------|
| layout.tsx | 布局组件，嵌套路由共享 |
| page.tsx | 页面组件，对应路由 |
| loading.tsx | 加载状态 UI |
| error.tsx | 错误边界 |
| not-found.tsx | 404 页面 |
| route.tsx | API 路由 |

## 数据获取
```tsx
// 服务端组件直接 async
async function Page() {
  const data = await fetch('https://api.example.com', {
    cache: 'no-store' // 或 'force-cache'
  });
  return <div>{/* render data */}</div>;
}
```

## 动态路由
```
app/
  blog/
    [slug]/page.tsx      → /blog/:slug
    [...slug]/page.tsx   → /blog/* (catch-all)
    [[...slug]]/page.tsx → /blog/* (可选 catch-all)
```

## API Route
```tsx
// app/api/hello/route.ts
export async function GET(request: Request) {
  return Response.json({ message: 'Hello' });
}

export async function POST(request: Request) {
  const body = await request.json();
  return Response.json({ received: body });
}
```

## 中间件 (Middleware)
```tsx
// middleware.ts (项目根目录)
import { NextResponse } from 'next/server';
export function middleware(request) {
  return NextResponse.redirect(new URL('/home', request.url));
}
export const config = { matcher: '/api/:path*' };"""
    },
    {
        "title": "TypeScript 类型体操常用技巧",
        "content_type": "markdown",
        "category": "前端",
        "tags": ["typescript", "类型", "前端"],
        "content": """# TypeScript 类型体操常用技巧

## 基础工具类型
```typescript
// Partial: 所有属性可选
type Partial<T> = { [P in keyof T]?: T[P] };

// Required: 所有属性必填
type Required<T> = { [P in keyof T]-?: T[P] };

// Readonly: 所有属性只读
type Readonly<T> = { readonly [P in keyof T]: T[P] };

// Pick: 选取部分属性
type Pick<T, K extends keyof T> = { [P in K]: T[P] };

// Omit: 排除部分属性
type Omit<T, K extends keyof any> = Pick<T, Exclude<keyof T, K>>;
```

## 条件类型
```typescript
type IsString<T> = T extends string ? true : false;

// infer 推断
type ReturnType<T> = T extends (...args: any[]) => infer R ? R : never;
type ElementType<T> = T extends Array<infer E> ? E : never;
```

## 映射类型
```typescript
// 将所有属性变为可空
type Nullable<T> = { [K in keyof T]: T[K] | null };

// 将所有方法变为 Promise
type AsyncMethods<T> = {
  [K in keyof T]: T[K] extends (...args: infer A) => infer R
    ? (...args: A) => Promise<R>
    : T[K];
};
```

## 模板字面量类型
```typescript
type EventName = `on${Capitalize<'click' | 'change' | 'submit'>}`;
// 结果: 'onClick' | 'onChange' | 'onSubmit'

type CSSValue = `${number}px` | `${number}%` | `${number}rem`;
```

## 实用技巧
```typescript
// 非空断言
function getLength(arr: any[] | undefined) {
  return arr!.length;
}

// 可辨识联合
type Shape =
  | { kind: 'circle'; radius: number }
  | { kind: 'rect'; width: number; height: number };

function area(s: Shape) {
  switch (s.kind) {
    case 'circle': return Math.PI * s.radius ** 2;
    case 'rect': return s.width * s.height;
  }
}"""
    },
    # ==================== 工具与DevOps ====================
    {
        "title": "Git 常用操作与工作流",
        "content_type": "markdown",
        "category": "工具",
        "tags": ["git", "版本控制", "工具"],
        "content": """# Git 常用操作与工作流

## 基础命令速查
```bash
git init                          # 初始化仓库
git clone <url>                   # 克隆仓库
git add .                         # 暂存所有更改
git commit -m "message"           # 提交
git push origin <branch>          # 推送
git pull --rebase                 # 拉取并变基
git fetch                         # 获取远程更新（不合并）
```

## 分支操作
```bash
git branch                        # 列出本地分支
git branch -a                     # 列出所有分支
git checkout -b feature/xxx       # 创建并切换分支
git branch -d feature/xxx         # 删除分支
git push origin --delete branch   # 删除远程分支
```

## 撤销操作
```bash
git reset --soft HEAD~1           # 撤销提交，保留暂存区
git reset --mixed HEAD~1          # 撤销提交，取消暂存
git reset --hard HEAD~1           # 撤销提交，丢弃更改（危险）
git restore <file>                # 丢弃工作区更改
git restore --staged <file>       # 取消暂存
git stash                         # 暂存当前更改
git stash pop                     # 恢复暂存的更改
```

## Git Flow 工作流
- **main**: 生产环境代码
- **develop**: 开发主线
- **feature/***: 功能分支，从 develop 创建
- **release/***: 发布分支，从 develop 创建
- **hotfix/***: 紧急修复，从 main 创建

## Commit 规范 (Conventional Commits)
```
<type>(<scope>): <description>

feat:     新功能
fix:      Bug 修复
docs:     文档变更
style:    代码格式（不影响逻辑）
refactor: 重构
perf:     性能优化
test:     测试相关
chore:    构建/工具变更
```

## 常见问题解决
```bash
# 修改最近一次提交信息
git commit --amend

# 合并多个提交（交互式变基）
git rebase -i HEAD~3

# 解决冲突后继续变基
git rebase --continue

# 查看某个文件的修改历史
git log -p <file>

# 查看某行代码的修改人
git blame <file>"""
    },
    {
        "title": "Docker 容器化基础",
        "content_type": "markdown",
        "category": "工具",
        "tags": ["docker", "容器", "devops"],
        "content": """# Docker 容器化基础

## 核心概念
- **镜像 (Image)**: 只读模板，分层存储
- **容器 (Container)**: 镜像的运行实例
- **仓库 (Registry)**: 镜像存储，如 Docker Hub
- **Dockerfile**: 构建镜像的脚本

## 常用命令
```bash
docker images                     # 列出镜像
docker pull <image>               # 拉取镜像
docker build -t <name> .          # 构建镜像
docker run -d -p 8080:80 <image>  # 运行容器
docker ps                         # 查看运行中的容器
docker logs <container>           # 查看日志
docker exec -it <container> bash  # 进入容器
docker stop <container>           # 停止容器
docker rm <container>             # 删除容器
docker system prune               # 清理无用资源
```

## Dockerfile 最佳实践
```dockerfile
# 多阶段构建
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/dist ./dist
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
CMD ["node", "dist/main.js"]
```

## Docker Compose
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    depends_on:
      - db
    volumes:
      - ./data:/app/data
  db:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: secret
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

## 网络与存储
- **bridge**: 默认网络模式，容器间可通信
- **host**: 使用宿主机网络
- **volume**: Docker 管理的持久化存储
- **bind mount**: 挂载宿主机目录"""
    },
    {
        "title": "Linux 常用命令速查",
        "content_type": "markdown",
        "category": "工具",
        "tags": ["linux", "命令行", "运维"],
        "content": """# Linux 常用命令速查

## 文件操作
```bash
ls -la                            # 列出文件（含隐藏）
cd /path                          # 切换目录
pwd                               # 当前目录
mkdir -p dir1/dir2                # 递归创建目录
cp -r src dst                     # 复制目录
mv old new                        # 移动/重命名
rm -rf dir                        # 强制删除目录
ln -s target link                 # 创建软链接
find /path -name "*.log"          # 按名查找
find /path -size +100M            # 按大小查找
```

## 文本处理
```bash
cat file                          # 查看文件
head -n 20 file                   # 前20行
tail -f file                      # 实时跟踪
grep -rn "pattern" /path          # 递归搜索
grep -i "pattern" file            # 忽略大小写
sed -i 's/old/new/g' file         # 替换文本
awk '{print $1}' file             # 提取第一列
wc -l file                        # 统计行数
sort file | uniq                  # 排序去重
```

## 系统管理
```bash
top                               # 系统资源监控
htop                              # 增强版 top
df -h                             # 磁盘使用
du -sh *                          # 目录大小
free -h                           # 内存使用
ps aux | grep java                # 查找进程
kill -9 <pid>                     # 强制杀进程
systemctl status nginx            # 服务状态
journalctl -u nginx -f            # 查看服务日志
```

## 网络
```bash
curl -X GET http://url            # HTTP 请求
wget http://url -O file           # 下载文件
netstat -tlnp                     # 查看端口
ss -tlnp                          # 更好的端口查看
ping host                         # 测试连通性
traceroute host                    # 路由追踪
iptables -L                       # 查看防火墙规则
```

## 权限管理
```bash
chmod 755 file                    # 设置权限 (rwxr-xr-x)
chmod +x script.sh                # 添加执行权限
chown user:group file             # 修改所有者
sudo command                      # 以 root 执行"""
    },
    # ==================== 设计模式与架构 ====================
    {
        "title": "常用设计模式 (Java 示例)",
        "content_type": "markdown",
        "category": "架构",
        "tags": ["设计模式", "java", "架构"],
        "content": """# 常用设计模式 (Java 示例)

## 单例模式
```java
// 双重检查锁（推荐）
public class Singleton {
    private static volatile Singleton instance;
    private Singleton() {}
    public static Singleton getInstance() {
        if (instance == null) {
            synchronized (Singleton.class) {
                if (instance == null) {
                    instance = new Singleton();
                }
            }
        }
        return instance;
    }
}

// 枚举实现（最佳实践）
public enum Singleton {
    INSTANCE;
}
```

## 工厂模式
```java
// 简单工厂
public class PaymentFactory {
    public static Payment createPayment(String type) {
        return switch (type) {
            case "alipay" -> new AlipayPayment();
            case "wechat" -> new WechatPayment();
            default -> throw new IllegalArgumentException();
        };
    }
}
```

## 策略模式
```java
public interface SortStrategy {
    void sort(int[] arr);
}

public class Context {
    private SortStrategy strategy;
    public void setStrategy(SortStrategy s) { this.strategy = s; }
    public void executeSort(int[] arr) { strategy.sort(arr); }
}
```

## 观察者模式
```java
// Spring 事件机制就是观察者模式
@Service
public class OrderService {
    @Autowired
    private ApplicationEventPublisher publisher;

    public void createOrder(Order order) {
        // 创建订单逻辑
        publisher.publishEvent(new OrderCreatedEvent(order));
    }
}

@Component
public class OrderEventListener {
    @EventListener
    public void onOrderCreated(OrderCreatedEvent event) {
        // 发送通知、更新库存等
    }
}
```

## 代理模式
- **静态代理**: 手动编写代理类
- **JDK 动态代理**: 基于接口，Proxy.newProxyInstance()
- **CGLIB 动态代理**: 基于继承，Spring AOP 默认方式

## 模板方法模式
```java
public abstract class AbstractExportService {
    // 模板方法
    public final void export() {
        List<Data> data = queryData();
        byte[] file = generateFile(data);
        uploadFile(file);
    }
    protected abstract List<Data> queryData();
    protected abstract byte[] generateFile(List<Data> data);
}"""
    },
    {
        "title": "RESTful API 设计规范",
        "content_type": "markdown",
        "category": "架构",
        "tags": ["api", "rest", "设计规范"],
        "content": """# RESTful API 设计规范

## URL 设计原则
```
GET    /users              # 获取用户列表
GET    /users/{id}         # 获取单个用户
POST   /users              # 创建用户
PUT    /users/{id}         # 全量更新用户
PATCH  /users/{id}         # 部分更新用户
DELETE /users/{id}         # 删除用户

GET    /users/{id}/orders  # 获取用户的订单
```

## 命名规范
- 使用名词复数，不用动词
- 使用小写字母和连字符：`/user-profiles`
- 嵌套不超过3层：`/users/{id}/orders/{orderId}`
- 查询参数用驼峰：`?pageSize=10&pageNum=1`

## 状态码使用
| 状态码 | 含义 | 场景 |
|--------|------|------|
| 200 | OK | 成功 |
| 201 | Created | 创建成功 |
| 204 | No Content | 删除成功 |
| 400 | Bad Request | 参数错误 |
| 401 | Unauthorized | 未认证 |
| 403 | Forbidden | 无权限 |
| 404 | Not Found | 资源不存在 |
| 409 | Conflict | 冲突（如重复创建） |
| 422 | Unprocessable Entity | 业务校验失败 |
| 500 | Internal Server Error | 服务端异常 |

## 响应格式
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "name": "John"
  }
}

// 分页响应
{
  "code": 200,
  "data": {
    "items": [],
    "total": 100,
    "pageNum": 1,
    "pageSize": 10
  }
}
```

## 最佳实践
1. 版本控制：`/api/v1/users`
2. 分页：`?pageNum=1&pageSize=10`
3. 排序：`?sort=createdAt,desc`
4. 过滤：`?status=active&role=admin`
5. 搜索：`?q=keyword`
6. 限流：返回 `X-RateLimit-*` 头"""
    },
    {
        "title": "消息队列核心概念",
        "content_type": "markdown",
        "category": "架构",
        "tags": ["mq", "kafka", "rabbitmq", "消息队列"],
        "content": """# 消息队列核心概念

## 使用场景
1. **异步处理**: 注册后发送邮件/短信
2. **流量削峰**: 秒杀场景缓冲请求
3. **应用解耦**: 订单系统与库存系统
4. **日志收集**: ELK 架构中的 Kafka

## RabbitMQ vs Kafka
| 特性 | RabbitMQ | Kafka |
|------|----------|-------|
| 模型 | 队列 | 发布订阅日志 |
| 吞吐量 | 万级 | 百万级 |
| 延迟 | 微秒级 | 毫秒级 |
| 消息确认 | 支持 | offset管理 |
| 顺序性 | 单队列保证 | 分区内保证 |
| 适用场景 | 业务消息 | 日志/大数据 |

## 消息可靠性保证
### RabbitMQ
1. 生产者确认 (Publisher Confirm)
2. 消息持久化 (durable=true)
3. 消费者手动确认 (manual ack)
4. 死信队列 (DLX)

### Kafka
1. acks=all（所有副本确认）
2. min.insync.replicas=2
3. 生产者重试 retries>0
4. 消费者手动提交 offset

## 消息幂等性
- 全局唯一 ID + 去重表
- 数据库唯一约束
- Redis SETNX 判重

## 延迟队列实现
- RabbitMQ: TTL + 死信队列 / 延迟插件
- Redis: ZSet + 时间戳作为 score
- RocketMQ: 原生支持延迟消息"""
    },
    # ==================== 系统设计 ====================
    {
        "title": "分布式系统核心问题",
        "content_type": "markdown",
        "category": "架构",
        "tags": ["分布式", "架构", "CAP", "一致性"],
        "content": """# 分布式系统核心问题

## CAP 定理
- **Consistency 一致性**: 所有节点数据一致
- **Availability 可用性**: 每个请求都能响应
- **Partition tolerance 分区容错**: 网络分区时系统仍能运行
- 三者最多取其二，分布式系统必须保证 P，通常在 CP 和 AP 之间选择

## BASE 理论 (对 CAP 的补充)
- **Basically Available**: 基本可用
- **Soft State**: 软状态，允许中间状态
- **Eventually Consistent**: 最终一致性

## 分布式 ID 生成方案
| 方案 | 优点 | 缺点 |
|------|------|------|
| UUID | 简单、无网络开销 | 无序、存储空间大 |
| 数据库自增 | 有序、简单 | 单点瓶颈 |
| Redis INCR | 高性能 | 依赖 Redis |
| 雪花算法 | 有序、高性能 | 时钟回拨问题 |

## 分布式锁方案
1. **数据库**: 乐观锁/悲观锁（性能差）
2. **Redis**: SETNX + Lua（推荐，需处理续期）
3. **Zookeeper**: 临时顺序节点（强一致，性能一般）
4. **Redlock**: Redis 多节点锁（有争议）

## 分布式事务方案
1. **2PC/3PC**: 强一致，性能差
2. **TCC**: Try-Confirm-Cancel，灵活但侵入性强
3. **Saga**: 长事务拆分，补偿机制
4. **本地消息表**: 最终一致性
5. **事务消息**: RocketMQ 支持

## 一致性哈希
- 解决节点增减时大量数据迁移问题
- 虚拟节点解决数据倾斜
- 应用于负载均衡、分布式缓存"""
    },
    {
        "title": "系统设计面试常见问题",
        "content_type": "markdown",
        "category": "架构",
        "tags": ["系统设计", "面试", "架构"],
        "content": """# 系统设计面试常见问题

## 设计思路框架
1. **需求澄清**: 功能需求 + 非功能需求（QPS、延迟、可用性）
2. **估算**: 存储量、带宽、QPS
3. **高层设计**: 核心组件 + 数据流
4. **详细设计**: 数据库设计、API 设计、关键算法
5. **扩展**: 瓶颈识别 + 优化方案

## 短链接系统
- 62进制编码（a-z, A-Z, 0-9），6位可表示 568亿种组合
- 哈希 + 冲突处理 或 自增ID + 进制转换
- 302 重定向（便于统计）
- 缓存热点短链 + 数据库持久化

## 秒杀系统
1. 前端：静态资源 CDN + 按钮防抖 + 验证码
2. 网关：限流（令牌桶）+ 黑名单
3. 服务：Redis 预扣库存 + 消息队列异步下单
4. 数据库：乐观锁扣减库存

## Feed 流系统
- **推模式**: 发布时写入粉丝收件箱，读取快但写入扩散
- **拉模式**: 读取时拉取关注人动态，写入快但读取慢
- **推拉结合**: 大V用拉模式，普通用户用推模式

## 限流算法
| 算法 | 特点 | 实现 |
|------|------|------|
| 计数器 | 简单但有临界问题 | AtomicInteger |
| 滑动窗口 | 平滑限流 | Redis + 时间片 |
| 漏桶 | 恒定速率 | Queue |
| 令牌桶 | 允许突发 | Guava RateLimiter"""

    },
    # ==================== Python ====================
    {
        "title": "Python 异步编程 (asyncio)",
        "content_type": "markdown",
        "category": "Python",
        "tags": ["python", "asyncio", "异步"],
        "content": """# Python 异步编程 (asyncio)

## 核心概念
```python
import asyncio

async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

# 运行协程
asyncio.run(fetch_data("http://example.com"))
```

## 并发执行
```python
async def main():
    # 并发执行多个协程
    results = await asyncio.gather(
        fetch_data("http://api1.com"),
        fetch_data("http://api2.com"),
        fetch_data("http://api3.com")
    )

    # 或使用 TaskGroup (Python 3.11+)
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_data("http://api1.com"))
        task2 = tg.create_task(fetch_data("http://api2.com"))
```

## 异步生成器与迭代
```python
async def async_range(n):
    for i in range(n):
        await asyncio.sleep(0.1)
        yield i

async def main():
    async for num in async_range(10):
        print(num)
```

## 异步上下文管理器
```python
class AsyncDB:
    async def __aenter__(self):
        self.conn = await create_connection()
        return self.conn

    async def __aexit__(self, exc_type, exc, tb):
        await self.conn.close()

async def main():
    async with AsyncDB() as conn:
        await conn.execute("SELECT 1")
```

## FastAPI 中的异步
```python
@app.get("/items/{item_id}")
async def read_item(item_id: int):
    # 数据库查询使用 async session
    async with AsyncSession(engine) as session:
        result = await session.execute(
            select(Item).where(Item.id == item_id)
        )
        return result.scalar_one_or_none()
```

## 注意事项
1. 不要在异步代码中使用 time.sleep()，用 asyncio.sleep()
2. 不要在异步代码中调用同步阻塞 IO
3. CPU 密集型任务用 ProcessPoolExecutor
4. IO 密集型任务用 asyncio 或 ThreadPoolExecutor"""
    },
    # ==================== 面试相关 ====================
    {
        "title": "Java 面试八股文精选",
        "content_type": "markdown",
        "category": "面试",
        "tags": ["java", "面试", "八股文"],
        "content": """# Java 面试八股文精选

## == 和 equals() 区别
- `==` 比较基本类型的值，比较引用类型的地址
- `equals()` 默认等同于 ==，String/Integer 等重写为值比较
- 重写 equals() 必须同时重写 hashCode()

## String、StringBuilder、StringBuffer
| 类型 | 可变性 | 线程安全 | 性能 |
|------|--------|----------|------|
| String | 不可变 | 是 | 拼接慢 |
| StringBuilder | 可变 | 否 | 拼接快 |
| StringBuffer | 可变 | 是 | 拼接较快 |

## 为什么重写 equals 必须重写 hashCode
- HashMap 先用 hashCode 定位桶，再用 equals 比较
- equals 相等的对象 hashCode 必须相等
- hashCode 相等的对象 equals 不一定相等

## 接口和抽象类区别
| 特性 | 接口 | 抽象类 |
|------|------|--------|
| 多继承 | 支持多实现 | 单继承 |
| 构造器 | 无 | 有 |
| 成员变量 | 只能 public static final | 任意 |
| 方法 | Java 8+ 可有默认实现 | 可有实现 |
| 设计意图 | 能力(has-a) | 是(is-a) |

## Java 8 新特性
1. Lambda 表达式
2. 函数式接口 (@FunctionalInterface)
3. Stream API (流式操作集合)
4. Optional (防空指针)
5. 新日期 API (LocalDate/LocalDateTime)
6. 接口默认方法 (default)

## 深拷贝 vs 浅拷贝
- 浅拷贝：复制对象本身，引用类型字段仍指向原对象
- 深拷贝：递归复制所有引用对象
- 实现方式：实现 Cloneable / 序列化 / 手动复制

## 强引用、软引用、弱引用、虚引用
| 类型 | GC 时机 | 用途 |
|------|---------|------|
| 强引用 | 不回收 | 普通引用 |
| 软引用 | 内存不足时回收 | 缓存 |
| 弱引用 | 下次 GC 回收 | WeakHashMap |
| 虚引用 | 随时回收 | 跟踪回收状态"""
    },
    {
        "title": "Spring 常见面试题",
        "content_type": "markdown",
        "category": "面试",
        "tags": ["spring", "面试", "ioc", "aop"],
        "content": """# Spring 常见面试题

## IoC 和 DI
- **IoC (控制反转)**: 对象的创建和管理权从程序转移给容器
- **DI (依赖注入)**: IoC 的实现方式，容器自动注入依赖
- 注入方式：构造器注入（推荐）、Setter 注入、字段注入

## Bean 生命周期
1. 实例化 → 2. 属性赋值 → 3. Aware 接口回调
4. BeanPostProcessor.postProcessBeforeInitialization
5. InitializingBean.afterPropertiesSet / @PostConstruct
6. BeanPostProcessor.postProcessAfterInitialization
7. 使用 → 8. DisposableBean.destroy / @PreDestroy

## Bean 作用域
| 作用域 | 描述 |
|--------|------|
| singleton | 默认，容器内唯一实例 |
| prototype | 每次请求新实例 |
| request | 每个 HTTP 请求一个实例 |
| session | 每个 HTTP Session 一个实例 |

## AOP 核心概念
- **切面 (Aspect)**: 横切关注点的模块化
- **连接点 (JoinPoint)**: 程序执行的某个位置
- **切入点 (Pointcut)**: 匹配连接点的表达式
- **通知 (Advice)**: 切面在特定切入点执行的动作
  - @Before: 前置通知
  - @After: 后置通知
  - @AfterReturning: 返回通知
  - @AfterThrowing: 异常通知
  - @Around: 环绕通知（最强）

## @Transactional 事务失效场景
1. 方法非 public
2. 同类方法内部调用（未经代理）
3. 异常被 catch 未抛出
4. 抛出非 RuntimeException（默认只回滚 RuntimeException）
5. 数据库引擎不支持（如 MyISAM）

## Spring 循环依赖解决
- 三级缓存：
  1. singletonObjects: 完整 Bean
  2. earlySingletonObjects: 提前暴露的 Bean（半成品）
  3. singletonFactories: Bean 工厂
- 只能解决单例 + setter/字段注入的循环依赖
- 构造器注入的循环依赖无法解决"""
    },
]


def seed():
    db = SessionLocal()
    try:
        existing = knowledge_service.list(db, limit=1)
        if existing:
            return

        created = knowledge_service.import_batch(db, KNOWLEDGE_ITEMS)
        categories = {}
        for item in created:
            cat = item.category or "未分类"
            categories[cat] = categories.get(cat, 0) + 1
        summary = ", ".join(f"{cat}({cnt})" for cat, cnt in sorted(categories.items()))
        print(f"已导入 {len(created)} 条: {summary}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
