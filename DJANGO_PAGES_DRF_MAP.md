DJANGO pages -> planned DRF endpoints (block mapping)

Notes:
- If an endpoint is marked TBD, it is not yet defined in DRF_MIGRATION_URL_MAP.md.
- Downloads remain in Django (no DRF endpoint planned).
- Plan: use slug lookup for all endpoints that mirror slug-based Django URLs.

Home page (`/`, `core/home.html`)
- Reading progress -> /api/profile/finished-stats/ (OK)
- Unfinished volumes -> /api/volumes/started/
- Unfinished story arcs -> /api/story-arcs/started/
- Counter cards -> entity count endpoints (OK; e.g., /api/characters/count/, /api/issues/count/, etc.)
- Update history -> /api/issues/update-history/

New issues by day (`/new_issues/<year>/<month>/<day>/`, `core/new_issues.html`)
- Page data -> TBD (suggest /api/issues/by-date/<year>/<month>/<day>/)

Search page (`/search/`, `search/search.html`)
- Page data -> /api/search/ (PLAN)

Characters list (`/characters/`, `characters/list.html`)
- Page data -> /api/characters/ (OK)

Concepts list (`/concepts/`, `concepts/list.html`)
- Page data -> /api/concepts/ (OK)

Issues list (`/issues/`, `issues/list.html`)
- Page data -> /api/issues/ (OK)

Locations list (`/locations/`, `locations/list.html`)
- Page data -> /api/locations/ (OK)

Objects list (`/objects/`, `objects/list.html`)
- Page data -> /api/objects/ (OK)

People list (`/people/`, `people/list.html`)
- Page data -> /api/people/ (OK)

Publishers list (`/publishers/`, `publishers/list.html`)
- Page data -> /api/publishers/ (OK)

Story arcs list (`/story_arcs/`, `story_arcs/list.html`)
- Page data -> /api/story-arcs/ (OK)

Teams list (`/teams/`, `teams/list.html`)
- Page data -> /api/teams/ (OK)

Volumes list (`/volumes/`, `volumes/list.html`)
- Page data -> /api/volumes/ (OK)

Volumes continue reading (`/volumes/continue_reading`, `volumes/continue_reading.html`)
- Page data -> /api/volumes/started/ (OK)

Story arcs continue reading (`/story_arcs/continue_reading`, `story_arcs/continue_reading.html`)
- Page data -> /api/story-arcs/started/ (OK)

Character detail (`/characters/<slug>/`, `characters/detail.html`)
- Header + Tab selector -> /api/characters/<slug>/ (OK)
- Reading progress -> /api/characters/<slug>/ (OK)
- Main info tab -> /api/characters/<slug>/ (OK)
- Issues tab -> /api/characters/<slug>/issues/ (PLAN)
- Volumes tab -> /api/characters/<slug>/volumes/ (PLAN)
- Died in tab -> /api/characters/<slug>/died-in-issues/ (PLAN)
- Authors tab -> /api/characters/<slug>/authors/ (PLAN)
- Friends tab -> /api/characters/<slug>/friends/ (PLAN)
- Enemies tab -> /api/characters/<slug>/enemies/ (PLAN)
- Teams tab -> /api/characters/<slug>/teams/ (PLAN)
- Team friends tab -> /api/characters/<slug>/team-friends/ (PLAN)
- Team enemies tab -> /api/characters/<slug>/team-enemies/ (PLAN)
- Missing issues link (staff) -> no DRF endpoint (staff-only link)
- Technical info tab -> /api/characters/<slug>/technical-info/ (OK)
- Start/stop watch -> /api/characters/<slug>/start-watch/ (PLAN), /api/characters/<slug>/stop-watch/ (PLAN)
- Download -> Django only

