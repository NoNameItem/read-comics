Refactoring Plan (pages -> tasks, blocks -> subtasks)

## Task: Home page ([RC-8](https://nonameitem.atlassian.net/browse/RC-8))
Description: Django URL: `/`, template: `core/home.html`
Tags: home
Subtasks:
- Reading progress — endpoints: /api/profile/finished-stats/ [OK] | tags: home | Jira: [RC-28](https://nonameitem.atlassian.net/browse/RC-28)
- Unfinished volumes — endpoints: /api/volumes/started/ [OK (action started)] (ref: DRF_MIGRATION_URL_MAP.md:164) | tags: home, volumes | Jira: [RC-29](https://nonameitem.atlassian.net/browse/RC-29)
- Unfinished story arcs — endpoints: /api/story-arcs/started/ [OK (action started)] (ref: DRF_MIGRATION_URL_MAP.md:125) | tags: home, story-arcs | Jira: [RC-30](https://nonameitem.atlassian.net/browse/RC-30)
- Counter cards — endpoints: /api/characters/count/ [OK]; /api/issues/count/ [OK] | tags: home, characters, issues | Jira: [RC-31](https://nonameitem.atlassian.net/browse/RC-31)
- Update history — endpoints: /api/issues/update-history/ [UNKNOWN (not in DRF_MIGRATION_URL_MAP.md)] | tags: home, issues | Jira: [RC-32](https://nonameitem.atlassian.net/browse/RC-32)

## Task: New issues by day ([RC-164](https://nonameitem.atlassian.net/browse/RC-164))
Description: Django URL: `/new_issues/<year>/<month>/<day>/`, template: `core/new_issues.html`
Tags: issues
Subtasks:
- Page data — endpoints: /api/issues/by-date/<year>/<month>/<day>/ [TBD (not in DRF_MIGRATION_URL_MAP.md)] | tags: issues | Jira: [RC-171](https://nonameitem.atlassian.net/browse/RC-171)

## Task: Search page ([RC-162](https://nonameitem.atlassian.net/browse/RC-162))
Description: Django URL: `/search/`, template: `search/search.html`
Tags: search
Subtasks:
- Page data — endpoints: /api/search/ [PLAN] | tags: search | Jira: [RC-162](https://nonameitem.atlassian.net/browse/RC-162)

## Task: Characters list ([RC-4](https://nonameitem.atlassian.net/browse/RC-4))
Description: Django URL: `/characters/`, template: `characters/list.html`
Tags: characters
Subtasks:
- Page data — endpoints: /api/characters/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:23) | tags: characters | Jira: [RC-173](https://nonameitem.atlassian.net/browse/RC-173)

## Task: Concepts list ([RC-2](https://nonameitem.atlassian.net/browse/RC-2))
Description: Django URL: `/concepts/`, template: `concepts/list.html`
Tags: concepts
Subtasks:
- Page data — endpoints: /api/concepts/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:42) | tags: concepts | Jira: [RC-174](https://nonameitem.atlassian.net/browse/RC-174)

## Task: Issues list ([RC-6](https://nonameitem.atlassian.net/browse/RC-6))
Description: Django URL: `/issues/`, template: `issues/list.html`
Tags: issues
Subtasks:
- Page data — endpoints: /api/issues/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:54) | tags: issues | Jira: [RC-175(https://nonameitem.atlassian.net/browse/RC-175)

## Task: Locations list ([RC-9](https://nonameitem.atlassian.net/browse/RC-9))
Description: Django URL: `/locations/`, template: `locations/list.html`
Tags: locations
Subtasks:
- Page data — endpoints: /api/locations/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:72) | tags: locations | Jira: [RC-176](https://nonameitem.atlassian.net/browse/RC-176)

## Task: Objects list ([RC-11](https://nonameitem.atlassian.net/browse/RC-11))
Description: Django URL: `/objects/`, template: `objects/list.html`
Tags: objects
Subtasks:
- Page data — endpoints: /api/objects/ [OK (list)] (ref: DRF_MIGRATION_URL_MAP.md:84) | tags: objects | Jira: [RC-177](https://nonameitem.atlassian.net/browse/RC-177)

## Task: People list ([RC-13](https://nonameitem.atlassian.net/browse/RC-13))
Description: Django URL: `/people/`, template: `people/list.html`
Tags: people
Subtasks:
- Page data — endpoints: /api/people/ [OK (list)] (ref: DRF_MIGRATION_URL_MAP.md:96) | tags: people | Jira: [RC-178](https://nonameitem.atlassian.net/browse/RC-178)

## Task: Publishers list ([RC-15](https://nonameitem.atlassian.net/browse/RC-15))
Description: Django URL: `/publishers/`, template: `publishers/list.html`
Tags: publishers
Subtasks:
- Page data — endpoints: /api/publishers/ [OK (list)] (ref: DRF_MIGRATION_URL_MAP.md:109) | tags: publishers | Jira: [RC-179](https://nonameitem.atlassian.net/browse/RC-179)

## Task: Story arcs list ([RC-17](https://nonameitem.atlassian.net/browse/RC-17))
Description: Django URL: `/story_arcs/`, template: `story_arcs/list.html`
Tags: story-arcs
Subtasks:
- Page data — endpoints: /api/story-arcs/ [OK (list)] (ref: DRF_MIGRATION_URL_MAP.md:124) | tags: story-arcs | Jira: [RC-180](https://nonameitem.atlassian.net/browse/RC-180)

## Task: Teams list ([RC-19](https://nonameitem.atlassian.net/browse/RC-19))
Description: Django URL: `/teams/`, template: `teams/list.html`
Tags: teams
Subtasks:
- Page data — endpoints: /api/teams/ [OK (list)] (ref: DRF_MIGRATION_URL_MAP.md:147) | tags: teams | Jira: [RC-181](https://nonameitem.atlassian.net/browse/RC-181)

## Task: Volumes list ([RC-21](https://nonameitem.atlassian.net/browse/RC-21))
Description: Django URL: `/volumes/`, template: `volumes/list.html`
Tags: volumes
Subtasks:
- Page data — endpoints: /api/volumes/ [OK (list)] (ref: DRF_MIGRATION_URL_MAP.md:163) | tags: volumes | Jira: [RC-182](https://nonameitem.atlassian.net/browse/RC-182)

## Task: Volumes continue reading ([RC-165](https://nonameitem.atlassian.net/browse/RC-165))
Description: Django URL: `/volumes/continue_reading`, template: `volumes/continue_reading.html`
Tags: volumes
Subtasks:
- Page data — endpoints: /api/volumes/started/ [OK (action started)] (ref: DRF_MIGRATION_URL_MAP.md:164) | tags: volumes | Jira: [RC-183](https://nonameitem.atlassian.net/browse/RC-183)

## Task: Story arcs continue reading ([RC-166](https://nonameitem.atlassian.net/browse/RC-166))
Description: Django URL: `/story_arcs/continue_reading`, template: `story_arcs/continue_reading.html`
Tags: story-arcs
Subtasks:
- Page data — endpoints: /api/story-arcs/started/ [OK (action started)] (ref: DRF_MIGRATION_URL_MAP.md:125) | tags: story-arcs | Jira: [RC-184](https://nonameitem.atlassian.net/browse/RC-184)

## Task: Character detail ([RC-5](https://nonameitem.atlassian.net/browse/RC-5))
Description: Django URL: `/characters/<slug>/`, template: `characters/detail.html`
Tags: characters
Subtasks:
- Header + Tab selector — endpoints: /api/characters/<slug>/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:24) | tags: characters | Jira: [RC-198](https://nonameitem.atlassian.net/browse/RC-198)
- Reading progress — endpoints: /api/characters/<slug>/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:24) | tags: characters | Jira: [RC-199](https://nonameitem.atlassian.net/browse/RC-199)
- Main info tab — endpoints: /api/characters/<slug>/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:24) | tags: characters | Jira: [RC-34](https://nonameitem.atlassian.net/browse/RC-34)
- Issues tab — endpoints: /api/characters/<slug>/issues/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:28) | tags: characters, issues | Jira: [RC-36](https://nonameitem.atlassian.net/browse/RC-36)
- Volumes tab — endpoints: /api/characters/<slug>/volumes/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:29) | tags: characters, volumes | Jira: [RC-37](https://nonameitem.atlassian.net/browse/RC-37)
- Died in tab — endpoints: /api/characters/<slug>/died-in-issues/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:30) | tags: characters | Jira: [RC-39](https://nonameitem.atlassian.net/browse/RC-39)
- Authors tab — endpoints: /api/characters/<slug>/authors/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:36) | tags: characters | Jira: [RC-38](https://nonameitem.atlassian.net/browse/RC-38)
- Friends tab — endpoints: /api/characters/<slug>/friends/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:32) | tags: characters | Jira: [RC-40](https://nonameitem.atlassian.net/browse/RC-40)
- Enemies tab — endpoints: /api/characters/<slug>/enemies/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:31) | tags: characters | Jira: [RC-41](https://nonameitem.atlassian.net/browse/RC-41)
- Teams tab — endpoints: /api/characters/<slug>/teams/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:33) | tags: characters, teams | Jira: [RC-42](https://nonameitem.atlassian.net/browse/RC-42)
- Team friends tab — endpoints: /api/characters/<slug>/team-friends/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:34) | tags: characters | Jira: [RC-43](https://nonameitem.atlassian.net/browse/RC-43)
- Team enemies tab — endpoints: /api/characters/<slug>/team-enemies/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:35) | tags: characters | Jira: [RC-44](https://nonameitem.atlassian.net/browse/RC-44)
- Missing issues link (staff) — endpoints: no DRF endpoint (staff-only link) [N/A] | tags: characters, missing-issues | Jira: [RC-53](https://nonameitem.atlassian.net/browse/RC-53)
- Technical info tab — endpoints: /api/characters/<slug>/technical-info/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:25) | tags: characters | Jira: [RC-35](https://nonameitem.atlassian.net/browse/RC-35)
- Start/stop watch — endpoints: /api/characters/<slug>/start-watch/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:26); /api/characters/<slug>/stop-watch/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:27) | tags: characters | Jira: [RC-52](https://nonameitem.atlassian.net/browse/RC-52)
- Download — endpoints: Django only [N/A] | tags: characters | Jira: [RC-51](https://nonameitem.atlassian.net/browse/RC-51)

## Task: Concept detail ([RC-3](https://nonameitem.atlassian.net/browse/RC-3))
Description: Django URL: `/concepts/<slug>/`, template: `concepts/detail.html`
Tags: concepts
Subtasks:
- Header + Tab selector — endpoints: /api/concepts/<slug>/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:43) | tags: concepts | Jira: [RC-200](https://nonameitem.atlassian.net/browse/RC-200)
- Reading progress — endpoints: /api/concepts/<slug>/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:43) | tags: concepts | Jira: [RC-201](https://nonameitem.atlassian.net/browse/RC-201)
- Main info tab — endpoints: /api/concepts/<slug>/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:43) | tags: concepts | Jira: [RC-33](https://nonameitem.atlassian.net/browse/RC-33)
- Issues tab — endpoints: /api/concepts/<slug>/issues/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:47) | tags: concepts, issues | Jira: [RC-46](https://nonameitem.atlassian.net/browse/RC-46)
- Volumes tab — endpoints: /api/concepts/<slug>/volumes/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:48) | tags: concepts, volumes | Jira: [RC-47](https://nonameitem.atlassian.net/browse/RC-47)
- Missing issues link (staff) — endpoints: no DRF endpoint (staff-only link) [N/A] | tags: concepts, missing-issues | Jira: [RC-50](https://nonameitem.atlassian.net/browse/RC-50)
- Technical info tab — endpoints: /api/concepts/<slug>/technical-info/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:44) | tags: concepts | Jira: [RC-45](https://nonameitem.atlassian.net/browse/RC-45)
- Start/stop watch — endpoints: /api/concepts/<slug>/start-watch/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:45); /api/concepts/<slug>/stop-watch/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:46) | tags: concepts | Jira: [RC-49](https://nonameitem.atlassian.net/browse/RC-49)
- Download — endpoints: Django only [N/A] | tags: concepts | Jira: [RC-48](https://nonameitem.atlassian.net/browse/RC-48)

## Task: Issue detail ([RC-7](https://nonameitem.atlassian.net/browse/RC-7))
Description: Django URL: `/issues/<slug>/`, template: `issues/detail.html`
Tags: issues
Subtasks:
- Header + Tab selector — endpoints: /api/issues/<slug>/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:55) | tags: issues | Jira: [RC-225](https://nonameitem.atlassian.net/browse/RC-225)
- Reading progress (volume) — endpoints: /api/volumes/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:165) | tags: issues, volumes | Jira: [RC-226](https://nonameitem.atlassian.net/browse/RC-226)
- Main info tab — endpoints: /api/issues/<slug>/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:55) | tags: issues | Jira: [RC-54](https://nonameitem.atlassian.net/browse/RC-54)
- Characters tab — endpoints: /api/issues/<slug>/characters/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:58) | tags: characters, issues | Jira: [RC-56](https://nonameitem.atlassian.net/browse/RC-56)
- Characters died tab — endpoints: /api/issues/<slug>/characters-died/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:59) | tags: characters, issues | Jira: [RC-59](https://nonameitem.atlassian.net/browse/RC-59)
- Concepts tab — endpoints: /api/issues/<slug>/concepts/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:60) | tags: concepts, issues | Jira: [RC-60](https://nonameitem.atlassian.net/browse/RC-60)
- Locations tab — endpoints: /api/issues/<slug>/locations/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:61) | tags: issues, locations | Jira: [RC-61](https://nonameitem.atlassian.net/browse/RC-61)
- Objects tab — endpoints: /api/issues/<slug>/objects/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:62) | tags: issues, objects | Jira: [RC-62](https://nonameitem.atlassian.net/browse/RC-62)
- Authors tab — endpoints: /api/issues/<slug>/authors/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:63) | tags: issues | Jira: [RC-57](https://nonameitem.atlassian.net/browse/RC-57)
- Story arcs tab — endpoints: /api/issues/<slug>/story-arcs/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:64) | tags: issues, story-arcs | Jira: [RC-63](https://nonameitem.atlassian.net/browse/RC-63)
- Teams tab — endpoints: /api/issues/<slug>/teams/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:65) | tags: issues, teams | Jira: [RC-64](https://nonameitem.atlassian.net/browse/RC-64)
- Disbanded teams tab — endpoints: /api/issues/<slug>/disbanded-teams/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:66) | tags: issues, teams | Jira: [RC-65](https://nonameitem.atlassian.net/browse/RC-65)
- First appearances tab — endpoints: /api/issues/<slug>/first-appearances/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:67) | tags: issues | Jira: [RC-58](https://nonameitem.atlassian.net/browse/RC-58)
- Technical info tab — endpoints: /api/issues/<slug>/technical-info/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:56) | tags: issues | Jira: [RC-55](https://nonameitem.atlassian.net/browse/RC-55)
- Download — endpoints: Django only [N/A] | tags: issues | Jira: [RC-68](https://nonameitem.atlassian.net/browse/RC-68)
- Mark read — endpoints: /api/issues/<slug>/mark-read/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:57) | tags: issues | Jira: [RC-71](https://nonameitem.atlassian.net/browse/RC-71)
- Previous/Next — endpoints: /api/issues/<slug>/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:55) | tags: issues | Jira: [RC-69](https://nonameitem.atlassian.net/browse/RC-69)

## Task: Character Issue detail ([RC-153](https://nonameitem.atlassian.net/browse/RC-153))
Description: Django URL: `/characters/<slug>/issues/<issue_slug>/`, template: `issues/detail.html`
Tags: characters, issues
Subtasks:
- Reading progress (volume + character) — endpoints: /api/volumes/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:165); /api/characters/<slug>/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:24) | tags: characters, issues, volumes | Jira: [RC-228](https://nonameitem.atlassian.net/browse/RC-228)
- Previous/Next (within sublist) — endpoints: /api/characters/<slug>/issues/<issue_slug>/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:37) | tags: characters, issues | Jira: [RC-229](https://nonameitem.atlassian.net/browse/RC-229)

## Task: Concept Issue detail ([RC-154](https://nonameitem.atlassian.net/browse/RC-154))
Description: Django URL: `/concepts/<slug>/issues/<issue_slug>/`, template: `issues/detail.html`
Tags: concepts, issues
Subtasks:
- Reading progress (volume + concept) — endpoints: /api/volumes/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:165); /api/concepts/<slug>/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:43) | tags: concepts, issues, volumes | Jira: [RC-230](https://nonameitem.atlassian.net/browse/RC-230)
- Previous/Next (within sublist) — endpoints: /api/concepts/<slug>/issues/<issue_slug>/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:49) | tags: concepts, issues | Jira: [RC-231](https://nonameitem.atlassian.net/browse/RC-231)

## Task: Location Issue detail ([RC-155](https://nonameitem.atlassian.net/browse/RC-155))
Description: Django URL: `/locations/<slug>/issues/<issue_slug>/`, template: `issues/detail.html`
Tags: issues, locations
Subtasks:
- Reading progress (volume + location) — endpoints: /api/volumes/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:165); /api/locations/<slug>/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:73) | tags: issues, locations, volumes | Jira: [RC-232](https://nonameitem.atlassian.net/browse/RC-232)
- Previous/Next (within sublist) — endpoints: /api/locations/<slug>/issues/<issue_slug>/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:79) | tags: issues, locations | Jira: [RC-233](https://nonameitem.atlassian.net/browse/RC-233)

## Task: Object Issue detail ([RC-156](https://nonameitem.atlassian.net/browse/RC-156))
Description: Django URL: `/objects/<slug>/issues/<issue_slug>/`, template: `issues/detail.html`
Tags: issues, objects
Subtasks:
- Reading progress (volume + object) — endpoints: /api/volumes/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:165); /api/objects/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:85) | tags: issues, objects, volumes | Jira: [RC-234](https://nonameitem.atlassian.net/browse/RC-234)
- Previous/Next (within sublist) — endpoints: /api/objects/<slug>/issues/<issue_slug>/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:91) | tags: issues, objects | Jira: [RC-235](https://nonameitem.atlassian.net/browse/RC-235)

## Task: Person Issue detail ([RC-157](https://nonameitem.atlassian.net/browse/RC-157))
Description: Django URL: `/people/<slug>/issues/<issue_slug>/`, template: `issues/detail.html`
Tags: issues, people
Subtasks:
- Reading progress (volume + person) — endpoints: /api/volumes/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:165); /api/people/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:97) | tags: issues, people, volumes | Jira: [RC-236](https://nonameitem.atlassian.net/browse/RC-236)
- Previous/Next (within sublist) — endpoints: /api/people/<slug>/issues/<issue_slug>/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:104) | tags: issues, people | Jira: [RC-237](https://nonameitem.atlassian.net/browse/RC-237)

## Task: Publisher Issue detail ([RC-158](https://nonameitem.atlassian.net/browse/RC-158))
Description: Django URL: `/publishers/<slug>/issues/<issue_slug>/`, template: `issues/detail.html`
Tags: issues, publishers
Subtasks:
- Reading progress (volume + publisher) — endpoints: /api/volumes/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:165); /api/publishers/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:110) | tags: issues, publishers, volumes | Jira: [RC-238](https://nonameitem.atlassian.net/browse/RC-238)
- Previous/Next (within sublist) — endpoints: /api/publishers/<slug>/issues/<issue_slug>/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:119) | tags: issues, publishers | Jira: [RC-239](https://nonameitem.atlassian.net/browse/RC-239)

## Task: Story Arc Issue detail ([RC-159](https://nonameitem.atlassian.net/browse/RC-159))
Description: Django URL: `/story_arcs/<slug>/issues/<issue_slug>/`, template: `issues/detail.html`
Tags: issues, story-arcs
Subtasks:
- Reading progress (volume + story arc) — endpoints: /api/volumes/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:165); /api/story-arcs/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:126) | tags: issues, story-arcs, volumes | Jira: [RC-240](https://nonameitem.atlassian.net/browse/RC-240)
- Previous/Next (within sublist) — endpoints: /api/story-arcs/<slug>/issues/<issue_slug>/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:137) | tags: issues, story-arcs | Jira: [RC-241](https://nonameitem.atlassian.net/browse/RC-241)

## Task: Team Issue detail ([RC-160](https://nonameitem.atlassian.net/browse/RC-160))
Description: Django URL: `/teams/<slug>/issues/<issue_slug>/`, template: `issues/detail.html`
Tags: issues, teams
Subtasks:
- Reading progress (volume + team) — endpoints: /api/volumes/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:165); /api/teams/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:148) | tags: issues, teams, volumes | Jira: [RC-242](https://nonameitem.atlassian.net/browse/RC-242)
- Previous/Next (within sublist) — endpoints: /api/teams/<slug>/issues/<issue_slug>/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:152) | tags: issues, teams | Jira: [RC-243](https://nonameitem.atlassian.net/browse/RC-243)

## Task: Volume Issue detail ([RC-161](https://nonameitem.atlassian.net/browse/RC-161))
Description: Django URL: `/volumes/<slug>/issues/<issue_slug>/`, template: `issues/detail.html`
Tags: issues, volumes
Subtasks:
- Reading progress (volume + volume) — endpoints: /api/volumes/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:165) | tags: issues, volumes | Jira: [RC-244](https://nonameitem.atlassian.net/browse/RC-244)
- Previous/Next (within sublist) — endpoints: /api/volumes/<slug>/issues/<issue_slug>/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:182) | tags: issues, volumes | Jira: [RC-245](https://nonameitem.atlassian.net/browse/RC-245)

## Task: Location detail ([RC-10](https://nonameitem.atlassian.net/browse/RC-10))
Description: Django URL: `/locations/<slug>/`, template: `locations/detail.html`
Tags: locations
Subtasks:
- Header + Tab selector — endpoints: /api/locations/<slug>/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:73) | tags: locations | Jira: [RC-202](https://nonameitem.atlassian.net/browse/RC-202)
- Reading progress — endpoints: /api/locations/<slug>/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:73) | tags: locations | Jira: [RC-203](https://nonameitem.atlassian.net/browse/RC-203)
- Main info tab — endpoints: /api/locations/<slug>/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:73) | tags: locations | Jira: [RC-72](https://nonameitem.atlassian.net/browse/RC-72)
- Issues tab — endpoints: /api/locations/<slug>/issues/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:77) | tags: issues, locations | Jira: [RC-74](https://nonameitem.atlassian.net/browse/RC-74)
- Volumes tab — endpoints: /api/locations/<slug>/volumes/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:78) | tags: locations, volumes | Jira: [RC-75](https://nonameitem.atlassian.net/browse/RC-75)
- Missing issues link (staff) — endpoints: no DRF endpoint (staff-only link) [N/A] | tags: locations, missing-issues | Jira: [RC-78](https://nonameitem.atlassian.net/browse/RC-78)
- Technical info tab — endpoints: /api/locations/<slug>/technical-info/ [OK] (ref: DRF_MIGRATION_URL_MAP.md:74) | tags: locations | Jira: [RC-73](https://nonameitem.atlassian.net/browse/RC-73)
- Start/stop watch — endpoints: /api/locations/<slug>/start-watch/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:75); /api/locations/<slug>/stop-watch/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:76) | tags: locations | Jira: [RC-77](https://nonameitem.atlassian.net/browse/RC-77)
- Download — endpoints: Django only [N/A] | tags: locations | Jira: [RC-76](https://nonameitem.atlassian.net/browse/RC-76)

## Task: Object detail ([RC-12](https://nonameitem.atlassian.net/browse/RC-12))
Description: Django URL: `/objects/<slug>/`, template: `objects/detail.html`
Tags: objects
Subtasks:
- Header + Tab selector — endpoints: /api/objects/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:85) | tags: objects | Jira: [RC-204](https://nonameitem.atlassian.net/browse/RC-204)
- Reading progress — endpoints: /api/objects/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:85) | tags: objects | Jira: [RC-205](https://nonameitem.atlassian.net/browse/RC-205)
- Main info tab — endpoints: /api/objects/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:85) | tags: objects | Jira: [RC-79](https://nonameitem.atlassian.net/browse/RC-79)
- Issues tab — endpoints: /api/objects/<slug>/issues/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:89) | tags: issues, objects | Jira: [RC-81](https://nonameitem.atlassian.net/browse/RC-81)
- Volumes tab — endpoints: /api/objects/<slug>/volumes/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:90) | tags: objects, volumes | Jira: [RC-82](https://nonameitem.atlassian.net/browse/RC-82)
- Missing issues link (staff) — endpoints: no DRF endpoint (staff-only link) [N/A] | tags: objects, missing-issues | Jira: [RC-206](https://nonameitem.atlassian.net/browse/RC-206)
- Technical info tab — endpoints: /api/objects/<slug>/technical-info/ [PLAN (plus detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:86) | tags: objects | Jira: [RC-80](https://nonameitem.atlassian.net/browse/RC-80)
- Start/stop watch — endpoints: /api/objects/<slug>/start-watch/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:87); /api/objects/<slug>/stop-watch/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:88) | tags: objects | Jira: [RC-83](https://nonameitem.atlassian.net/browse/RC-83)
- Download — endpoints: Django only [N/A] | tags: objects | Jira: [RC-84](https://nonameitem.atlassian.net/browse/RC-84)

## Task: Person detail ([RC-14](https://nonameitem.atlassian.net/browse/RC-14))
Description: Django URL: `/people/<slug>/`, template: `people/detail.html`
Tags: people
Subtasks:
- Header + Tab selector — endpoints: /api/people/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:97) | tags: people | Jira: [RC-207](https://nonameitem.atlassian.net/browse/RC-207)
- Reading progress — endpoints: /api/people/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:97) | tags: people | Jira: [RC-208](https://nonameitem.atlassian.net/browse/RC-208)
- Main info tab — endpoints: /api/people/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:97) | tags: people | Jira: [RC-85](https://nonameitem.atlassian.net/browse/RC-85)
- Issues tab — endpoints: /api/people/<slug>/issues/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:101) | tags: issues, people | Jira: [RC-87](https://nonameitem.atlassian.net/browse/RC-87)
- Volumes tab — endpoints: /api/people/<slug>/volumes/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:102) | tags: people, volumes | Jira: [RC-88](https://nonameitem.atlassian.net/browse/RC-88)
- Characters tab — endpoints: /api/people/<slug>/characters/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:103) | tags: characters, people | Jira: [RC-89](https://nonameitem.atlassian.net/browse/RC-89)
- Missing issues link (staff) — endpoints: no DRF endpoint (staff-only link) [N/A] | tags: people, missing-issues | Jira: [RC-209](https://nonameitem.atlassian.net/browse/RC-209)
- Technical info tab — endpoints: /api/people/<slug>/technical-info/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:98) | tags: people | Jira: [RC-86](https://nonameitem.atlassian.net/browse/RC-86)
- Start/stop watch — endpoints: /api/people/<slug>/start-watch/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:99); /api/people/<slug>/stop-watch/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:100) | tags: people | Jira: [RC-91](https://nonameitem.atlassian.net/browse/RC-91)
- Download — endpoints: Django only [N/A] | tags: people | Jira: [RC-90](https://nonameitem.atlassian.net/browse/RC-90)

## Task: Publisher detail ([RC-16](https://nonameitem.atlassian.net/browse/RC-16))
Description: Django URL: `/publishers/<slug>/`, template: `publishers/detail.html`
Tags: publishers
Subtasks:
- Header + Tab selector — endpoints: /api/publishers/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:110) | tags: publishers | Jira: [RC-210](https://nonameitem.atlassian.net/browse/RC-210)
- Reading progress — endpoints: /api/publishers/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:110) | tags: publishers | Jira: [RC-211](https://nonameitem.atlassian.net/browse/RC-211)
- Main info tab — endpoints: /api/publishers/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:110) | tags: publishers | Jira: [RC-92](https://nonameitem.atlassian.net/browse/RC-92)
- Issues tab — endpoints: /api/publishers/<slug>/issues/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:114) | tags: issues, publishers | Jira: [RC-94](https://nonameitem.atlassian.net/browse/RC-94)
- Volumes tab — endpoints: /api/publishers/<slug>/volumes/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:118) | tags: publishers, volumes | Jira: [RC-95](https://nonameitem.atlassian.net/browse/RC-95)
- Characters tab — endpoints: /api/publishers/<slug>/characters/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:115) | tags: characters, publishers | Jira: [RC-96](https://nonameitem.atlassian.net/browse/RC-96)
- Story arcs tab — endpoints: /api/publishers/<slug>/story-arcs/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:117) | tags: publishers, story-arcs | Jira: [RC-97](https://nonameitem.atlassian.net/browse/RC-97)
- Teams tab — endpoints: /api/publishers/<slug>/teams/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:116) | tags: publishers, teams | Jira: [RC-98](https://nonameitem.atlassian.net/browse/RC-98)
- Missing issues link (staff) — endpoints: no DRF endpoint (staff-only link) [N/A] | tags: publishers, missing-issues | Jira: [RC-212](https://nonameitem.atlassian.net/browse/RC-212)
- Technical info tab — endpoints: /api/publishers/<slug>/technical-info/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:111) | tags: publishers | Jira: [RC-93](https://nonameitem.atlassian.net/browse/RC-93)
- Start/stop watch — endpoints: /api/publishers/<slug>/start-watch/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:112); /api/publishers/<slug>/stop-watch/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:113) | tags: publishers | Jira: [RC-100](https://nonameitem.atlassian.net/browse/RC-100)
- Download — endpoints: Django only [N/A] | tags: publishers | Jira: [RC-99](https://nonameitem.atlassian.net/browse/RC-99)

## Task: Story arc detail ([RC-18](https://nonameitem.atlassian.net/browse/RC-18))
Description: Django URL: `/story_arcs/<slug>/`, template: `story_arcs/detail.html`
Tags: story-arcs
Subtasks:
- Header + Tab selector — endpoints: /api/story-arcs/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:126) | tags: story-arcs | Jira: [RC-213](https://nonameitem.atlassian.net/browse/RC-213)
- Reading progress — endpoints: /api/story-arcs/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:126) | tags: story-arcs | Jira: [RC-214](https://nonameitem.atlassian.net/browse/RC-214)
- Main info tab — endpoints: /api/story-arcs/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:126) | tags: story-arcs | Jira: [RC-101](https://nonameitem.atlassian.net/browse/RC-101)
- Issues tab — endpoints: /api/story-arcs/<slug>/issues/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:139) | tags: issues, story-arcs | Jira: [RC-103](https://nonameitem.atlassian.net/browse/RC-103)
- Volumes tab — endpoints: /api/story-arcs/<slug>/volumes/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:142) | tags: story-arcs, volumes | Jira: [RC-104](https://nonameitem.atlassian.net/browse/RC-104)
- Characters tab — endpoints: /api/story-arcs/<slug>/characters/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:133) | tags: characters, story-arcs | Jira: [RC-106](https://nonameitem.atlassian.net/browse/RC-106)
- Died tab — endpoints: /api/story-arcs/<slug>/died/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:131) | tags: story-arcs, characters | Jira: [RC-107](https://nonameitem.atlassian.net/browse/RC-107)
- Concepts tab — endpoints: /api/story-arcs/<slug>/concepts/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:134) | tags: concepts, story-arcs | Jira: [RC-108](https://nonameitem.atlassian.net/browse/RC-108)
- Locations tab — endpoints: /api/story-arcs/<slug>/locations/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:138) | tags: locations, story-arcs | Jira: [RC-109](https://nonameitem.atlassian.net/browse/RC-109)
- Objects tab — endpoints: /api/story-arcs/<slug>/objects/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:140) | tags: objects, story-arcs | Jira: [RC-110](https://nonameitem.atlassian.net/browse/RC-110)
- Authors tab — endpoints: /api/story-arcs/<slug>/authors/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:132) | tags: story-arcs | Jira: [RC-111](https://nonameitem.atlassian.net/browse/RC-111)
- Teams tab — endpoints: /api/story-arcs/<slug>/teams/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:141) | tags: story-arcs, teams | Jira: [RC-112](https://nonameitem.atlassian.net/browse/RC-112)
- Disbanded tab — endpoints: /api/story-arcs/<slug>/disbanded/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:135) | tags: story-arcs, teams | Jira: [RC-113](https://nonameitem.atlassian.net/browse/RC-113)
- First appearances tab — endpoints: /api/story-arcs/<slug>/first-appearances/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:136) | tags: story-arcs | Jira: [RC-105](https://nonameitem.atlassian.net/browse/RC-105)
- Missing issues link (staff) — endpoints: no DRF endpoint (staff-only link) [N/A] | tags: story-arcs, missing-issues | Jira: [RC-215](https://nonameitem.atlassian.net/browse/RC-215)
- Technical info tab — endpoints: /api/story-arcs/<slug>/technical-info/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:127) | tags: story-arcs | Jira: [RC-102](https://nonameitem.atlassian.net/browse/RC-102)
- Start/stop watch — endpoints: /api/story-arcs/<slug>/start-watch/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:128); /api/story-arcs/<slug>/stop-watch/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:129) | tags: story-arcs | Jira: [RC-116](https://nonameitem.atlassian.net/browse/RC-116)
- Mark finished — endpoints: /api/story-arcs/<slug>/mark-finished/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:130) | tags: story-arcs | Jira: [RC-114](https://nonameitem.atlassian.net/browse/RC-114)
- Download — endpoints: Django only [N/A] | tags: story-arcs | Jira: [RC-115](https://nonameitem.atlassian.net/browse/RC-115)

## Task: Team detail ([RC-20](https://nonameitem.atlassian.net/browse/RC-20))
Description: Django URL: `/teams/<slug>/`, template: `teams/detail.html`
Tags: teams
Subtasks:
- Header + Tab selector — endpoints: /api/teams/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:148) | tags: teams | Jira: [RC-216](https://nonameitem.atlassian.net/browse/RC-216)
- Reading progress — endpoints: /api/teams/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:148) | tags: teams | Jira: [RC-217](https://nonameitem.atlassian.net/browse/RC-217)
- Main info tab — endpoints: /api/teams/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:148) | tags: teams | Jira: [RC-119](https://nonameitem.atlassian.net/browse/RC-119)
- Issues tab — endpoints: /api/teams/<slug>/issues/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:153) | tags: issues, teams | Jira: [RC-121](https://nonameitem.atlassian.net/browse/RC-121)
- Volumes tab — endpoints: /api/teams/<slug>/volumes/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:155) | tags: teams, volumes | Jira: [RC-122](https://nonameitem.atlassian.net/browse/RC-122)
- Disbanded in issues tab — endpoints: /api/teams/<slug>/disbanded-in/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:158) | tags: teams | Jira: [RC-126](https://nonameitem.atlassian.net/browse/RC-126)
- Members tab — endpoints: /api/teams/<slug>/characters/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:157) | tags: characters, teams | Jira: [RC-123](https://nonameitem.atlassian.net/browse/RC-123)
- Friends tab — endpoints: /api/teams/<slug>/friends/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:156) | tags: teams | Jira: [RC-125](https://nonameitem.atlassian.net/browse/RC-125)
- Enemies tab — endpoints: /api/teams/<slug>/enemies/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:154) | tags: teams | Jira: [RC-124](https://nonameitem.atlassian.net/browse/RC-124)
- Missing issues link (staff) — endpoints: no DRF endpoint (staff-only link) [N/A] | tags: teams, missing-issues | Jira: [RC-218](https://nonameitem.atlassian.net/browse/RC-218)
- Technical info tab — endpoints: /api/teams/<slug>/technical-info/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:149) | tags: teams | Jira: [RC-120](https://nonameitem.atlassian.net/browse/RC-120)
- Start/stop watch — endpoints: /api/teams/<slug>/start-watch/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:150); /api/teams/<slug>/stop-watch/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:151) | tags: teams | Jira: [RC-128](https://nonameitem.atlassian.net/browse/RC-128)
- Download — endpoints: Django only [N/A] | tags: teams | Jira: [RC-127](https://nonameitem.atlassian.net/browse/RC-127)

## Task: Volume detail ([RC-22](https://nonameitem.atlassian.net/browse/RC-22))
Description: Django URL: `/volumes/<slug>/`, template: `volumes/detail.html`
Tags: volumes
Subtasks:
- Header + Tab selector — endpoints: /api/volumes/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:165) | tags: volumes | Jira: [RC-219](https://nonameitem.atlassian.net/browse/RC-219)
- Reading progress — endpoints: /api/volumes/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:165) | tags: volumes | Jira: [RC-220](https://nonameitem.atlassian.net/browse/RC-220)
- Main info tab — endpoints: /api/volumes/<slug>/ [NEEDS WORK (detail serializer); slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:165) | tags: volumes | Jira: [RC-221](https://nonameitem.atlassian.net/browse/RC-221)
- Issues tab — endpoints: /api/volumes/<slug>/issues/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:171) | tags: issues, volumes | Jira: [RC-129](https://nonameitem.atlassian.net/browse/RC-129)
- Characters tab — endpoints: /api/volumes/<slug>/characters/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:172) | tags: characters, volumes | Jira: [RC-131](https://nonameitem.atlassian.net/browse/RC-131)
- Characters died tab — endpoints: /api/volumes/<slug>/died/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:173) | tags: characters, volumes | Jira: [RC-132](https://nonameitem.atlassian.net/browse/RC-132)
- Concepts tab — endpoints: /api/volumes/<slug>/concepts/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:174) | tags: concepts, volumes | Jira: [RC-133](https://nonameitem.atlassian.net/browse/RC-133)
- Locations tab — endpoints: /api/volumes/<slug>/locations/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:175) | tags: locations, volumes | Jira: [RC-134](https://nonameitem.atlassian.net/browse/RC-134)
- Objects tab — endpoints: /api/volumes/<slug>/objects/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:176) | tags: objects, volumes | Jira: [RC-135](https://nonameitem.atlassian.net/browse/RC-135)
- Authors tab — endpoints: /api/volumes/<slug>/authors/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:177) | tags: volumes | Jira: [RC-136](https://nonameitem.atlassian.net/browse/RC-136)
- Story arcs tab — endpoints: /api/volumes/<slug>/story-arcs/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:178) | tags: story-arcs, volumes | Jira: [RC-137](https://nonameitem.atlassian.net/browse/RC-137)
- Teams tab — endpoints: /api/volumes/<slug>/teams/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:179) | tags: teams, volumes | Jira: [RC-138](https://nonameitem.atlassian.net/browse/RC-138)
- Disbanded tab — endpoints: /api/volumes/<slug>/disbanded/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:180) | tags: volumes | Jira: [RC-139](https://nonameitem.atlassian.net/browse/RC-139)
- First appearances tab — endpoints: /api/volumes/<slug>/first-appearances/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:181) | tags: volumes | Jira: [RC-130](https://nonameitem.atlassian.net/browse/RC-130)
- Missing issues link (staff) — endpoints: no DRF endpoint (staff-only link) [N/A] | tags: volumes, missing-issues | Jira: [RC-223](https://nonameitem.atlassian.net/browse/RC-223)
- Technical info tab — endpoints: /api/volumes/<slug>/technical-info/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:166) | tags: volumes | Jira: [RC-222](https://nonameitem.atlassian.net/browse/RC-222)
- Start/stop watch — endpoints: /api/volumes/<slug>/start-watch/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:168); /api/volumes/<slug>/stop-watch/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:169) | tags: volumes | Jira: [RC-142](https://nonameitem.atlassian.net/browse/RC-142)
- Mark finished — endpoints: /api/volumes/<slug>/mark-finished/ [PLAN; slug lookup pending (currently pk)] (ref: DRF_MIGRATION_URL_MAP.md:170) | tags: volumes | Jira: [RC-224](https://nonameitem.atlassian.net/browse/RC-224)
- Download — endpoints: Django only [N/A] | tags: volumes | Jira: [RC-140](https://nonameitem.atlassian.net/browse/RC-140)

## Task: Missing issues list ([RC-23](https://nonameitem.atlassian.net/browse/RC-23))
Description: Django URL: `/missing_issues/`, template: `missing_issues/missing_issues_list.html`
Tags: missing-issues
Subtasks:
- Purge deleted — endpoints: /api/missing-issues/purge-deleted/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:189) | tags: missing-issues | Jira: [RC-246](https://nonameitem.atlassian.net/browse/RC-246)
- Issues table — endpoints: /api/missing-issues/ [NOT READY (no serializer_class)] (ref: DRF_MIGRATION_URL_MAP.md:187) | tags: missing-issues | Jira: [RC-185](https://nonameitem.atlassian.net/browse/RC-185)
- DO Reload modal (tree + confirm) — endpoints: /api/missing-issues/reload-from-do/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:202) | tags: missing-issues | Jira: [RC-247](https://nonameitem.atlassian.net/browse/RC-247)
- Skip publisher — endpoints: /api/missing-issues/skip-publisher/<comicvine_id>/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:198) | tags: missing-issues | Jira: [RC-248](https://nonameitem.atlassian.net/browse/RC-248)
- Ignore publisher — endpoints: /api/missing-issues/ignore-publisher/<comicvine_id>/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:201) | tags: missing-issues | Jira: [RC-249](https://nonameitem.atlassian.net/browse/RC-249)
- Skip volume — endpoints: /api/missing-issues/skip-volume/<comicvine_id>/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:197) | tags: missing-issues | Jira: [RC-250](https://nonameitem.atlassian.net/browse/RC-250)
- Ignore volume — endpoints: /api/missing-issues/ignore-volume/<comicvine_id>/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:200) | tags: missing-issues | Jira: [RC-251](https://nonameitem.atlassian.net/browse/RC-251)
- Skip issue — endpoints: /api/missing-issues/skip-issue/<comicvine_id>/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:196) | tags: missing-issues | Jira: [RC-252](https://nonameitem.atlassian.net/browse/RC-252)
- Ignore issue — endpoints: /api/missing-issues/ignore-issue/<comicvine_id>/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:199) | tags: missing-issues | Jira: [RC-253](https://nonameitem.atlassian.net/browse/RC-253)

## Task: Character missing issues list ([RC-144](https://nonameitem.atlassian.net/browse/RC-144))
Description: Django URL: `/missing_issues/character/<slug>/`, template: `missing_issues/missing_issues_list.html`
Tags: characters, missing-issues
Subtasks:
- Page data — endpoints: /api/characters/<slug>/missing-issues/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:210) | tags: characters, missing-issues | Jira: [RC-186](https://nonameitem.atlassian.net/browse/RC-186)

## Task: Concept missing issues list ([RC-145](https://nonameitem.atlassian.net/browse/RC-145))
Description: Django URL: `/missing_issues/concept/<slug>/`, template: `missing_issues/missing_issues_list.html`
Tags: concepts, missing-issues
Subtasks:
- Page data — endpoints: /api/concepts/<slug>/missing-issues/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:210) | tags: concepts, missing-issues | Jira: [RC-187](https://nonameitem.atlassian.net/browse/RC-187)

## Task: Location missing issues list ([RC-146](https://nonameitem.atlassian.net/browse/RC-146))
Description: Django URL: `/missing_issues/location/<slug>/`, template: `missing_issues/missing_issues_list.html`
Tags: locations, missing-issues
Subtasks:
- Page data — endpoints: /api/locations/<slug>/missing-issues/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:210) | tags: locations, missing-issues | Jira: [RC-188](https://nonameitem.atlassian.net/browse/RC-188)

## Task: Object missing issues list ([RC-147](https://nonameitem.atlassian.net/browse/RC-147))
Description: Django URL: `/missing_issues/object/<slug>/`, template: `missing_issues/missing_issues_list.html`
Tags: objects, missing-issues
Subtasks:
- Page data — endpoints: /api/objects/<slug>/missing-issues/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:210) | tags: objects, missing-issues | Jira: [RC-189](https://nonameitem.atlassian.net/browse/RC-189)

## Task: Person missing issues list ([RC-148](https://nonameitem.atlassian.net/browse/RC-148))
Description: Django URL: `/missing_issues/person/<slug>/`, template: `missing_issues/missing_issues_list.html`
Tags: people, missing-issues
Subtasks:
- Page data — endpoints: /api/people/<slug>/missing-issues/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:210) | tags: people, missing-issues | Jira: [RC-190](https://nonameitem.atlassian.net/browse/RC-190)

## Task: Publisher missing issues list ([RC-149](https://nonameitem.atlassian.net/browse/RC-149))
Description: Django URL: `/missing_issues/publisher/<slug>/`, template: `missing_issues/missing_issues_list.html`
Tags: publishers, missing-issues
Subtasks:
- Page data — endpoints: /api/publishers/<slug>/missing-issues/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:210) | tags: publishers, missing-issues | Jira: [RC-191](https://nonameitem.atlassian.net/browse/RC-191)

## Task: Story arc missing issues list ([RC-150](https://nonameitem.atlassian.net/browse/RC-150))
Description: Django URL: `/missing_issues/story_arc/<slug>/`, template: `missing_issues/missing_issues_list.html`
Tags: story-arcs, missing-issues
Subtasks:
- Page data — endpoints: /api/story-arcs/<slug>/missing-issues/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:210) | tags: story-arcs, missing-issues | Jira: [RC-192](https://nonameitem.atlassian.net/browse/RC-192)

## Task: Team missing issues list ([RC-151](https://nonameitem.atlassian.net/browse/RC-151))
Description: Django URL: `/missing_issues/team/<slug>/`, template: `missing_issues/missing_issues_list.html`
Tags: teams, missing-issues
Subtasks:
- Page data — endpoints: /api/teams/<slug>/missing-issues/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:210) | tags: teams, missing-issues | Jira: [RC-193](https://nonameitem.atlassian.net/browse/RC-193)

## Task: Volume missing issues list ([RC-152](https://nonameitem.atlassian.net/browse/RC-152))
Description: Django URL: `/missing_issues/volume/<slug>/`, template: `missing_issues/missing_issues_list.html`
Tags: volumes, missing-issues
Subtasks:
- Page data — endpoints: /api/volumes/<slug>/missing-issues/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:210) | tags: volumes, missing-issues | Jira: [RC-194](https://nonameitem.atlassian.net/browse/RC-194)

## Task: Ignored issues list ([RC-24](https://nonameitem.atlassian.net/browse/RC-24))
Description: Django URL: `/missing_issues/ignored_issues/`, template: `missing_issues/ignored_issues_list.html`
Tags: missing-issues
Subtasks:
- Table of ignored issues — endpoints: /api/missing-issues/ignored-issues/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:190) | tags: missing-issues | Jira: [RC-195](https://nonameitem.atlassian.net/browse/RC-195)
- Delete ignored issue — endpoints: /api/missing-issues/ignored-issues/<pk>/delete/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:193) | tags: missing-issues | Jira: [RC-254](https://nonameitem.atlassian.net/browse/RC-254)

## Task: Ignored volumes list ([RC-25](https://nonameitem.atlassian.net/browse/RC-25))
Description: Django URL: `/missing_issues/ignored_volumes/`, template: `missing_issues/ignored_volumes_list.html`
Tags: volumes, missing-issues
Subtasks:
- Table of ignored volumes — endpoints: /api/missing-issues/ignored-volumes/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:191) | tags: volumes, missing-issues | Jira: [RC-196](https://nonameitem.atlassian.net/browse/RC-196)
- Delete ignored volume — endpoints: /api/missing-issues/ignored-volumes/<pk>/delete/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:194) | tags: volumes, missing-issues | Jira: [RC-255](https://nonameitem.atlassian.net/browse/RC-255)

## Task: Ignored publishers list ([RC-26](https://nonameitem.atlassian.net/browse/RC-26))
Description: Django URL: `/missing_issues/ignored_publishers/`, template: `missing_issues/ignored_publishers_list.html`
Tags: publishers, missing-issues
Subtasks:
- Table of ignored publishers — endpoints: /api/missing-issues/ignored-publishers/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:192) | tags: publishers, missing-issues | Jira: [RC-197](https://nonameitem.atlassian.net/browse/RC-197)
- Delete ignored publisher — endpoints: /api/missing-issues/ignored-publishers/<pk>/delete/ [PLAN] (ref: DRF_MIGRATION_URL_MAP.md:195) | tags: publishers, missing-issues | Jira: [RC-256](https://nonameitem.atlassian.net/browse/RC-256)
