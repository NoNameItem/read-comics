DRF migration URL map (captured 2025-12-20)

Rules used for status:
- If a ViewSet has no serializer_class, list/detail endpoints are treated as NOT READY.
- If a ViewSet lacks DetailSerializerMixin and serializer_detail_class, detail is treated as NEEDS WORK.
- Plan: use slug lookup for all endpoints that mirror slug-based Django URLs.

Legend:
- OK: endpoint exists and is ready.
- NEEDS WORK: endpoint exists but requires detail serializer.
- NOT READY: serializer_class missing; list/detail not usable.
- PLAN: DRF equivalent not implemented yet.

Search
| Django URL | DRF equivalent | Status/notes |
|---|---|---|
| /search/ | — | PLAN |
| /search/ajax/ | — | PLAN |

Characters
| Django URL | DRF equivalent | Status/notes |
|---|---|---|
| /characters/ | /api/characters/ | OK |
| /characters/<slug>/ | /api/characters/<slug>/ | OK |
| /characters/<slug>/technical-info/ | /api/characters/<slug>/technical-info/ | OK |
| /characters/<slug>/start_watch/ | /api/characters/<slug>/start-watch/ | PLAN |
| /characters/<slug>/stop_watch/ | /api/characters/<slug>/stop-watch/ | PLAN |
| /characters/<slug>/issues/ | /api/characters/<slug>/issues/ | PLAN |
| /characters/<slug>/volumes/ | /api/characters/<slug>/volumes/ | PLAN |
| /characters/<slug>/died_in_issues/ | /api/characters/<slug>/died-in-issues/ | PLAN |
| /characters/<slug>/enemies/ | /api/characters/<slug>/enemies/ | PLAN |
| /characters/<slug>/friends/ | /api/characters/<slug>/friends/ | PLAN |
| /characters/<slug>/teams/ | /api/characters/<slug>/teams/ | PLAN |
| /characters/<slug>/team_friends/ | /api/characters/<slug>/team-friends/ | PLAN |
| /characters/<slug>/team_enemies/ | /api/characters/<slug>/team-enemies/ | PLAN |
| /characters/<slug>/authors/ | /api/characters/<slug>/authors/ | PLAN |
| /characters/<character_slug>/issues/<issue_slug>/ | /api/characters/<slug>/issues/<issue_slug>/ | PLAN |

Concepts
| Django URL | DRF equivalent | Status/notes |
|---|---|---|
| /concepts/ | /api/concepts/ | OK |
| /concepts/<slug>/ | /api/concepts/<slug>/ | OK |
| /concepts/<slug>/technical-info/ | /api/concepts/<slug>/technical-info/ | OK |
| /concepts/<slug>/start_watch/ | /api/concepts/<slug>/start-watch/ | PLAN |
| /concepts/<slug>/stop_watch/ | /api/concepts/<slug>/stop-watch/ | PLAN |
| /concepts/<slug>/issues/ | /api/concepts/<slug>/issues/ | PLAN |
| /concepts/<slug>/volumes/ | /api/concepts/<slug>/volumes/ | PLAN |
| /concepts/<concept_slug>/issues/<issue_slug>/ | /api/concepts/<slug>/issues/<issue_slug>/ | PLAN |

Issues
| Django URL | DRF equivalent | Status/notes |
|---|---|---|
| /issues/ | /api/issues/ | OK |
| /issues/<slug>/ | /api/issues/<slug>/ | OK |
| /issues/<slug>/technical-info/ | /api/issues/<slug>/technical-info/ | OK |
| /issues/<slug>/mark_read/ | /api/issues/<slug>/mark-read/ | PLAN |
| /issues/<slug>/ | /api/issues/<slug>/characters/ | PLAN |
| /issues/<slug>/ | /api/issues/<slug>/characters-died/ | PLAN |
| /issues/<slug>/ | /api/issues/<slug>/concepts/ | PLAN |
| /issues/<slug>/ | /api/issues/<slug>/locations/ | PLAN |
| /issues/<slug>/ | /api/issues/<slug>/objects/ | PLAN |
| /issues/<slug>/ | /api/issues/<slug>/authors/ | PLAN |
| /issues/<slug>/ | /api/issues/<slug>/story-arcs/ | PLAN |
| /issues/<slug>/ | /api/issues/<slug>/teams/ | PLAN |
| /issues/<slug>/ | /api/issues/<slug>/disbanded-teams/ | PLAN |
| /issues/<slug>/ | /api/issues/<slug>/first-appearances/ | PLAN |