Concept detail (`/concepts/<slug>/`, `concepts/detail.html`)
- Header + Tab selector -> /api/concepts/<slug>/ (OK)
- Reading progress -> /api/concepts/<slug>/ (OK)
- Main info tab -> /api/concepts/<slug>/ (OK)
- Issues tab -> /api/concepts/<slug>/issues/ (PLAN)
- Volumes tab -> /api/concepts/<slug>/volumes/ (PLAN)
- Missing issues link (staff) -> no DRF endpoint (staff-only link)
- Technical info tab -> /api/concepts/<slug>/technical-info/ (OK)
- Start/stop watch -> /api/concepts/<slug>/start-watch/ (PLAN), /api/concepts/<slug>/stop-watch/ (PLAN)
- Download -> Django only

Issue detail (`/issues/<slug>/`, `issues/detail.html`)
- Header + Tab selector -> /api/issues/<slug>/ (OK)
- Reading progress (volume + issue) -> /api/volumes/<slug>/ (detail) + /api/issues/<slug>/ (detail)
- Main info tab -> /api/issues/<slug>/ (OK)
- Characters tab -> /api/issues/<slug>/characters/ (PLAN)
- Characters died tab -> /api/issues/<slug>/characters-died/ (PLAN)
- Concepts tab -> /api/issues/<slug>/concepts/ (PLAN)
- Locations tab -> /api/issues/<slug>/locations/ (PLAN)
- Objects tab -> /api/issues/<slug>/objects/ (PLAN)
- Authors tab -> /api/issues/<slug>/authors/ (PLAN)
- Story arcs tab -> /api/issues/<slug>/story-arcs/ (PLAN)
- Teams tab -> /api/issues/<slug>/teams/ (PLAN)
- Disbanded teams tab -> /api/issues/<slug>/disbanded-teams/ (PLAN)
- First appearances tab -> /api/issues/<slug>/first-appearances/ (PLAN)
- Technical info tab -> /api/issues/<slug>/technical-info/ (OK)
- Download -> Django only
- Mark read -> /api/issues/<slug>/mark-read/ (PLAN)
- Previous/Next -> /api/issues/<slug>/ (OK)

Character Issue detail (`/characters/<slug>/issues/<issue_slug>/`, `issues/detail.html`)
- Reading progress (volume + character) -> /api/volumes/<slug>/ (detail) + /api/characters/<slug>/ (detail)
- Previous/Next (within sublist) -> /api/characters/<slug>/issues/<issue_slug>/ (PLAN)

Concept Issue detail (`/concepts/<slug>/issues/<issue_slug>/`, `issues/detail.html`)
- Reading progress (volume + concept) -> /api/volumes/<slug>/ (detail) + /api/concepts/<slug>/ (detail)
- Previous/Next (within sublist) -> /api/concepts/<slug>/issues/<issue_slug>/ (PLAN)

Location Issue detail (`/locations/<slug>/issues/<issue_slug>/`, `issues/detail.html`)
- Reading progress (volume + location) -> /api/volumes/<slug>/ (detail) + /api/locations/<slug>/ (detail)
- Previous/Next (within sublist) -> /api/locations/<slug>/issues/<issue_slug>/ (PLAN)

Object Issue detail (`/objects/<slug>/issues/<issue_slug>/`, `issues/detail.html`)
- Reading progress (volume + object) -> /api/volumes/<slug>/ (detail) + /api/objects/<slug>/ (detail)
- Previous/Next (within sublist) -> /api/objects/<slug>/issues/<issue_slug>/ (PLAN)

People Issue detail (`/people/<slug>/issues/<issue_slug>/`, `issues/detail.html`)
- Reading progress (volume + person) -> /api/volumes/<slug>/ (detail) + /api/people/<slug>/ (detail)
- Previous/Next (within sublist) -> /api/people/<slug>/issues/<issue_slug>/ (PLAN)

Publisher Issue detail (`/publishers/<slug>/issues/<issue_slug>/`, `issues/detail.html`)
- Reading progress (volume + publisher) -> /api/volumes/<slug>/ (detail) + /api/publishers/<slug>/ (detail)
- Previous/Next (within sublist) -> /api/publishers/<slug>/issues/<issue_slug>/ (PLAN)

