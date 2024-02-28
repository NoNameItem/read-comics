import { useCharacterKeys } from "@/composables/queries/useCharacterKeys.js"
import { useConceptKeys } from "@/composables/queries/useConceptKeys.js"
import { useIssueKeys } from "@/composables/queries/useIssueKeys.js"
import { useLocationKeys } from "@/composables/queries/useLocationKeys.js"
import { useMissingIssueKeys } from "@/composables/queries/useMissingIssueKeys.js"
import { useObjectKeys } from "@/composables/queries/useObjectKeys.js"
import { usePeopleKeys } from "@/composables/queries/usePeopleKeys.js"
import { useProfileKeys } from "@/composables/queries/useProfileKeys.js"
import { usePublisherKeys } from "@/composables/queries/usePublisherKeys.js"
import { useStoryArcKeys } from "@/composables/queries/useStoryArcKeys.js"
import { useTeamKeys } from "@/composables/queries/useTeamKeys.js"
import { useVolumeKeys } from "@/composables/queries/useVolumeKeys.js"
import { mergeQueryKeys } from "@lukemorales/query-key-factory"

export const useQueryKeys = () => {
  const queries = mergeQueryKeys(
    useCharacterKeys(),
    useConceptKeys(),
    useIssueKeys(),
    useLocationKeys(),
    useMissingIssueKeys(),
    useObjectKeys(),
    usePeopleKeys(),
    useProfileKeys(),
    usePublisherKeys(),
    useStoryArcKeys(),
    useTeamKeys(),
    useVolumeKeys(),
  )

  const getQueryByString = (queryPath) => {
    if (!queries) {
      return null
    }

    let query = queries

    for (const part of queryPath.split(".")) {
      query = query[part]
    }

    return query
  }

  return { getQueryByString, queries }
}
