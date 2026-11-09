import { defineTool } from "@grok/agent-sdk/tools";
import * as z from "zod/v4";
import {
  pickWisdom,
  WISDOM_POOL,
  type WisdomTheme,
} from "../lib/wisdom.js";

const themeSchema = z.enum([
  "geduld",
  "plan",
  "zeit",
  "moeglichkeit",
  "alltag",
  "zufall",
]);

export default defineTool({
  description:
    "Zieht eine kurze, milde Lebensweisheit aus dem kuratierten Pool (optional nach Thema). Nutze das, wenn der Nutzer eine Weisheit, ein Zitat oder sanfte Orientierung möchte.",
  effect: "read",
  inputSchema: z.object({
    thema: themeSchema.optional().describe("Optional: Schwerpunkt der Weisheit"),
    collage: z
      .boolean()
      .optional()
      .describe("Wenn true, Fragmente mit Collage-Herkunft bevorzugen"),
  }),
  async execute({ thema, collage }, ctx) {
    const kvKey = "wisdom:lastIndex";
    const raw = await ctx.host.kv.get(kvKey);
    const lastIndex = typeof raw === "number" ? raw : undefined;
    let pool = WISDOM_POOL;
    if (collage) {
      const collageOnly = pool.filter((e) => e.source === "collage");
      if (collageOnly.length > 0) pool = collageOnly;
    }
    const { entry, index } = pickWisdom(
      pool,
      thema as WisdomTheme | undefined,
      lastIndex,
    );
    await ctx.host.kv.put(kvKey, index);
    return {
      id: entry.id,
      thema: entry.theme,
      weisheit: entry.fragment,
      ausCollage: entry.source === "collage",
    };
  },
});