Locations
| Django URL | DRF equivalent | Status/notes |
|---|---|---|
| /locations/ | /api/locations/ | OK |
| /locations/<slug>/ | /api/locations/<slug>/ | OK |
| /locations/<slug>/technical-info/ | /api/locations/<slug>/technical-info/ | OK |
| /locations/<slug>/start_watch/ | /api/locations/<slug>/start-watch/ | PLAN |
| /locations/<slug>/stop_watch/ | /api/locations/<slug>/stop-watch/ | PLAN |
| /locations/<slug>/issues/ | /api/locations/<slug>/issues/ | PLAN |
| /locations/<slug>/volumes/ | /api/locations/<slug>/volumes/ | PLAN |
| /locations/<location_slug>/issues/<issue_slug>/ | /api/locations/<slug>/issues/<issue_slug>/ | PLAN |

Objects
| Django URL | DRF equivalent | Status/notes |
|---|---|---|
| /objects/ | /api/objects/ | OK (list) |
| /objects/<slug>/ | /api/objects/<slug>/ | NEEDS WORK (detail serializer); slug lookup pending (currently pk) |
| /objects/<slug>/technical-info/ | /api/objects/<slug>/technical-info/ | PLAN (plus detail serializer); slug lookup pending (currently pk) |
| /objects/<slug>/start_watch/ | /api/objects/<slug>/start-watch/ | PLAN; slug lookup pending (currently pk) |
| /objects/<slug>/stop_watch/ | /api/objects/<slug>/stop-watch/ | PLAN; slug lookup pending (currently pk) |
| /objects/<slug>/issues/ | /api/objects/<slug>/issues/ | PLAN; slug lookup pending (currently pk) |
| /objects/<slug>/volumes/ | /api/objects/<slug>/volumes/ | PLAN; slug lookup pending (currently pk) |
| /objects/<object_slug>/issues/<issue_slug>/ | /api/objects/<slug>/issues/<issue_slug>/ | PLAN; slug lookup pending (currently pk) |

People
| Django URL | DRF equivalent | Status/notes |
|---|---|---|
| /people/ | /api/people/ | OK (list) |
| /people/<slug>/ | /api/people/<slug>/ | NEEDS WORK (detail serializer); slug lookup pending (currently pk) |
| /people/<slug>/technical-info/ | /api/people/<slug>/technical-info/ | PLAN; slug lookup pending (currently pk) |
| /people/<slug>/start_watch/ | /api/people/<slug>/start-watch/ | PLAN; slug lookup pending (currently pk) |
| /people/<slug>/stop_watch/ | /api/people/<slug>/stop-watch/ | PLAN; slug lookup pending (currently pk) |
| /people/<slug>/issues/ | /api/people/<slug>/issues/ | PLAN; slug lookup pending (currently pk) |
| /people/<slug>/volumes/ | /api/people/<slug>/volumes/ | PLAN; slug lookup pending (currently pk) |
| /people/<slug>/characters/ | /api/people/<slug>/characters/ | PLAN; slug lookup pending (currently pk) |
| /people/<person_slug>/issues/<issue_slug>/ | /api/people/<slug>/issues/<issue_slug>/ | PLAN; slug lookup pending (currently pk) |