Story Arc Issue detail (`/story_arcs/<slug>/issues/<issue_slug>/`, `issues/detail.html`)
- Reading progress (volume + story arc) -> /api/volumes/<slug>/ (detail) + /api/story-arcs/<slug>/ (detail)
- Previous/Next (within sublist) -> /api/story-arcs/<slug>/issues/<issue_slug>/ (PLAN)

Team Issue detail (`/teams/<slug>/issues/<issue_slug>/`, `issues/detail.html`)
- Reading progress (volume + team) -> /api/volumes/<slug>/ (detail) + /api/teams/<slug>/ (detail)
- Previous/Next (within sublist) -> /api/teams/<slug>/issues/<issue_slug>/ (PLAN)

Volume Issue detail (`/volumes/<slug>/issues/<issue_slug>/`, `issues/detail.html`)
- Reading progress (volume + volume) -> /api/volumes/<slug>/ (detail; same endpoint for volume entity)
- Previous/Next (within sublist) -> /api/volumes/<slug>/issues/<issue_slug>/ (PLAN)

Location detail (`/locations/<slug>/`, `locations/detail.html`)
- Header + Tab selector -> /api/locations/<slug>/ (OK)
- Reading progress -> /api/locations/<slug>/ (OK)
- Main info tab -> /api/locations/<slug>/ (OK)
- Issues tab -> /api/locations/<slug>/issues/ (PLAN)
- Volumes tab -> /api/locations/<slug>/volumes/ (PLAN)
- Missing issues link (staff) -> no DRF endpoint (staff-only link)
- Technical info tab -> /api/locations/<slug>/technical-info/ (OK)
- Start/stop watch -> /api/locations/<slug>/start-watch/ (PLAN), /api/locations/<slug>/stop-watch/ (PLAN)
- Download -> Django only

Object detail (`/objects/<slug>/`, `objects/detail.html`)
- Header + Tab selector -> /api/objects/<slug>/
- Reading progress -> /api/objects/<slug>/
- Main info tab -> /api/objects/<slug>/
- Issues tab -> /api/objects/<slug>/issues/ (PLAN)
- Volumes tab -> /api/objects/<slug>/volumes/ (PLAN)
- Missing issues link (staff) -> no DRF endpoint (staff-only link)
- Technical info tab -> /api/objects/<slug>/technical-info/ (PLAN)
- Start/stop watch -> /api/objects/<slug>/start-watch/ (PLAN), /api/objects/<slug>/stop-watch/ (PLAN)
- Download -> Django only

People detail (`/people/<slug>/`, `people/detail.html`)
- Header + Tab selector -> /api/people/<slug>/
- Reading progress -> /api/people/<slug>/
- Main info tab -> /api/people/<slug>/
- Issues tab -> /api/people/<slug>/issues/ (PLAN)
- Volumes tab -> /api/people/<slug>/volumes/ (PLAN)
- Characters tab -> /api/people/<slug>/characters/ (PLAN)
- Missing issues link (staff) -> no DRF endpoint (staff-only link)
- Technical info tab -> /api/people/<slug>/technical-info/ (PLAN)
- Start/stop watch -> /api/people/<slug>/start-watch/ (PLAN), /api/people/<slug>/stop-watch/ (PLAN)
- Download -> Django only

Publisher detail (`/publishers/<slug>/`, `publishers/detail.html`)
- Header + Tab selector -> /api/publishers/<slug>/
- Reading progress -> /api/publishers/<slug>/
- Main info tab -> /api/publishers/<slug>/
- Issues tab -> /api/publishers/<slug>/issues/ (PLAN)
- Volumes tab -> /api/publishers/<slug>/volumes/ (PLAN)
- Characters tab -> /api/publishers/<slug>/characters/ (PLAN)
- Story arcs tab -> /api/publishers/<slug>/story-arcs/ (PLAN)
- Teams tab -> /api/publishers/<slug>/teams/ (PLAN)
- Missing issues link (staff) -> no DRF endpoint (staff-only link)
- Technical info tab -> /api/publishers/<slug>/technical-info/ (PLAN)
- Start/stop watch -> /api/publishers/<slug>/start-watch/ (PLAN), /api/publishers/<slug>/stop-watch/ (PLAN)
- Download -> Django only

