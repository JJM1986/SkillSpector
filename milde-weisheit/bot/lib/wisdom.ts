export type WisdomTheme =
  | "geduld"
  | "plan"
  | "zeit"
  | "moeglichkeit"
  | "alltag"
  | "zufall";

export type WisdomEntry = {
  id: string;
  theme: WisdomTheme;
  fragment: string;
  source?: "collage";
};

/** Kuratierte Fragmente — u. a. inspiriert vom Analog-Collage „Milde Weisheit“. */
export const WISDOM_POOL: WisdomEntry[] = [
  {
    id: "collage-langwierig",
    theme: "geduld",
    fragment:
      "Es wird ein langwieriges Werden. Naja — so fühlst du es manchmal. Dass etwas nach Plan verläuft, ist die Ausnahme, nicht die Regel.",
    source: "collage",
  },
  {
    id: "collage-moeglich",
    theme: "moeglichkeit",
    fragment:
      "Frag nicht zuerst, was unmöglich ist. Frag sanft, was möglich ist — und was sich verändert, wenn du nur einen Schritt gehst.",
    source: "collage",
  },
  {
    id: "collage-dinge",
    theme: "zeit",
    fragment:
      "Womit du deine Tage verbringst, verändert dich leiser, als du denkst. Achte darauf, nicht nur auf die großen Entscheidungen.",
    source: "collage",
  },
  {
    id: "collage-ein-tag",
    theme: "zeit",
    fragment:
      "Das Beste lässt du dir manchmal nur einen Tag Zeit. Manchmal reicht genau ein Tag — nicht perfekt, nur ehrlich.",
    source: "collage",
  },
  {
    id: "collage-plan",
    theme: "plan",
    fragment:
      "Wenn der Plan kippt: atme. Milde Weisheit heißt nicht, den Plan zu vergessen — sondern dich nicht mit ihm zu zerschlagen.",
    source: "collage",
  },
  {
    id: "alltag-achtung",
    theme: "alltag",
    fragment:
      "Achtung heißt hier nicht Alarm. Es heißt: Hinsehen, ohne dich selbst zu verurteilen.",
  },
  {
    id: "geduld-wasser",
    theme: "geduld",
    fragment:
      "Geduld ist kein Warten auf besseres Wetter. Geduld ist Regen mitnehmen und trotzdem einen Schritt tun.",
  },
  {
    id: "plan-zweiter",
    theme: "plan",
    fragment:
      "Ein Plan ist eine Landkarte. Du darfst umkehren, wenn der Weg dein Herz enger macht.",
  },
  {
    id: "zeit-heute",
    theme: "zeit",
    fragment:
      "Nicht alles, was wichtig ist, ist dringend. Nicht alles Dringende verdient deinen besten Teil des Tages.",
  },
  {
    id: "moeglichkeit-klein",
    theme: "moeglichkeit",
    fragment:
      "Große Veränderung beginnt oft mit einer kleinen, erträglichen Tat. Das ist keine Feigheit. Das ist Klugheit.",
  },
  {
    id: "alltag-milde",
    theme: "alltag",
    fragment:
      "Sei dir selbst nicht der strengste Richter im Raum. Milde beginnt mit der Stimme, die du innerlich benutzt.",
  },
  {
    id: "zufall-offen",
    theme: "zufall",
    fragment:
      "Zufall und Plan können Nachbarn sein. Lass eine kleine Tür offen für das Unerwartete — ohne alles daran zu hängen.",
  },
];

export function pickWisdom(
  pool: WisdomEntry[],
  theme: WisdomTheme | undefined,
  lastIndex: number | undefined,
): { entry: WisdomEntry; index: number } {
  const filtered = theme
    ? pool.filter((e) => e.theme === theme)
    : pool.slice();
  const choices = filtered.length > 0 ? filtered : pool;
  let index = 0;
  if (typeof lastIndex === "number" && choices.length > 1) {
    const globalIdx = pool.indexOf(choices[(lastIndex + 1) % choices.length]!);
    index = globalIdx >= 0 ? globalIdx : (lastIndex + 1) % pool.length;
  } else {
    index = Math.floor(Math.random() * pool.length);
  }
  const entry = pool[index]!;
  return { entry, index };
}