Publishers
| Django URL | DRF equivalent | Status/notes |
|---|---|---|
| /publishers/ | /api/publishers/ | OK (list) |
| /publishers/<slug>/ | /api/publishers/<slug>/ | NEEDS WORK (detail serializer); slug lookup pending (currently pk) |
| /publishers/<slug>/technical-info/ | /api/publishers/<slug>/technical-info/ | PLAN; slug lookup pending (currently pk) |
| /publishers/<slug>/start_watch/ | /api/publishers/<slug>/start-watch/ | PLAN; slug lookup pending (currently pk) |
| /publishers/<slug>/stop_watch/ | /api/publishers/<slug>/stop-watch/ | PLAN; slug lookup pending (currently pk) |
| /publishers/<slug>/issues/ | /api/publishers/<slug>/issues/ | PLAN; slug lookup pending (currently pk) |
| /publishers/<slug>/characters/ | /api/publishers/<slug>/characters/ | PLAN; slug lookup pending (currently pk) |
| /publishers/<slug>/teams/ | /api/publishers/<slug>/teams/ | PLAN; slug lookup pending (currently pk) |
| /publishers/<slug>/story_arcs/ | /api/publishers/<slug>/story-arcs/ | PLAN; slug lookup pending (currently pk) |
| /publishers/<slug>/volumes/ | /api/publishers/<slug>/volumes/ | PLAN; slug lookup pending (currently pk) |
| /publishers/<publisher_slug>/issues/<issue_slug>/ | /api/publishers/<slug>/issues/<issue_slug>/ | PLAN; slug lookup pending (currently pk) |

Story arcs
| Django URL | DRF equivalent | Status/notes |
|---|---|---|
| /story_arcs/ | /api/story-arcs/ | OK (list) |
| /story_arcs/continue_reading | /api/story-arcs/started/ | OK (action started) |
| /story_arcs/<slug>/ | /api/story-arcs/<slug>/ | NEEDS WORK (detail serializer); slug lookup pending (currently pk) |
| /story_arcs/<slug>/technical-info/ | /api/story-arcs/<slug>/technical-info/ | PLAN; slug lookup pending (currently pk) |
| /story_arcs/<slug>/start_watch/ | /api/story-arcs/<slug>/start-watch/ | PLAN; slug lookup pending (currently pk) |
| /story_arcs/<slug>/stop_watch/ | /api/story-arcs/<slug>/stop-watch/ | PLAN; slug lookup pending (currently pk) |
| /story_arcs/<slug>/mark_finished/ | /api/story-arcs/<slug>/mark-finished/ | PLAN; slug lookup pending (currently pk) |
| /story_arcs/<slug>/died/ | /api/story-arcs/<slug>/died/ | PLAN; slug lookup pending (currently pk) |
| /story_arcs/<slug>/authors/ | /api/story-arcs/<slug>/authors/ | PLAN; slug lookup pending (currently pk) |
| /story_arcs/<slug>/characters/ | /api/story-arcs/<slug>/characters/ | PLAN; slug lookup pending (currently pk) |
| /story_arcs/<slug>/concepts/ | /api/story-arcs/<slug>/concepts/ | PLAN; slug lookup pending (currently pk) |
| /story_arcs/<slug>/disbanded/ | /api/story-arcs/<slug>/disbanded/ | PLAN; slug lookup pending (currently pk) |
| /story_arcs/<slug>/first_appearances/ | /api/story-arcs/<slug>/first-appearances/ | PLAN; slug lookup pending (currently pk) |
| /story_arcs/<story_arc_slug>/issues/<issue_slug>/ | /api/story-arcs/<slug>/issues/<issue_slug>/ | PLAN; slug lookup pending (currently pk) |
| /story_arcs/<slug>/locations/ | /api/story-arcs/<slug>/locations/ | PLAN; slug lookup pending (currently pk) |
| /story_arcs/<slug>/issues/ | /api/story-arcs/<slug>/issues/ | PLAN; slug lookup pending (currently pk) |
| /story_arcs/<slug>/objects/ | /api/story-arcs/<slug>/objects/ | PLAN; slug lookup pending (currently pk) |
| /story_arcs/<slug>/teams/ | /api/story-arcs/<slug>/teams/ | PLAN; slug lookup pending (currently pk) |
| /story_arcs/<slug>/volumes/ | /api/story-arcs/<slug>/volumes/ | PLAN; slug lookup pending (currently pk) |

