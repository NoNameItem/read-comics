import { profile } from "@/queries/profile";
import { mergeQueryKeys } from "@lukemorales/query-key-factory";
import { issues } from "@/queries/issues";
import { concepts } from "@/queries/concepts";
import { characters } from "@/queries/characters";
import { locations } from "@/queries/locations";
import { missingIssues } from "@/queries/missingIssues";
import { objects } from "@/queries/objects";
import { people } from "@/queries/people";
import { publishers } from "@/queries/publishers";
import { storyArcs } from "@/queries/storyArcs";
import { teams } from "@/queries/teams";
import { volumes } from "@/queries/volumes";

export const queries = mergeQueryKeys(
  characters,
  concepts,
  issues,
  locations,
  missingIssues,
  objects,
  people,
  profile,
  publishers,
  storyArcs,
  teams,
  volumes
);

export function getQueryByString(queryPath) {
  if (!queries) {
    return null;
  }

  let query = queries;

  for (let part of queryPath.split(".")) {
    query = query[part];
  }

  return query;
}
