# Changelog

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
