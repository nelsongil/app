// Nombre de la caché
var cacheName = 'mcontrol-horario';

// Lista de recursos a ser almacenados en caché
var resourcesToCache = [
  '/',
  '/static/css/styles.css',
  '/static/img/logo.png'
];

// Evento de instalación del Service Worker
self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open(cacheName).then(function(cache) {
      return cache.addAll(resourcesToCache);
    })
  );
});

// Evento de recuperación de recursos del caché
self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request).then(function(response) {
      return response || fetch(event.request);
    })
  );
});