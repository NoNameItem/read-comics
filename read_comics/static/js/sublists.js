function getSublistPage(pageNum, tabSelector, sourceUrl) {
  let $tabContent = $(tabSelector + ' .tab-content');
  $tabContent.block({
      message: '<div class="bx bx-revision icon-spin font-medium-2"></div>',
      overlayCSS: {
        backgroundColor: '#fff',
        opacity: 0.8,
        cursor: 'wait'
      },
      css: {
        border: 0,
        padding: 0,
        backgroundColor: 'transparent'
      }
    });
  $.ajax({
    url  : sourceUrl + '?page=' + pageNum,
    type : 'GET'
  }).done(function (data, textStatus, jqXHR) {
    $tabContent.html(data);
    $tabContent.unblock()
  }).fail(function (jqXHR, textStatus, errorThrown) {
    if (jqXHR.status === 404) {
      toastr.error("Could not get info");
    }
    $tabContent.unblock()
  });
}

function getIssuesPage(pageNum) {
  getSublistPage(pageNum, '#issues', issuesUrl);
}

function getCharactersPage(pageNum) {
  getSublistPage(pageNum, '#characters', charactersUrl);
}

function getDiedPage(pageNum) {
  getSublistPage(pageNum, '#died', diedUrl);
}

function getConceptsPage(pageNum) {
  getSublistPage(pageNum, '#concepts', conceptsUrl);
}

function getLocationsPage(pageNum) {
  getSublistPage(pageNum, '#locations', locationsUrl);
}

function getObjectsPage(pageNum) {
  getSublistPage(pageNum, '#objects', objectsUrl);
}

function getAuthorsPage(pageNum) {
  getSublistPage(pageNum, '#authors', authorsUrl);
}

function getStoryArcsPage(pageNum) {
  getSublistPage(pageNum, '#story-arcs', storyArcsUrl);
}

function getTeamsPage(pageNum) {
  getSublistPage(pageNum, '#teams', teamsUrl);
}

function getDisbandedPage(pageNum) {
  getSublistPage(pageNum, '#disbanded', disbandedUrl);
}

function getFirstAppearancesPage(pageNum) {
  getSublistPage(pageNum, '#first-appearance', firstAppearancesUrl);
}

function getVolumesPage(pageNum) {
  getSublistPage(pageNum, '#volumes', volumesUrl);
}

function getEnemiesPage(pageNum) {
  getSublistPage(pageNum, '#enemies', enemiesUrl);
}

function getFriendsPage(pageNum) {
  getSublistPage(pageNum, '#friends', friendsUrl);
}

function getTeamFriendsPage(pageNum) {
  getSublistPage(pageNum, '#team-friends', teamFriendsUrl);
}

function getTeamEnemiesPage(pageNum) {
  getSublistPage(pageNum, '#team-enemies', teamEnemiesUrl);
}