Story arc detail (`/story_arcs/<slug>/`, `story_arcs/detail.html`)
- Header + Tab selector -> /api/story-arcs/<slug>/
- Reading progress -> /api/story-arcs/<slug>/
- Main info tab -> /api/story-arcs/<slug>/
- Issues tab -> /api/story-arcs/<slug>/issues/ (PLAN)
- Volumes tab -> /api/story-arcs/<slug>/volumes/ (PLAN)
- Characters tab -> /api/story-arcs/<slug>/characters/ (PLAN)
- Died tab -> /api/story-arcs/<slug>/died/ (PLAN)
- Concepts tab -> /api/story-arcs/<slug>/concepts/ (PLAN)
- Locations tab -> /api/story-arcs/<slug>/locations/ (PLAN)
- Objects tab -> /api/story-arcs/<slug>/objects/ (PLAN)
- Authors tab -> /api/story-arcs/<slug>/authors/ (PLAN)
- Teams tab -> /api/story-arcs/<slug>/teams/ (PLAN)
- Disbanded tab -> /api/story-arcs/<slug>/disbanded/ (PLAN)
- First appearances tab -> /api/story-arcs/<slug>/first-appearances/ (PLAN)
- Missing issues link (staff) -> no DRF endpoint (staff-only link)
- Technical info tab -> /api/story-arcs/<slug>/technical-info/ (PLAN)
- Start/stop watch -> /api/story-arcs/<slug>/start-watch/ (PLAN), /api/story-arcs/<slug>/stop-watch/ (PLAN)
- Mark finished -> /api/story-arcs/<slug>/mark-finished/ (PLAN)
- Download -> Django only

Team detail (`/teams/<slug>/`, `teams/detail.html`)
- Header + Tab selector -> /api/teams/<slug>/
- Reading progress -> /api/teams/<slug>/
- Main info tab -> /api/teams/<slug>/
- Issues tab -> /api/teams/<slug>/issues/ (PLAN)
- Volumes tab -> /api/teams/<slug>/volumes/ (PLAN)
- Disbanded in issues tab -> /api/teams/<slug>/disbanded-in/ (PLAN)
- Characters tab -> /api/teams/<slug>/characters/ (PLAN)
- Friends tab -> /api/teams/<slug>/friends/ (PLAN)
- Enemies tab -> /api/teams/<slug>/enemies/ (PLAN)
- Missing issues link (staff) -> no DRF endpoint (staff-only link)
- Technical info tab -> /api/teams/<slug>/technical-info/ (PLAN)
- Start/stop watch -> /api/teams/<slug>/start-watch/ (PLAN), /api/teams/<slug>/stop-watch/ (PLAN)
- Download -> Django only

Volume detail (`/volumes/<slug>/`, `volumes/detail.html`)
- Header + Tab selector -> /api/volumes/<slug>/
- Reading progress -> /api/volumes/<slug>/
- Main info tab -> /api/volumes/<slug>/
- Issues tab -> /api/volumes/<slug>/issues/ (PLAN)
- Characters tab -> /api/volumes/<slug>/characters/ (PLAN)
- Died tab -> /api/volumes/<slug>/died/ (PLAN)
- Concepts tab -> /api/volumes/<slug>/concepts/ (PLAN)
- Locations tab -> /api/volumes/<slug>/locations/ (PLAN)
- Objects tab -> /api/volumes/<slug>/objects/ (PLAN)
- Authors tab -> /api/volumes/<slug>/authors/ (PLAN)
- Story arcs tab -> /api/volumes/<slug>/story-arcs/ (PLAN)
- Teams tab -> /api/volumes/<slug>/teams/ (PLAN)
- Disbanded tab -> /api/volumes/<slug>/disbanded/ (PLAN)
- First appearances tab -> /api/volumes/<slug>/first-appearances/ (PLAN)
- Missing issues link (staff) -> no DRF endpoint (staff-only link)
- Technical info tab -> /api/volumes/<slug>/technical-info/ (PLAN)
- Start/stop watch -> /api/volumes/<slug>/start-watch/ (PLAN), /api/volumes/<slug>/stop-watch/ (PLAN)
- Mark finished -> /api/volumes/<slug>/mark-finished/ (PLAN)
- Download -> Django only

