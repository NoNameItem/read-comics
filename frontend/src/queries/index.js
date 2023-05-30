import { profile } from "@/queries/profile";
import { mergeQueryKeys } from "@lukemorales/query-key-factory";

export const queries = mergeQueryKeys(profile);
