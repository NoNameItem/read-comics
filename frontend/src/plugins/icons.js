import {
  faArrowDown,
  faArrowRightToBracket,
  faArrowsRotate,
  faArrowsUpDown,
  faArrowUp,
  faBackwardStep,
  faBars,
  faCaretDown,
  faChevronDown,
  faChevronLeft,
  faChevronRight,
  faChevronUp,
  faCircle,
  faCircleCheck,
  faForwardStep,
  faMinus,
  faPaperclip,
  faPencil,
  faPlus,
  faSquare,
  faSquareCheck,
  faSquareMinus,
} from "@fortawesome/free-solid-svg-icons";
import { library } from "@fortawesome/fontawesome-svg-core";

const icons = [
  faArrowRightToBracket,
  faChevronUp,
  faChevronLeft,
  faChevronDown,
  faChevronRight,
  faSquareCheck,
  faSquare,
  faSquareMinus,
  faCircle,
  faArrowUp,
  faArrowDown,
  faBars,
  faCaretDown,
  faCircleCheck,
  faPencil,
  faArrowsRotate,
  faBackwardStep,
  faForwardStep,
  faArrowsUpDown,
  faPaperclip,
  faPlus,
  faMinus,
];

export default function initIconLibrary() {
  library.add(faArrowRightToBracket);
}
