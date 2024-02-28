import { h, resolveComponent } from "vue"

const fab = {
  component: (props) => {
    const { icon, ...rest } = props
    const stringIcon = icon
    return h(props.tag, rest, [
      h(resolveComponent("font-awesome-icon"), {
        icon: ["fab", stringIcon.includes(" fa-") ? stringIcon.split(" fa-") : stringIcon],
        key:  stringIcon,
      }),
    ])
  },
}

export { fab }
