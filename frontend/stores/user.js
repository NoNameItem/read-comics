import { defineStore } from "pinia"
import axios from "@axios"

import FThumb from "@images/avatars/F_thumb.png"
import MThumb from "@images/avatars/M_thumb.png"
import OThumb from "@images/avatars/O_thumb.png"
import UThumb from "@images/avatars/U_thumb.png"

import F from "@images/avatars/F.png"
import M from "@images/avatars/M.png"
import O from "@images/avatars/O.png"
import U from "@images/avatars/U.png"

const defaultImages = {
  F,
  M,
  O,
  U,
}

const defaultThumbnails = {
  F: FThumb,
  M: MThumb,
  O: OThumb,
  U: UThumb,
}

export const useUserStore = defineStore(
  "user",
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

    const image = computed(() => images.value?.image ?? defaultImages[gender.value?.value ?? "O"])
    const thumbnail = computed(() => images.value?.thumbnail ?? defaultThumbnails[gender.value?.value ?? "O"])
    const loggedIn = computed(() => !!accessToken.value)
    const isSuperuserOrStaff = computed(() => isSuperuser.value || isStaff.value)

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
      const loginUrl = "/auth/login/"
      try {
        const response = await axios.post(loginUrl, { username, password })
        if (response?.status === 200) {
          const data = await response.data

          setTokens(data.access, data.refresh)
          setUser(data.user)
        }
      }
      catch (e) {
        return e
      }
    }

    const refreshTokens = async () => {
      const refreshUrl = "/auth/token/refresh/"
      try {
        const response = await axios.post(refreshUrl, { refresh: refreshToken.value })
        if (response.status === 200) {
          const data = await response.data

          setTokens(data.access, data.refresh)
        }
      }
      catch (e) {
      }
    }

    const register = async (username, email, password) => {
      const registerUrl = "/auth/registration/"
      try {
        const response = await axios.post(registerUrl, { username, email, password1: password, password2: password })

        if (response?.status === 201) {
          const data = await response.data

          setTokens(data.access, data.refresh)
          setUser(data.user)
        }
      }
      catch (e) {
        return e
      }
    }

    const logout = () => {
      $reset()
    }

    return {
      accessToken,
      refreshToken,
      refreshingToken,

      username,
      name,
      email,
      email_verified: emailVerified,
      gender,
      images,
      birthDate,
      registerDate,
      isSuperuser,
      isStaff,

      image,
      thumbnail,
      loggedIn,
      isSuperuserOrStaff,

      setUser,
      setImage,
      resetImage,
      $reset,
      setTokens,
      login,
      refreshTokens,
      register,
      logout,
    }
  },
  { persist: true },
)