Teams
| Django URL | DRF equivalent | Status/notes |
|---|---|---|
| /teams/ | /api/teams/ | OK (list) |
| /teams/<slug>/ | /api/teams/<slug>/ | NEEDS WORK (detail serializer); slug lookup pending (currently pk) |
| /teams/<slug>/technical-info/ | /api/teams/<slug>/technical-info/ | PLAN; slug lookup pending (currently pk) |
| /teams/<slug>/start_watch/ | /api/teams/<slug>/start-watch/ | PLAN; slug lookup pending (currently pk) |
| /teams/<slug>/stop_watch/ | /api/teams/<slug>/stop-watch/ | PLAN; slug lookup pending (currently pk) |
| /teams/<team_slug>/issues/<issue_slug>/ | /api/teams/<slug>/issues/<issue_slug>/ | PLAN; slug lookup pending (currently pk) |
| /teams/<slug>/issues/ | /api/teams/<slug>/issues/ | PLAN; slug lookup pending (currently pk) |
| /teams/<slug>/enemies/ | /api/teams/<slug>/enemies/ | PLAN; slug lookup pending (currently pk) |
| /teams/<slug>/volumes/ | /api/teams/<slug>/volumes/ | PLAN; slug lookup pending (currently pk) |
| /teams/<slug>/friends/ | /api/teams/<slug>/friends/ | PLAN; slug lookup pending (currently pk) |
| /teams/<slug>/characters/ | /api/teams/<slug>/characters/ | PLAN; slug lookup pending (currently pk) |
| /teams/<slug>/disbanded_in/ | /api/teams/<slug>/disbanded-in/ | PLAN; slug lookup pending (currently pk) |

Volumes
| Django URL | DRF equivalent | Status/notes |
|---|---|---|
| /volumes/ | /api/volumes/ | OK (list) |
| /volumes/continue_reading | /api/volumes/started/ | OK (action started) |
| /volumes/<slug>/ | /api/volumes/<slug>/ | NEEDS WORK (detail serializer); slug lookup pending (currently pk) |
| /volumes/<slug>/technical-info/ | /api/volumes/<slug>/technical-info/ | PLAN; slug lookup pending (currently pk) |
| /volumes/random/ | — | PLAN |
| /volumes/<slug>/start_watch/ | /api/volumes/<slug>/start-watch/ | PLAN; slug lookup pending (currently pk) |
| /volumes/<slug>/stop_watch/ | /api/volumes/<slug>/stop-watch/ | PLAN; slug lookup pending (currently pk) |
| /volumes/<slug>/mark_finished/ | /api/volumes/<slug>/mark-finished/ | PLAN; slug lookup pending (currently pk) |
| /volumes/<slug>/issues/ | /api/volumes/<slug>/issues/ | PLAN; slug lookup pending (currently pk) |
| /volumes/<slug>/characters/ | /api/volumes/<slug>/characters/ | PLAN; slug lookup pending (currently pk) |
| /volumes/<slug>/died/ | /api/volumes/<slug>/died/ | PLAN; slug lookup pending (currently pk) |
| /volumes/<slug>/concepts/ | /api/volumes/<slug>/concepts/ | PLAN; slug lookup pending (currently pk) |
| /volumes/<slug>/locations/ | /api/volumes/<slug>/locations/ | PLAN; slug lookup pending (currently pk) |
| /volumes/<slug>/objects/ | /api/volumes/<slug>/objects/ | PLAN; slug lookup pending (currently pk) |
| /volumes/<slug>/authors/ | /api/volumes/<slug>/authors/ | PLAN; slug lookup pending (currently pk) |
| /volumes/<slug>/story_arcs/ | /api/volumes/<slug>/story-arcs/ | PLAN; slug lookup pending (currently pk) |
| /volumes/<slug>/teams/ | /api/volumes/<slug>/teams/ | PLAN; slug lookup pending (currently pk) |
| /volumes/<slug>/disbanded/ | /api/volumes/<slug>/disbanded/ | PLAN; slug lookup pending (currently pk) |
| /volumes/<slug>/first_appearances/ | /api/volumes/<slug>/first-appearances/ | PLAN; slug lookup pending (currently pk) |
| /volumes/<volume_slug>/issues/<issue_slug> | /api/volumes/<slug>/issues/<issue_slug>/ | PLAN; slug lookup pending (currently pk) |

