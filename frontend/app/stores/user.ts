// noinspection D

import FThumb from '~/assets/images/avatars/F_thumb.png'
import F from '~/assets/images/avatars/F.png'
import MThumb from '~/assets/images/avatars/M_thumb.png'
import M from '~/assets/images/avatars/M.png'
import OThumb from '~/assets/images/avatars/O_thumb.png'
import O from '~/assets/images/avatars/O.png'
import UThumb from '~/assets/images/avatars/U_thumb.png'
import U from '~/assets/images/avatars/U.png'
import { defineStore } from 'pinia'

const defaultImages = {
  F,
  M,
  O,
  U
}

const defaultThumbnails = {
  F: FThumb,
  M: MThumb,
  O: OThumb,
  U: UThumb
}

export const useUserStore = defineStore(
  'user',
  () => {
    const accessToken = ref(null)
    const refreshToken = ref(null)
    const refreshingToken = ref(false)

    const username = ref(null)
    const name = ref(null)
    const email = ref(null)
    const emailVerified = ref(null)
    const gender = ref(null)
    const images = ref(null)
    const birthDate = ref(null)
    const registerDate = ref(null)
    const isSuperuser = ref(false)
    const isStaff = ref(false)

    const $reset = () => {
      accessToken.value = null
      refreshToken.value = null
      refreshingToken.value = false
      username.value = null
      name.value = null
      email.value = null
      emailVerified.value = null
      gender.value = null
      images.value = null
      birthDate.value = null
      registerDate.value = null
      isSuperuser.value = false
      isStaff.value = false
    }

    const image = computed(() => images.value?.image ?? defaultImages[gender.value?.value ?? 'O'])
    const thumbnail = computed(
      () => images.value?.thumbnail ?? defaultThumbnails[gender.value?.value ?? 'O']
    )
    const loggedIn = computed(() => !!accessToken.value)
    const isSuperuserOrStaff = computed(() => isSuperuser.value || isStaff.value)
    const displayName = computed<string>(() => name.value || username.value || '')

    const setUser = (user) => {
      username.value = user?.username
      name.value = user?.name
      email.value = user?.email
      emailVerified.value = user?.email_verified ?? emailVerified.value
      gender.value = user?.gender
      images.value = user?.images
      birthDate.value = user?.birth_date
      registerDate.value = user?.date_joined
      isSuperuser.value = user?.is_superuser ?? isSuperuser.value
      isStaff.value = user?.is_staff ?? isStaff.value
    }

    const setImage = (user) => {
      images.value = user?.images
    }

    const resetImage = () => {
      images.value = null
    }

    const setTokens = (newAccessToken, newRefreshToken) => {
      accessToken.value = newAccessToken
      refreshToken.value = newRefreshToken
    }

    const login = async (username, password) => {
      const axios = useAxios()

      const loginUrl = '/auth/login/'
      try {
        const response = await axios.post(loginUrl, { password, username })
        if (response?.status === 200) {
          const data = await response.data

          setTokens(data.access, data.refresh)
          setUser(data.user)
        }
      } catch (e) {
        return e
      }
    }

    const refreshTokens = async () => {
      const axios = useAxios()

      const refreshUrl = '/auth/token/refresh/'
      try {
        const response = await axios.post(refreshUrl, { refresh: refreshToken.value })
        if (response.status === 200) {
          const data = await response.data

          setTokens(data.access, data.refresh)
        }
      } catch {
        // Ignore - token refresh can fail
      }
    }

    const register = async (username, email, password) => {
      const axios = useAxios()

      const registerUrl = '/auth/registration/'
      try {
        const response = await axios.post(registerUrl, {
          email,
          password1: password,
          password2: password,
          username
        })

        if (response?.status === 201) {
          const data = await response.data

          setTokens(data.access, data.refresh)
          setUser(data.user)
        }
      } catch (e) {
        return e
      }
    }

    const logout = async () => {
      const axios = useAxios()
      const toast = useToast()

      // Save the name before $reset() for the toast message
      const userName = name.value || username.value

      // Send refresh token to backend for blacklisting
      // Ignore errors - logout should work even if backend is unavailable
      if (refreshToken.value) {
        try {
          await axios.post('/auth/logout/', { refresh: refreshToken.value })
        } catch {
          // Ignore errors - clearing local state is more important
        }
      }

      $reset()

      // Show toast after clearing state
      if (userName) {
        toast.add({
          title: `Bye, ${userName}. Hope to see you soon!`,
          color: 'success'
        })
      }
    }

    return {
      $reset,
      accessToken,
      birthDate,

      email,
      email_verified: emailVerified,
      gender,
      image,
      images,
      isStaff,
      isSuperuser,
      isSuperuserOrStaff,
      loggedIn,
      login,

      logout,
      name,
      refreshingToken,
      refreshToken,

      refreshTokens,
      register,
      registerDate,
      resetImage,
      setImage,
      setTokens,
      setUser,
      thumbnail,
      username,
      displayName
    }
  },
  { persist: true }
)
