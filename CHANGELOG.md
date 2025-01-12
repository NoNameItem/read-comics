# Changelog

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
