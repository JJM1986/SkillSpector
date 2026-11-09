import { defineEval } from "@grok/agent-sdk/evals";

export default defineEval({
  tags: ["smoke"],
  description: "Lebensweisheit-Tool liefert ein Fragment.",
  async test(t) {
    await t.send(
      "Gib mir eine milde Lebensweisheit für heute. Nutze dazu das Tool lebensweisheit.",
    );
    t.succeeded();
    t.calledTool("lebensweisheit");
  },
});
