import { h, resolveComponent } from "vue"

const fasl = {
  component: (props) => {
    const { icon, ...rest } = props
    const stringIcon = icon
    return h(props.tag, rest, [
      h(resolveComponent("font-awesome-icon"), {
        icon: ["fasl", stringIcon.includes(" fa-") ? stringIcon.split(" fa-") : stringIcon],
        key:  stringIcon,
      }),
    ])
  },
}

export { fasl }