Missing issues list (`/missing_issues/`, `missing_issues/missing_issues_list.html`)
- Purge deleted -> /api/missing-issues/purge-deleted/ (PLAN)
- Issues table -> /api/missing-issues/ (NOT READY)
- DO Reload modal (tree + confirm) -> /api/missing-issues/reload-from-do/ (PLAN)
- Skip publisher -> /api/missing-issues/skip-publisher/<comicvine_id>/ (PLAN)
- Ignore publisher -> /api/missing-issues/ignore-publisher/<comicvine_id>/ (PLAN)
- Skip volume -> /api/missing-issues/skip-volume/<comicvine_id>/ (PLAN)
- Ignore volume -> /api/missing-issues/ignore-volume/<comicvine_id>/ (PLAN)
- Skip issue -> /api/missing-issues/skip-issue/<comicvine_id>/ (PLAN)
- Ignore issue -> /api/missing-issues/ignore-issue/<comicvine_id>/ (PLAN)

Character missing issues list (`/missing_issues/character/<slug>/`, `missing_issues/missing_issues_list.html`)
- Page data -> /api/characters/<slug>/missing-issues/ (PLAN)

Concept missing issues list (`/missing_issues/concept/<slug>/`, `missing_issues/missing_issues_list.html`)
- Page data -> /api/concepts/<slug>/missing-issues/ (PLAN)

Location missing issues list (`/missing_issues/location/<slug>/`, `missing_issues/missing_issues_list.html`)
- Page data -> /api/locations/<slug>/missing-issues/ (PLAN)

Object missing issues list (`/missing_issues/object/<slug>/`, `missing_issues/missing_issues_list.html`)
- Page data -> /api/objects/<slug>/missing-issues/ (PLAN)

Person missing issues list (`/missing_issues/person/<slug>/`, `missing_issues/missing_issues_list.html`)
- Page data -> /api/people/<slug>/missing-issues/ (PLAN)

Publisher missing issues list (`/missing_issues/publisher/<slug>/`, `missing_issues/missing_issues_list.html`)
- Page data -> /api/publishers/<slug>/missing-issues/ (PLAN)

Story arc missing issues list (`/missing_issues/story_arc/<slug>/`, `missing_issues/missing_issues_list.html`)
- Page data -> /api/story-arcs/<slug>/missing-issues/ (PLAN)

Team missing issues list (`/missing_issues/team/<slug>/`, `missing_issues/missing_issues_list.html`)
- Page data -> /api/teams/<slug>/missing-issues/ (PLAN)

Volume missing issues list (`/missing_issues/volume/<slug>/`, `missing_issues/missing_issues_list.html`)
- Page data -> /api/volumes/<slug>/missing-issues/ (PLAN)

Ignored issues list (`/missing_issues/ignored_issues/`, `missing_issues/ignored_issues_list.html`)
- Table of ignored issues -> /api/missing-issues/ignored-issues/ (PLAN)
- Delete ignored issue -> /api/missing-issues/ignored-issues/<pk>/delete/ (PLAN)

Ignored volumes list (`/missing_issues/ignored_volumes/`, `missing_issues/ignored_volumes_list.html`)
- Table of ignored volumes -> /api/missing-issues/ignored-volumes/ (PLAN)
- Delete ignored volume -> /api/missing-issues/ignored-volumes/<pk>/delete/ (PLAN)

Ignored publishers list (`/missing_issues/ignored_publishers/`, `missing_issues/ignored_publishers_list.html`)
- Table of ignored publishers -> /api/missing-issues/ignored-publishers/ (PLAN)
- Delete ignored publisher -> /api/missing-issues/ignored-publishers/<pk>/delete/ (PLAN)
