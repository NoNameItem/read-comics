# Changelog

## [1.23.5](https://github.com/NoNameItem/read-comics/compare/1.23.4...1.23.5) (2025-03-14)


### Bug Fixes

* **core:** Freeze kombu version on 5.4.2 ([69623c9](https://github.com/NoNameItem/read-comics/commit/69623c9427b7f272fd20742ce3ab3a54547a6a42))
* **missing-issues:** Retry missing issues tasks on WorkerLostError ([dbfb678](https://github.com/NoNameItem/read-comics/commit/dbfb678f90a073151e9ea77c43c59260ac5abbc8))

## [1.23.4](https://github.com/NoNameItem/read-comics/compare/1.23.3...1.23.4) (2025-03-14)


### Bug Fixes

* **missing-issues:** Fixed 1.23.3 ([20964ec](https://github.com/NoNameItem/read-comics/commit/20964ecebda2f15e6246ac00073e1291439f3e5f))

## [1.23.3](https://github.com/NoNameItem/read-comics/compare/1.23.2...1.23.3) (2025-03-14)


### Bug Fixes

* **missing-issues:** Retry missing issues tasks on WorkerLostError ([c815652](https://github.com/NoNameItem/read-comics/commit/c815652aeecd22e4d96c110bc95643b8421ab7b1))

## [1.23.2](https://github.com/NoNameItem/read-comics/compare/1.23.1...1.23.2) (2025-03-07)


### Bug Fixes

* **core:** Management command clearqueue ([ce64d6b](https://github.com/NoNameItem/read-comics/commit/ce64d6b2038b80399221642b553e2d6c85dc22ee))

## [1.23.1](https://github.com/NoNameItem/read-comics/compare/1.23.0...1.23.1) (2025-03-07)


### Bug Fixes

* **core:** MultipleObjectsReturned in fill_from_comicvine ([66f7a99](https://github.com/NoNameItem/read-comics/commit/66f7a991422b783581c73beb07b82c498f99ff77))

## [1.23.0](https://github.com/NoNameItem/read-comics/compare/1.22.3...1.23.0) (2025-03-06)


### Features

* **core:** Clear selected queues on celery launch ([8a852c7](https://github.com/NoNameItem/read-comics/commit/8a852c79a31d0c8f84c15a64a00bff87359f6f05))

## [1.22.3](https://github.com/NoNameItem/read-comics/compare/1.22.2...1.22.3) (2025-03-06)


### Bug Fixes

* **core:** Set comicvine_status = NOT_MATCHED on BaseComicvineInfoTask retry ([3a952e5](https://github.com/NoNameItem/read-comics/commit/3a952e5692c70581120feec0976fd20188d13493))

## [1.22.2](https://github.com/NoNameItem/read-comics/compare/1.22.1...1.22.2) (2025-03-04)


### Bug Fixes

* **core:** Purge offline workers from flower ([c0cf6e9](https://github.com/NoNameItem/read-comics/commit/c0cf6e98a51e83ac000463413153a2d6563aae37))

## [1.22.1](https://github.com/NoNameItem/read-comics/compare/1.22.0...1.22.1) (2025-03-04)


### Bug Fixes

* **core:** Purge offline workers from flower ([8842c46](https://github.com/NoNameItem/read-comics/commit/8842c46f7dff8a0e165dbd9e1f2d813e7d54c5d7))

## [1.22.0](https://github.com/NoNameItem/read-comics/compare/1.21.1...1.22.0) (2025-03-03)


### Features

* **core:** Celeryworker -n option parametrized ([944eff5](https://github.com/NoNameItem/read-comics/commit/944eff503c360765b7a1e0e2f4dec40db7bfa359))

## [1.21.1](https://github.com/NoNameItem/read-comics/compare/1.21.0...1.21.1) (2025-03-02)


### Bug Fixes

* **core:** Celeryworker --autoscale option parametrized ([b2b1cbf](https://github.com/NoNameItem/read-comics/commit/b2b1cbf97311a979701b844448f2c76492f64f04))

## [1.21.0](https://github.com/NoNameItem/read-comics/compare/1.20.9...1.21.0) (2025-03-02)


### Features

* **core:** Celeryworker --autoscale option parametrized ([d9b0da9](https://github.com/NoNameItem/read-comics/commit/d9b0da9ecf7e21534bee858f5913facad08ba5bd))
* **core:** Celeryworker -Q option parametrized ([4b5fa4f](https://github.com/NoNameItem/read-comics/commit/4b5fa4f83506849a197d0683275b87ddfc4700b0))
* **core:** Task routing ([29ac3d6](https://github.com/NoNameItem/read-comics/commit/29ac3d61ba2677af3596f25ebbbf5cf7fdbe48e1))


### Build System

* Clear API queue on celery launch ([b4e6d28](https://github.com/NoNameItem/read-comics/commit/b4e6d2828e967982b35d69b7cf31ef51bdf24ce9))

## [1.20.9](https://github.com/NoNameItem/read-comics/compare/1.20.8...1.20.9) (2025-02-28)


### Bug Fixes

* **core:** Additional logging in tasks ([91aef77](https://github.com/NoNameItem/read-comics/commit/91aef773010ba49de5657ca691f71f8994a7ee41))
* **core:** Log levels ([135a117](https://github.com/NoNameItem/read-comics/commit/135a1171a217e576f2e63a39fbb74467f6327d5e))

## [1.20.8](https://github.com/NoNameItem/read-comics/compare/1.20.7...1.20.8) (2025-02-27)


### Bug Fixes

* **core:** Logging ([6f0789d](https://github.com/NoNameItem/read-comics/commit/6f0789d421e5af231a0ff97ea698a76467a054f7))

## [1.20.7](https://github.com/NoNameItem/read-comics/compare/1.20.6...1.20.7) (2025-02-27)


### Bug Fixes

* **core:** Race condition in getting info from comicvine API ([a0c5603](https://github.com/NoNameItem/read-comics/commit/a0c5603fd0a17484d539188a2984d82e3a361446))

## [1.20.6](https://github.com/NoNameItem/read-comics/compare/1.20.5...1.20.6) (2025-02-27)


### Bug Fixes

* **core:** Race condition in getting info from comicvine API ([d539bd2](https://github.com/NoNameItem/read-comics/commit/d539bd2b93997dc06e261af48a949b4c92c4aacd))

## [1.20.5](https://github.com/NoNameItem/read-comics/compare/1.20.4...1.20.5) (2025-02-27)


### Bug Fixes

* Wrong attribute in celery run command ([c476c2f](https://github.com/NoNameItem/read-comics/commit/c476c2fe789b5712f7e759a700e0ca8db2e108a4))

## [1.20.4](https://github.com/NoNameItem/read-comics/compare/1.20.3...1.20.4) (2025-02-27)


### Performance Improvements

* **core:** Changed queue algorithm for fetching info from comicvine API ([9522d39](https://github.com/NoNameItem/read-comics/commit/9522d397a5f4ecd75d77c917a62b98837c2e1202))

## [1.20.3](https://github.com/NoNameItem/read-comics/compare/1.20.2...1.20.3) (2025-02-27)


### Bug Fixes

* **core:** Ignore comicvine_actual when force_api_refresh is true ([8128d62](https://github.com/NoNameItem/read-comics/commit/8128d620695c39468b6a34f7b6128e9767d83d1b))
* **core:** Log in comicvine_actual ([efcb163](https://github.com/NoNameItem/read-comics/commit/efcb163dc8d2feb9841905751ddef076f5a597a9))

## [1.20.2](https://github.com/NoNameItem/read-comics/compare/1.20.1...1.20.2) (2025-02-27)


### Bug Fixes

* **core:** Separate log for forced API refresh ([eb82256](https://github.com/NoNameItem/read-comics/commit/eb8225644f37baaedc34c231e29a4ad6b1d3008b))

## [1.20.1](https://github.com/NoNameItem/read-comics/compare/1.20.0...1.20.1) (2025-02-26)


### Bug Fixes

* Missing migrations ([be03740](https://github.com/NoNameItem/read-comics/commit/be037404d7208a23a68a8c35765cc218c740958e))

## [1.20.0](https://github.com/NoNameItem/read-comics/compare/1.19.2...1.20.0) (2025-02-26)


### Features

* **core:** Allow to pass all kwargs in delayed fill_from_comicvine ([4c052a5](https://github.com/NoNameItem/read-comics/commit/4c052a58fafb69e52451594d87e01f3212211108))
* **issues:** Display variant covers ([707e1d0](https://github.com/NoNameItem/read-comics/commit/707e1d0a2184244fda5b7b588eb1d4342a3a337b))
* **issues:** Save associated_images in issue fetch from comicvine API ([1843a83](https://github.com/NoNameItem/read-comics/commit/1843a831b22c0d12120addde1a57d8eb641e7e1b))
* **spiders:** Save associated_images for issues ([0f6b90a](https://github.com/NoNameItem/read-comics/commit/0f6b90a3a261a014ae3c17707603c549674cc7fb))

## [1.19.2](https://github.com/NoNameItem/read-comics/compare/1.19.1...1.19.2) (2025-02-24)


### Bug Fixes

* **core:** Media files ([5820a5e](https://github.com/NoNameItem/read-comics/commit/5820a5ec82125f42887496f6cc9340acc691c703))

## [1.19.1](https://github.com/NoNameItem/read-comics/compare/1.19.0...1.19.1) (2025-02-24)


### Bug Fixes

* **issues:** Fixed download ([6dc7291](https://github.com/NoNameItem/read-comics/commit/6dc7291eb9bc540f284dec6909e6929dd619d12c))

## [1.19.0](https://github.com/NoNameItem/read-comics/compare/1.18.5...1.19.0) (2025-02-21)


### Features

* **core:** Missing issues metrics ([5f77f96](https://github.com/NoNameItem/read-comics/commit/5f77f96fa762b9730c8635a328b93f531aaa2e80))

## [1.18.5](https://github.com/NoNameItem/read-comics/compare/1.18.4...1.18.5) (2025-02-18)


### Bug Fixes

* **core:** Celery task_acks_late = True ([359af80](https://github.com/NoNameItem/read-comics/commit/359af80952b3c4fd655b13bbf3d1b7551d5bc323))
* **core:** Use app timezone in celery ([a0bd861](https://github.com/NoNameItem/read-comics/commit/a0bd8610ee16774e2baf71c4d8273c68f1ac3836))

## [1.18.4](https://github.com/NoNameItem/read-comics/compare/1.18.3...1.18.4) (2025-02-15)


### Bug Fixes

* **core:** Close mongo connections ([084032a](https://github.com/NoNameItem/read-comics/commit/084032a4696ac11415a5402cfceb240a3b249a4d))
* **spiders:** Adjust list/detail priority ([f18ec5f](https://github.com/NoNameItem/read-comics/commit/f18ec5fef849765b7ec98f815902665b6478728b))
* **spiders:** Adjust list/detail priority in full_spider ([f18ec5f](https://github.com/NoNameItem/read-comics/commit/f18ec5fef849765b7ec98f815902665b6478728b))
* **spiders:** Disable depth priority adjustment ([f18ec5f](https://github.com/NoNameItem/read-comics/commit/f18ec5fef849765b7ec98f815902665b6478728b))

## [1.18.3](https://github.com/NoNameItem/read-comics/compare/1.18.2...1.18.3) (2025-02-12)


### Performance Improvements

* **core:** Optimize db metrics collection ([6925d1d](https://github.com/NoNameItem/read-comics/commit/6925d1d7fb51716bf2fa241f76d321ba4c873ee0))
* **core:** Optimize mongo metrics collection ([b31c238](https://github.com/NoNameItem/read-comics/commit/b31c238ea6938ba8b185df706954d9fa68590aac))

## [1.18.2](https://github.com/NoNameItem/read-comics/compare/1.18.1...1.18.2) (2025-02-07)


### Bug Fixes

* **core:** Consolidate all db metrics ([8b898fb](https://github.com/NoNameItem/read-comics/commit/8b898fb5337706474a7692f9ebdd8a90d9500968))

## [1.18.1](https://github.com/NoNameItem/read-comics/compare/1.18.0...1.18.1) (2025-02-07)


### Bug Fixes

* **core:** Consolidate all mongo metrics ([ad80e54](https://github.com/NoNameItem/read-comics/commit/ad80e548b3318776cf56ec4487b8f10e88718b8b))

## [1.18.0](https://github.com/NoNameItem/read-comics/compare/1.17.4...1.18.0) (2025-02-07)


### Features

* **core:** /metrics endpoint with mongo and db statistics ([d6da536](https://github.com/NoNameItem/read-comics/commit/d6da536ab570bcea9e79cb8deac765e0d91e4384))

## [1.17.4](https://github.com/NoNameItem/read-comics/compare/1.17.3...1.17.4) (2025-02-05)


### Bug Fixes

* **spiders:** Crawl in FIFO order ([30e7c22](https://github.com/NoNameItem/read-comics/commit/30e7c22213dc13f3a370cdfdebc7a8bdc9ba6067))

## [1.17.3](https://github.com/NoNameItem/read-comics/compare/1.17.2...1.17.3) (2025-02-04)


### Bug Fixes

* **spiders:** Update info from list only if there is no info from detail ([fca7983](https://github.com/NoNameItem/read-comics/commit/fca79830546900b0c7287ff862f3d1322c9f60e8))

## [1.17.2](https://github.com/NoNameItem/read-comics/compare/1.17.1...1.17.2) (2025-02-04)


### Bug Fixes

* **spiders:** Fix scrapyscript ([9b2707f](https://github.com/NoNameItem/read-comics/commit/9b2707f84d530cd4576f55d5c372128460998268))

## [1.17.1](https://github.com/NoNameItem/read-comics/compare/1.17.0...1.17.1) (2025-02-03)


### Bug Fixes

* **core:** Changed total stats endpoint query params to match grafana syntax ([0850b11](https://github.com/NoNameItem/read-comics/commit/0850b116d2600172bdf3e03a8edb64c0a8f81358))

## [1.17.0](https://github.com/NoNameItem/read-comics/compare/1.16.0...1.17.0) (2025-02-03)


### Features

* **core:** Total statistics endpoint ([f945661](https://github.com/NoNameItem/read-comics/commit/f94566102f849fb7299a104a7256059fd1c382a0))

## [1.16.0](https://github.com/NoNameItem/read-comics/compare/1.15.0...1.16.0) (2025-02-03)


### Features

* **characters:** Statistics API endpoint ([3294f75](https://github.com/NoNameItem/read-comics/commit/3294f75c6012ccc78ec12e18b8751baaa371a3e0))
* **concepts:** Statistics API endpoint ([79a9400](https://github.com/NoNameItem/read-comics/commit/79a94005e59092593d6d948b414b19624605bcc3))
* **issues:** Statistics API endpoint ([313cd17](https://github.com/NoNameItem/read-comics/commit/313cd1795b8ab986c279bb45388267b8f7d19191))
* **locations:** Statistics API endpoint ([0485d5c](https://github.com/NoNameItem/read-comics/commit/0485d5cd40a719ba74a354a2cb411400d70f1ba5))
* **objects:** Statistics API endpoint ([27b9acd](https://github.com/NoNameItem/read-comics/commit/27b9acd28b72719b539c4362719825edf46013b4))
* **people:** Statistics API endpoint ([d87b2e8](https://github.com/NoNameItem/read-comics/commit/d87b2e8e535b1af43b4ab92f39ee834e36f2d082))
* **powers:** Statistics API endpoint ([36baa67](https://github.com/NoNameItem/read-comics/commit/36baa67b5339f541f5317e6e6bc24998b51afb44))
* **publishers:** Statistics API endpoint ([9e0c618](https://github.com/NoNameItem/read-comics/commit/9e0c618bc5fb95d2281f1ef818895972b8970f57))
* **story-arcs:** Statistics API endpoint ([d8ea8df](https://github.com/NoNameItem/read-comics/commit/d8ea8df724586af699c8a08fe979acc6487fb9bf))
* **teams:** Statistics API endpoint ([48ce8bd](https://github.com/NoNameItem/read-comics/commit/48ce8bd7ea038653713860b816c31cd386d99858))
* **volumes:** Statistics API endpoint ([d765ce6](https://github.com/NoNameItem/read-comics/commit/d765ce603ec373a34f5b7f7ce5a411b95b2810af))

## [1.15.0](https://github.com/NoNameItem/read-comics/compare/1.14.6...1.15.0) (2025-02-01)


### Features

* Prometheus integration ([12b3874](https://github.com/NoNameItem/read-comics/commit/12b3874307c3e843b54ac00c14d1906e6828c270))


### Build System

* Update github actions ([1ea4ba5](https://github.com/NoNameItem/read-comics/commit/1ea4ba570d6511e6961c97ae288c5fdd279eaa76))
* Update github actions ([f002f8b](https://github.com/NoNameItem/read-comics/commit/f002f8b22219784839e05d9226cd3f222be615d4))

## [1.14.6](https://github.com/NoNameItem/read-comics/compare/1.14.5...1.14.6) (2025-01-31)


### Bug Fixes

* Allways use timezone.now() ([3545aad](https://github.com/NoNameItem/read-comics/commit/3545aadb3aa19c9d01af0f223bc865dbe985d592))

## [1.14.5](https://github.com/NoNameItem/read-comics/compare/1.14.4...1.14.5) (2025-01-31)


### Build System

* Update django-celery-deat ([8eb2c35](https://github.com/NoNameItem/read-comics/commit/8eb2c35d93d4031e72191b6a147367cb7e13ccff))

## [1.14.4](https://github.com/NoNameItem/read-comics/compare/1.14.3...1.14.4) (2025-01-30)


### Bug Fixes

* **core:** Get timezone from TZ environment variable ([2dee737](https://github.com/NoNameItem/read-comics/commit/2dee737b665892a81c9fde98071235703ed70e6b))

## [1.14.3](https://github.com/NoNameItem/read-comics/compare/1.14.2...1.14.3) (2025-01-30)


### Bug Fixes

* **core:** Get timezone from TZ environment variable ([e8855d1](https://github.com/NoNameItem/read-comics/commit/e8855d1767057c7d5c373bc77fa61ad23d77a208))

## [1.14.2](https://github.com/NoNameItem/read-comics/compare/1.14.1...1.14.2) (2025-01-30)


### Bug Fixes

* **core:** Update celery and flower ([fe113e2](https://github.com/NoNameItem/read-comics/commit/fe113e2bcdee7095287430c2656cdd8096ee5c4c))
* **core:** Update celery and flower ([18c0000](https://github.com/NoNameItem/read-comics/commit/18c0000b66a4f085c7c524f55d20a6a55abccd15))

## [1.14.1](https://github.com/NoNameItem/read-comics/compare/1.14.0...1.14.1) (2025-01-30)


### Bug Fixes

* **core:** Update celery and flower ([c69b61c](https://github.com/NoNameItem/read-comics/commit/c69b61cf14002e6c2a57443d2219f53b137f4e48))
* **core:** Update celery and flower ([5441d4e](https://github.com/NoNameItem/read-comics/commit/5441d4efd67e319d2044cbea6c13101007f22775))
* **core:** Update celery and flower ([473b1f7](https://github.com/NoNameItem/read-comics/commit/473b1f702f1399302a8a4e04aeae1b015ed253f9))

## [1.14.0](https://github.com/NoNameItem/read-comics/compare/1.13.2...1.14.0) (2025-01-30)


### Features

* **core:** Monitor rabbitmq queue from flower ([c4198e4](https://github.com/NoNameItem/read-comics/commit/c4198e43a4b1a60e88c7b038f1edea78814722d1))

## [1.13.2](https://github.com/NoNameItem/read-comics/compare/1.13.1...1.13.2) (2025-01-30)


### Bug Fixes

* **core:** Celery settings ([c459738](https://github.com/NoNameItem/read-comics/commit/c4597388d54b3c3698c32495b944a1430f59918f))

## [1.13.1](https://github.com/NoNameItem/read-comics/compare/1.13.0...1.13.1) (2025-01-30)


### Bug Fixes

* **core:** Fixed priorities ([3db95b8](https://github.com/NoNameItem/read-comics/commit/3db95b857d10254e30b58c4c7869a31915f75013))

## [1.13.0](https://github.com/NoNameItem/read-comics/compare/1.12.5...1.13.0) (2025-01-30)


### Features

* **missing-issues:** Management command for clearing api queue ([4eae7a9](https://github.com/NoNameItem/read-comics/commit/4eae7a94e949c5b627247e43887f0779fe348c4a))


### Build System

* Switch celery to rabbitmq and mongo ([1b32e50](https://github.com/NoNameItem/read-comics/commit/1b32e50692343e8041488158830df325741569f4))

## [1.12.5](https://github.com/NoNameItem/read-comics/compare/1.12.4...1.12.5) (2025-01-28)


### Bug Fixes

* **core:** Increased max retries in getting info from API ([18ca001](https://github.com/NoNameItem/read-comics/commit/18ca00168410016e8309e12a5a61357b2fa91ba9))
* **spiders:** Do not adjust priority on retries ([12e2373](https://github.com/NoNameItem/read-comics/commit/12e23735fc0878852b08dadfe090f7f9e90b2b04))

## [1.12.4](https://github.com/NoNameItem/read-comics/compare/1.12.3...1.12.4) (2025-01-27)


### Bug Fixes

* **core:** Changed order of queue wait and api wait ([3dd3801](https://github.com/NoNameItem/read-comics/commit/3dd3801c30136ece9ee102a845598655c0099399))

## [1.12.3](https://github.com/NoNameItem/read-comics/compare/1.12.2...1.12.3) (2025-01-27)


### Bug Fixes

* **core:** Added longer timeout while waiting for queue ([cc60680](https://github.com/NoNameItem/read-comics/commit/cc6068010ce63060fcc3e38cbe672df7ea0945ad))
* **core:** Changed order of queue wait and api wait ([486b704](https://github.com/NoNameItem/read-comics/commit/486b70404a5697efa76c889eea3130e2b1c8fec1))

## [1.12.2](https://github.com/NoNameItem/read-comics/compare/1.12.1...1.12.2) (2025-01-27)


### Bug Fixes

* **core:** Changed datatype for APIQueue.comicvine_id ([3f82002](https://github.com/NoNameItem/read-comics/commit/3f8200244dce54f37bde87ea1dd6528f358adfc3))

## [1.12.1](https://github.com/NoNameItem/read-comics/compare/1.12.0...1.12.1) (2025-01-27)


### Bug Fixes

* **core:** Added missing migrations ([0e4af06](https://github.com/NoNameItem/read-comics/commit/0e4af06da4b2e2c607969e30bad1c55133b91049))

## [1.12.0](https://github.com/NoNameItem/read-comics/compare/1.11.1...1.12.0) (2025-01-27)


### Features

* **core:** Queue for collecting info from api ([eb76f8b](https://github.com/NoNameItem/read-comics/commit/eb76f8b0d84eb04c1bd84daaa4c15495b1cd4a99))


### Bug Fixes

* **core:** Changed sleep timeout between API retries in adding info ([3a8fbc2](https://github.com/NoNameItem/read-comics/commit/3a8fbc2d83d67b8c00c1e961f821bfb67ec53833))
* **spiders:** Decrease delay between 420/429 retries to 10 minutes ([9e7ee50](https://github.com/NoNameItem/read-comics/commit/9e7ee5079e60e77403d46a51d43b5429b969fdf2))

## [1.11.1](https://github.com/NoNameItem/read-comics/compare/1.11.0...1.11.1) (2025-01-27)


### Bug Fixes

* **core:** Spaces in waiting for api logs ([6f0cee0](https://github.com/NoNameItem/read-comics/commit/6f0cee0df0d8c34dcf2327e1aac406f245f0ae08))

## [1.11.0](https://github.com/NoNameItem/read-comics/compare/1.10.11...1.11.0) (2025-01-27)


### Features

* **core:** Added try count in getting info from API logs ([dc9b0ff](https://github.com/NoNameItem/read-comics/commit/dc9b0ffa54640047a361caa8fdbc1e111cd413c7))
* **core:** Added waiting time in getting info from API logs ([3240ee9](https://github.com/NoNameItem/read-comics/commit/3240ee9168bc7954a0cfbe9276015245455b686d))

## [1.10.11](https://github.com/NoNameItem/read-comics/compare/1.10.10...1.10.11) (2025-01-26)


### Bug Fixes

* **core:** Changed sleep timeout between API retries in adding info ([8467c9d](https://github.com/NoNameItem/read-comics/commit/8467c9daee8f238c2079f52108401e0585a01e07))
* **core:** Changed waiting for API logs format ([10b67bd](https://github.com/NoNameItem/read-comics/commit/10b67bd6b6f924dc40a50b8c118c86567461f9be))
* **core:** Fixed IntegriryError on slug conflicts ([44a63f8](https://github.com/NoNameItem/read-comics/commit/44a63f8fd7ed1ee7786be883d29aaadcf1ef38b2))

## [1.10.10](https://github.com/NoNameItem/read-comics/compare/1.10.9...1.10.10) (2025-01-26)


### Bug Fixes

* **core:** Fixed AttributeError while getting crawl_source when no document found in collection ([5228e64](https://github.com/NoNameItem/read-comics/commit/5228e64f596c34821eb5fd0d3782dda122f6b784))

## [1.10.9](https://github.com/NoNameItem/read-comics/compare/1.10.8...1.10.9) (2025-01-26)


### Bug Fixes

* **core:** Request detail info only for issues, story arcs, volumes and publishers ([46651d9](https://github.com/NoNameItem/read-comics/commit/46651d9350776a022983313dd8d9235e66fe6708))

## [1.10.8](https://github.com/NoNameItem/read-comics/compare/1.10.7...1.10.8) (2025-01-25)


### Bug Fixes

* **spiders:** Retry delay middleware ([fc31766](https://github.com/NoNameItem/read-comics/commit/fc317669a92cff5491c9c56564b1fb61237abb23))

## [1.10.7](https://github.com/NoNameItem/read-comics/compare/1.10.6...1.10.7) (2025-01-25)


### Bug Fixes

* **core:** Changed logging format ([3e3b15d](https://github.com/NoNameItem/read-comics/commit/3e3b15d3a962ea3fda2dd15e04d57e2bdfe16035))
* **core:** Changed sleep timeout between API retries in adding info ([50fd15c](https://github.com/NoNameItem/read-comics/commit/50fd15c31e8895a0e3c3f1e905e26710fa17b87b))
* **spiders:** Retry delay middleware ([5635d5c](https://github.com/NoNameItem/read-comics/commit/5635d5c382d98dbb3e2446573548ac9aa90cccdf))

## [1.10.6](https://github.com/NoNameItem/read-comics/compare/1.10.5...1.10.6) (2025-01-25)


### Bug Fixes

* **core:** Separate locks for comicvine api endpoints ([41a6e5c](https://github.com/NoNameItem/read-comics/commit/41a6e5c5e38c79dcd8db743a635c2d41beeabeb5))

## [1.10.5](https://github.com/NoNameItem/read-comics/compare/1.10.4...1.10.5) (2025-01-18)


### Bug Fixes

* **core:** Decreased offset ([82513fe](https://github.com/NoNameItem/read-comics/commit/82513fe941bdc0a09f6fb20459c6ef8a9073a950))

## [1.10.4](https://github.com/NoNameItem/read-comics/compare/1.10.3...1.10.4) (2025-01-18)


### Bug Fixes

* **core:** Add 1 hour pause after failed spider request ([ba0f82e](https://github.com/NoNameItem/read-comics/commit/ba0f82edec4eb179627db2ee7d341e3b62a795d6))

## [1.10.3](https://github.com/NoNameItem/read-comics/compare/1.10.2...1.10.3) (2025-01-18)


### Bug Fixes

* **core:** Add 1 hour pause after failed spider request ([c1dc71e](https://github.com/NoNameItem/read-comics/commit/c1dc71edfdb9f7f3f4eb987bb41ea78fae063364))
* **core:** Extend backoff in getting document from api ([3f20e31](https://github.com/NoNameItem/read-comics/commit/3f20e31a45e82f02946f0227b483fc0b25a4f4a9))

## [1.10.2](https://github.com/NoNameItem/read-comics/compare/1.10.1...1.10.2) (2025-01-17)


### Bug Fixes

* **core:** Changed delay between api calls tries to half-delay to delay ([f822a10](https://github.com/NoNameItem/read-comics/commit/f822a10a0a4bfff4349528a30d10b834ed390017))
* **core:** If comicvine data comes from list, refetch from detail api when creating instance ([b802435](https://github.com/NoNameItem/read-comics/commit/b802435360a24c951b4292ddf60b91d1b6726184))

## [1.10.1](https://github.com/NoNameItem/read-comics/compare/1.10.0...1.10.1) (2025-01-17)


### Bug Fixes

* **core:** Added delay when fetching info from comicvine API ([302da0b](https://github.com/NoNameItem/read-comics/commit/302da0ba4339cdb781330375e79d5cf270a89a3c))

## [1.10.0](https://github.com/NoNameItem/read-comics/compare/1.9.1...1.10.0) (2025-01-17)


### Features

* **core:** Added delay when fetching info from comicvine API ([c0115d9](https://github.com/NoNameItem/read-comics/commit/c0115d93f7af46e5c188059e0d22029745ddd9dd))

## [1.9.1](https://github.com/NoNameItem/read-comics/compare/1.9.0...1.9.1) (2025-01-17)


### Bug Fixes

* **spiders:** Fixed api keys logging ([817f4ad](https://github.com/NoNameItem/read-comics/commit/817f4ad82fe490b19e4a423df390d081305bbffd))

## [1.9.0](https://github.com/NoNameItem/read-comics/compare/1.8.2...1.9.0) (2025-01-17)


### Features

* **spiders:** Multiple comicvine api keys support ([c5d513e](https://github.com/NoNameItem/read-comics/commit/c5d513e0e4310884039eef7de7ad57441eb32f74))

## [1.8.2](https://github.com/NoNameItem/read-comics/compare/1.8.1...1.8.2) (2025-01-17)


### Bug Fixes

* **spiders:** Decrease list api limit ([5594819](https://github.com/NoNameItem/read-comics/commit/55948190e299690c3c1738122944dffd6ec42cfc))

## [1.8.1](https://github.com/NoNameItem/read-comics/compare/1.8.0...1.8.1) (2025-01-14)


### Bug Fixes

* **spiders:** Prioritize next list link over detail links ([d00006f](https://github.com/NoNameItem/read-comics/commit/d00006f38cb7358e9e1a2ad9771517f3a0d9efbb))

## [1.8.0](https://github.com/NoNameItem/read-comics/compare/1.7.4...1.8.0) (2025-01-13)


### Features

* **spiders:** Save available info from list endpoints ([e594392](https://github.com/NoNameItem/read-comics/commit/e59439263968cad0094f4cad8e5d8c09ce7cca39))

## [1.7.4](https://github.com/NoNameItem/read-comics/compare/1.7.3...1.7.4) (2025-01-12)


### Bug Fixes

* **spiders:** Spider delay setting from env ([16f4080](https://github.com/NoNameItem/read-comics/commit/16f4080e8fd79d2260a4ad3ef0e81ef8719399ab))

## [1.7.3](https://github.com/NoNameItem/read-comics/compare/1.7.2...1.7.3) (2025-01-12)


### Bug Fixes

* **spiders:** Comicvine spiders settings ([6b8702f](https://github.com/NoNameItem/read-comics/commit/6b8702fb509b9b34a7d96446f7693fee49c646d5))

## [1.7.2](https://github.com/NoNameItem/read-comics/compare/1.7.1...1.7.2) (2025-01-12)


### Bug Fixes

* **spiders:** Celery tasks for different types of all spiders ([f559690](https://github.com/NoNameItem/read-comics/commit/f559690d75212de18acd67b48ecb2b5bedf96ae6))

## [1.7.1](https://github.com/NoNameItem/read-comics/compare/1.7.0...1.7.1) (2025-01-12)


### Bug Fixes

* **spiders:** Celery tasks for different types of full update ([07bbe0c](https://github.com/NoNameItem/read-comics/commit/07bbe0c8a3fb6c57ff4c7a94cada26eb9ff7937d))

## [1.7.0](https://github.com/NoNameItem/read-comics/compare/1.6.1...1.7.0) (2025-01-12)


### Features

* **spiders:** Celery tasks for different types of full update ([8b3bd9c](https://github.com/NoNameItem/read-comics/commit/8b3bd9c2145e3e6e78cc26d012698b1623d9c5d9))

## [1.6.1](https://github.com/NoNameItem/read-comics/compare/1.6.0...1.6.1) (2025-01-12)


### Bug Fixes

* Logging ([f4f967b](https://github.com/NoNameItem/read-comics/commit/f4f967b0959fc0c7e05e44dc41c247dd8eaeab3d))

## [1.6.0](https://github.com/NoNameItem/read-comics/compare/1.5.4...1.6.0) (2025-01-12)


### Features

* Added ability to http deploy ([afc51f0](https://github.com/NoNameItem/read-comics/commit/afc51f042374458b111b0c790da4095e69b55c90))

## [1.5.4](https://github.com/NoNameItem/read-comics/compare/1.5.3...1.5.4) (2025-01-11)


### Bug Fixes

* Moved gunicorn args to env variable ([aedf2ea](https://github.com/NoNameItem/read-comics/commit/aedf2eae2350c4b53412b9f49a28a2f40f490f11))

## [1.5.3](https://github.com/NoNameItem/read-comics/compare/1.5.2...1.5.3) (2025-01-10)


### Bug Fixes

* Fix pipeline ([e5a1dd4](https://github.com/NoNameItem/read-comics/commit/e5a1dd48de751ac7be815917b8e13e2e34d97211))

## [1.5.2](https://github.com/NoNameItem/read-comics/compare/1.5.1...1.5.2) (2025-01-10)


### Bug Fixes

* Disable Sentry ([4a5309e](https://github.com/NoNameItem/read-comics/commit/4a5309e8064314d797aee31953796355297eee19))

## [1.5.1](https://github.com/NoNameItem/read-comics/compare/1.5.0...1.5.1) (2024-05-06)


### Bug Fixes

* **issues:** Download link available only for logged in users ([f1a6b6e](https://github.com/NoNameItem/read-comics/commit/f1a6b6eb16927e59aaca1510787f46dda14f2f8e))

## [1.5.0](https://github.com/NoNameItem/read-comics/compare/1.4.6...1.5.0) (2024-04-15)


### Features

* **missing-issues:** Changed missing issues tasks schedule to refresh only on fridays ([4d94161](https://github.com/NoNameItem/read-comics/commit/4d9416102ade2b29e41c747e8a5ce4ac7f8b604e))

## [1.4.6](https://github.com/NoNameItem/read-comics/compare/1.4.5...1.4.6) (2024-04-02)


### Bug Fixes

* **missing-issues:** Check if issue is ignored before insert in missing issues ([8693658](https://github.com/NoNameItem/read-comics/commit/869365821c6c3006e5486674bf711210780a8906))

## [1.4.5](https://github.com/NoNameItem/read-comics/compare/1.4.4...1.4.5) (2024-04-02)


### Bug Fixes

* **missing-issues:** Check if issue is ignored before insert in missing issues ([8693658](https://github.com/NoNameItem/read-comics/commit/869365821c6c3006e5486674bf711210780a8906))

## [1.4.4](https://github.com/NoNameItem/read-comics/compare/1.4.3...1.4.4) (2024-03-03)


### Bug Fixes

* **missing-issues:** Publisher missing task fetch volumes ([a71fbdc](https://github.com/NoNameItem/read-comics/commit/a71fbdce46f8d7fdb78b20325195600499e52205))

## [1.4.3](https://github.com/NoNameItem/read-comics/compare/1.4.2...1.4.3) (2024-03-03)


### Bug Fixes

* **missing-issues:** Publisher missing task mongo query ([766aa44](https://github.com/NoNameItem/read-comics/commit/766aa4409bbe648f209d1f252fce24e3ded8ebd8))

## [1.4.2](https://github.com/NoNameItem/read-comics/compare/1.4.1...1.4.2) (2024-03-03)


### Bug Fixes

* **missing-issues:** Reset missing issue skip_date when issue no longer skipped ([26d29de](https://github.com/NoNameItem/read-comics/commit/26d29de00859c0b8b7dd1e64fb4348f30b372562))


### Performance Improvements

* **missing-issues:** Optimizing publisher missing task mongo query ([3a9fa50](https://github.com/NoNameItem/read-comics/commit/3a9fa504b851d93a35117982475e0904d6261e05))

## [1.4.1](https://github.com/NoNameItem/read-comics/compare/1.4.0...1.4.1) (2024-03-03)


### Bug Fixes

* **missing-issues:** Filtering of ignored publishers ([0cac79e](https://github.com/NoNameItem/read-comics/commit/0cac79ea87c5d5da839e1c350863e97f129b3303))

## [1.4.0](https://github.com/NoNameItem/read-comics/compare/1.3.6...1.4.0) (2024-03-03)


### Features

* **missing-issues:** Search missing issues for all publishers, even if publisher currently has 0 issues ([fa50a86](https://github.com/NoNameItem/read-comics/commit/fa50a86ea7d2baea370abd8236ad0285002e30c3))


### Bug Fixes

* **missing-issues:** Don't search missing issues for ignored publisher in manual run ([dc3b29e](https://github.com/NoNameItem/read-comics/commit/dc3b29ecb065a0e2ae65c5eed33896c4b27d98be))

## [1.3.6](https://github.com/NoNameItem/read-comics/compare/1.3.5...1.3.6) (2024-02-27)


### Bug Fixes

* Don't find missing issues for ignored publishers even if it watched ([9d90a3e](https://github.com/NoNameItem/read-comics/commit/9d90a3efa96732996a7b3da27f80be25ebf1ec54))

## [1.3.5](https://github.com/NoNameItem/read-comics/compare/1.3.4...1.3.5) (2024-02-22)


### Bug Fixes

* Bump scrappy version to include fix of https://github.com/scrapy/scrapy/issues/6024 ([9154d97](https://github.com/NoNameItem/read-comics/commit/9154d9756f4481f4e38ced12cec5e042ef89c963))

## [1.3.4](https://github.com/NoNameItem/read-comics/compare/1.3.3...1.3.4) (2024-02-20)


### Bug Fixes

* Issue DO key fixed ([a10e93d](https://github.com/NoNameItem/read-comics/commit/a10e93dde76da1071816c64e3a6e2484e33a4b6e))

## [1.3.3](https://github.com/NoNameItem/read-comics/compare/1.3.2...1.3.3) (2023-05-22)


### Bug Fixes

* **users:** Social login soon disable notification ([c7284ec](https://github.com/NoNameItem/read-comics/commit/c7284ec641af4a6b850ad0ba351d63264d44a11b))

## [1.3.2](https://github.com/NoNameItem/read-comics/compare/1.3.1...1.3.2) (2023-05-11)


### Bug Fixes

* Release fix ([b53eb4b](https://github.com/NoNameItem/read-comics/commit/b53eb4b8b0ad390691406d9e46b5ceb9cdd554e2))

## [1.3.1](https://github.com/NoNameItem/read-comics/compare/v1.3.0...1.3.1) (2023-05-11)


### Bug Fixes

* Please release config ([f5260fe](https://github.com/NoNameItem/read-comics/commit/f5260fe302bdd64c4f2516dd071c1d0a83d59e1c))

## [1.3.0](https://github.com/NoNameItem/read-comics/compare/v1.2.0...v1.3.0) (2023-05-11)


### Features

* Disable codecov ([04406d3](https://github.com/NoNameItem/read-comics/commit/04406d3714b1a35edf4917d280d83cfb5875294b))
* Pull requests setup ([51fb221](https://github.com/NoNameItem/read-comics/commit/51fb221684510bb33e5bc3cdace529bc569c274d))
* Sonar badges ([04406d3](https://github.com/NoNameItem/read-comics/commit/04406d3714b1a35edf4917d280d83cfb5875294b))
* Test publishing ([04406d3](https://github.com/NoNameItem/read-comics/commit/04406d3714b1a35edf4917d280d83cfb5875294b))
* Test publishing ([04406d3](https://github.com/NoNameItem/read-comics/commit/04406d3714b1a35edf4917d280d83cfb5875294b))
* Unit test continue in error ([04406d3](https://github.com/NoNameItem/read-comics/commit/04406d3714b1a35edf4917d280d83cfb5875294b))
* Update version in read_comics/__init__.py ([51fb221](https://github.com/NoNameItem/read-comics/commit/51fb221684510bb33e5bc3cdace529bc569c274d))


### Bug Fixes

* **core:** Broken accounts urls ([9f39e44](https://github.com/NoNameItem/read-comics/commit/9f39e44b07aba549104557a337cf9199e8933b0d))
* Delete codecov badge ([04406d3](https://github.com/NoNameItem/read-comics/commit/04406d3714b1a35edf4917d280d83cfb5875294b))
* Dev: ci pylint ([9f39e44](https://github.com/NoNameItem/read-comics/commit/9f39e44b07aba549104557a337cf9199e8933b0d))
* Fixed failing test ([04406d3](https://github.com/NoNameItem/read-comics/commit/04406d3714b1a35edf4917d280d83cfb5875294b))
* Fixed main branch ci permissions ([fc5d4a2](https://github.com/NoNameItem/read-comics/commit/fc5d4a2e0dd29d8d1458fdfef9930a181d811b22))
* Run actions on release PR ([d328519](https://github.com/NoNameItem/read-comics/commit/d328519b43f4252478fabd69a4eec695dd73258c))
* Sonar badges ([b12aa7a](https://github.com/NoNameItem/read-comics/commit/b12aa7a648596c14b1a637c20e841e121de9f91e))
* Test publishing fail job on test fails ([04406d3](https://github.com/NoNameItem/read-comics/commit/04406d3714b1a35edf4917d280d83cfb5875294b))
* Test publishing permissions ([04406d3](https://github.com/NoNameItem/read-comics/commit/04406d3714b1a35edf4917d280d83cfb5875294b))


### Build System

* **production-run:** Using standart traefik image ([9f39e44](https://github.com/NoNameItem/read-comics/commit/9f39e44b07aba549104557a337cf9199e8933b0d))
* **production-run:** Using standart traefik image ([954db68](https://github.com/NoNameItem/read-comics/commit/954db6844c311439ae31b856a38b8823e2e19541))

## 1.2.0 (2023-05-08)


### Bug Fixes

* Dev: release-please.yml ([ea57df0](https://github.com/NoNameItem/read-comics/commit/ea57df0d5a132dd26e3439025b9db81e1123f350))
* Dev: release-please.yml ([9121e3f](https://github.com/NoNameItem/read-comics/commit/9121e3fded1d3849095b2bf19edaf4779f23f336))
* Release-please.yml ([fab1aa8](https://github.com/NoNameItem/read-comics/commit/fab1aa88c9624a321ab2ddf52377dbfaa321a233))
* Release-please.yml ([32788b7](https://github.com/NoNameItem/read-comics/commit/32788b7fad6feb0d2b2a8e4df05f5edd7eff01a4))
