/* ========================================
   Elysia 升学攻略 - Service Worker
   功能：通知点击处理 + 核心资源预缓存
   版本：v1.4.0 (2026-08-22, 雅思小分诊断+细化计划)
   ======================================== */

const CACHE_NAME = 'elysia-cache-v7';
const CORE_ASSETS = [
    './',
    './index.html',
    './style.css',
    './data.js',
    './reminders.js',
    './manifest.json',
    './icons/icon-512.png',
    './qrcode.png'
];

// ==================== 安装：预缓存核心资源 ====================
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => cache.addAll(CORE_ASSETS))
            .then(() => self.skipWaiting())
    );
});

// ==================== 激活：清理旧缓存 ====================
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((keys) =>
            Promise.all(
                keys.filter((key) => key !== CACHE_NAME)
                    .map((key) => caches.delete(key))
            )
        ).then(() => self.clients.claim())
    );
});

// ==================== 通知点击：跳转到时间线页面 ====================
self.addEventListener('notificationclick', (event) => {
    event.notification.close();

    // 通知中携带的数据（在通知选项中设置 data.url）
    const targetUrl = (event.notification.data && event.notification.data.url) || './index.html#timeline';

    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true })
            .then((clientList) => {
                // 优先聚焦已打开的页面
                for (const client of clientList) {
                    if ('focus' in client) {
                        // 跳转到目标 hash
                        client.navigate(targetUrl).catch(() => {});
                        return client.focus();
                    }
                }
                // 没有已打开的窗口，则打开新窗口
                return clients.openWindow(targetUrl);
            })
    );
});

// ==================== 通知关闭 ====================
self.addEventListener('notificationclose', () => {
    // 预留：可在此埋点统计通知关闭率
});

// ==================== Fetch：网络优先 + 缓存兜底 ====================
self.addEventListener('fetch', (event) => {
    // 只处理同源 GET 请求
    if (event.request.method !== 'GET') return;
    const url = new URL(event.request.url);
    if (url.origin !== self.location.origin) return;

    event.respondWith(
        fetch(event.request)
            .then((response) => {
                // 网络成功，更新缓存（仅缓存核心静态资源）
                if (event.request.mode === 'navigate' ||
                    CORE_ASSETS.includes(url.pathname.replace(/^.*webapp/, './'))) {
                    const copy = response.clone();
                    caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
                }
                return response;
            })
            .catch(() => {
                // 离线时回退缓存
                return caches.match(event.request).then((cached) => {
                    if (cached) return cached;
                    if (event.request.mode === 'navigate') return caches.match('./index.html');
                    return new Response('', { status: 504, statusText: 'Offline' });
                });
            })
    );
});
