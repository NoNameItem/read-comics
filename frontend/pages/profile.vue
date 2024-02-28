<script setup>
import { useBreadcrumbsStore } from "@/stores/breadcrumbs"
import { useQuery } from "@tanstack/vue-query"
import { VSkeletonLoader } from "vuetify/labs/VSkeletonLoader"

definePageMeta({ loginRequired: true })

useServerSeoMeta({ title: "My profile" })

const { queries } = useQueryKeys()

const userTab = ref(null)

const tabs = [
  {
    icon:  "fasl:user",
    title: "Info",
  },
  {
    icon:  "fasl:lock",
    title: "Security",
  },
]

const breadcrumb = useBreadcrumbsStore()

breadcrumb.setBreadcrumbs("My profile", [{ title: "My profile" }])

const { data, isPending, suspense } = useQuery(queries.profile.profileData)

onServerPrefetch(async () => {
  await suspense()
})
</script>

<template>
  <div>
    <Breadcrumb />
    <VRow>
      <UserInfoPanel />

      <VCol
        cols="12"
        lg="8"
        md="7"
        xl="9"
        xxl="10"
      >
        <VTabs
          v-model="userTab"
          class="v-tabs-pill"
        >
          <VTab
            v-for="tab in tabs"
            :key="tab.icon"
          >
            <VIcon
              :icon="tab.icon"
              :size="18"
              class="me-1"
            />
            <span>{{ tab.title }}</span>
          </VTab>
        </VTabs>

        <VWindow
          v-model="userTab"
          :touch="false"
          class="mt-6 fullscreen"
        >
          <VWindowItem>
            <VSkeletonLoader
              :loading="isPending"
              style="background: transparent"
              type="paragraph"
            >
              <p
                v-if="data?.bio"
                class="bio"
              >
                {{ data?.bio }}
              </p>
            </VSkeletonLoader>
          </VWindowItem>

          <VWindowItem>
            <UserTabSecurity />
          </VWindowItem>
        </VWindow>
      </VCol>
    </VRow>
  </div>
</template>

<style scoped>
p.bio {
  white-space: pre-wrap;
}

.fullscreen .v-window-container {
  height: 100px;
  overflow-y: scroll;
}
</style>

<route lang="json">
{ "meta": { "loginRequired": true } }
</route>