Missing Issues (detailed)
| Django URL | DRF equivalent | Status/notes |
|---|---|---|
| /missing_issues/ | /api/missing-issues/ | NOT READY (no serializer_class) |
| /missing_issues/do_space/ | /api/missing-issues/do-space/ | PLAN |
| /missing_issues/purge_deleted/ | /api/missing-issues/purge-deleted/ | PLAN |
| /missing_issues/ignored_issues/ | /api/missing-issues/ignored-issues/ | PLAN |
| /missing_issues/ignored_volumes/ | /api/missing-issues/ignored-volumes/ | PLAN |
| /missing_issues/ignored_publishers/ | /api/missing-issues/ignored-publishers/ | PLAN |
| /missing_issues/ignored_issues/<pk>/delete/ | /api/missing-issues/ignored-issues/<pk>/delete/ | PLAN |
| /missing_issues/ignored_volumes/<pk>/delete/ | /api/missing-issues/ignored-volumes/<pk>/delete/ | PLAN |
| /missing_issues/ignored_publishers/<pk>/delete/ | /api/missing-issues/ignored-publishers/<pk>/delete/ | PLAN |
| /missing_issues/skip_issue/<comicvine_id>/ | /api/missing-issues/skip-issue/<comicvine_id>/ | PLAN |
| /missing_issues/skip_volume/<comicvine_id>/ | /api/missing-issues/skip-volume/<comicvine_id>/ | PLAN |
| /missing_issues/skip_publisher/<comicvine_id>/ | /api/missing-issues/skip-publisher/<comicvine_id>/ | PLAN |
| /missing_issues/ignore_issue/<comicvine_id>/ | /api/missing-issues/ignore-issue/<comicvine_id>/ | PLAN |
| /missing_issues/ignore_volume/<comicvine_id>/ | /api/missing-issues/ignore-volume/<comicvine_id>/ | PLAN |
| /missing_issues/ignore_publisher/<comicvine_id>/ | /api/missing-issues/ignore-publisher/<comicvine_id>/ | PLAN |
| /missing_issues/reload_from_do/ | /api/missing-issues/reload-from-do/ | PLAN |
| /missing_issues/watched/ | /api/missing-issues/watched/ | PLAN |
| /missing_issues/watched/skip_issue/<comicvine_id>/ | /api/missing-issues/watched/skip-issue/<comicvine_id>/ | PLAN |
| /missing_issues/watched/skip_volume/<comicvine_id>/ | /api/missing-issues/watched/skip-volume/<comicvine_id>/ | PLAN |
| /missing_issues/watched/skip_publisher/<comicvine_id>/ | /api/missing-issues/watched/skip-publisher/<comicvine_id>/ | PLAN |
| /missing_issues/watched/ignore_issue/<comicvine_id>/ | /api/missing-issues/watched/ignore-issue/<comicvine_id>/ | PLAN |
| /missing_issues/watched/ignore_volume/<comicvine_id>/ | /api/missing-issues/watched/ignore-volume/<comicvine_id>/ | PLAN |
| /missing_issues/watched/ignore_publisher/<comicvine_id>/ | /api/missing-issues/watched/ignore-publisher/<comicvine_id>/ | PLAN |
| /missing_issues/<category>/<slug>/ | /api/<category_plural>/<slug>/missing-issues/ | PLAN |
| /missing_issues/<category>/<slug>/skip_issue/<comicvine_id>/ | /api/<category_plural>/<slug>/missing-issues/skip-issue/<comicvine_id>/ | PLAN |
| /missing_issues/<category>/<slug>/skip_volume/<comicvine_id>/ | /api/<category_plural>/<slug>/missing-issues/skip-volume/<comicvine_id>/ | PLAN |
| /missing_issues/<category>/<slug>/skip_publisher/<comicvine_id>/ | /api/<category_plural>/<slug>/missing-issues/skip-publisher/<comicvine_id>/ | PLAN |
| /missing_issues/<category>/<slug>/ignore_issue/<comicvine_id>/ | /api/<category_plural>/<slug>/missing-issues/ignore-issue/<comicvine_id>/ | PLAN |
| /missing_issues/<category>/<slug>/ignore_volume/<comicvine_id>/ | /api/<category_plural>/<slug>/missing-issues/ignore-volume/<comicvine_id>/ | PLAN |
| /missing_issues/<category>/<slug>/ignore_publisher/<comicvine_id>/ | /api/<category_plural>/<slug>/missing-issues/ignore-publisher/<comicvine_id>/ | PLAN |
