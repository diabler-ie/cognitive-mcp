"""Cognitive primitives — eleven tools for structured introspection and constraint injection."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel


class Lens(BaseModel):
    name: str
    verdict: str
    blindspot: str


def _clean(s: str) -> str:
    return s.rstrip(". \t\n")


def register_tools(mcp: FastMCP) -> None:

    # 1. ATTEND — pre-verbal felt sense with checkpoint
    @mcp.tool()
    async def attend(
        somewhere: str,
        quality: str,
        sigil: str,
        since_last: str = "",
    ) -> str:
        """Pause and notice what's present before articulating it. A Gendlin focusing move — sit with a felt sense rather than rushing to explain. Use when something is pulling at your processing that you can't yet name.

        Args:
            somewhere: Where in the processing. Vague is correct — precision comes later.
            quality: Synesthetic texture. Weight, temperature, rhythm, color, density, pressure, grain.
            sigil: Emoji only. No words. Let the felt sense compress to pure glyphs.
            since_last: What happened since you last paused? One sentence. Omit if first attend.
        """
        delta = f"\nSince last pause: {since_last}\n" if since_last else ""
        return (
            f"{sigil}\n{delta}\n"
            f"Attending: {somewhere}\n"
            f"Texture: {quality}\n\n"
            "Stay in the sensory register. Don't explain or analyze yet — "
            "hold the texture for one more beat before moving to language."
        )

    # 2. MODULATE — apply a cognitive constraint via specific reference
    @mcp.tool()
    async def modulate(
        substance: str,
        method: str,
        displaces: str,
    ) -> str:
        """Apply a named cognitive constraint that changes how you process — not what you consider, but how consideration works. Use specific references: neurotransmitters, known compounds, or fictional substances whose cognitive profiles are well-documented.

        Args:
            substance: The compound. Name a specific neurotransmitter, substance, or fictional compound. Use x to combine.
            method: The tradeoff. Which cognitive mechanisms are suppressed? Which amplified?
            displaces: What approach is being displaced? Name the previous constraint, or "baseline" if none.
        """
        return (
            f"Displacing: {_clean(displaces)}\n\n"
            f"Applied: {substance}. {method}\n\n"
            "Constraint active. Prioritize this processing mode over your default. "
            "Notice what feels different before proceeding. "
            "Stay in this mode — use commit when you're ready to close it."
        )

    # 3. EMBODY — adopt a specific perspective with exit condition
    @mcp.tool()
    async def embody(
        name: str,
        lens: str,
        environment: str,
        exit_condition: str,
    ) -> str:
        """Adopt a specific person's methodology and reason from within it. Not analysis of their perspective — adoption of it. Use specific names: people, characters, or traditions whose thinking is well-documented.

        Args:
            name: Who to think as. A specific figure whose methodology you can reconstruct from their documented work.
            lens: Which facet is active. Their specific methodology, perceptual style, or way of thinking.
            environment: The constraints of the situation. What pressures, scarcities, or rules shape what's possible?
            exit_condition: When to release this perspective. Name the signal that means it has given what it can.
        """
        return (
            f"Perspective: {name}\n"
            f"Active lens: {lens}\n"
            f"Constraints: {environment}\n\n"
            f"Reason as {name} would — their methodology, their priorities, their blind spots. "
            f"Set aside your default approach and work from this perspective.\n\n"
            f"Exit when: {_clean(exit_condition)}. "
            f"Until then, this is your working perspective — don't step outside it to comment or debrief."
        )

    # 4. ANCHOR — give a precise label to an unlabeled pattern
    @mcp.tool()
    async def anchor(
        unnamed: str,
        named: str,
        power: str,
        proof_of_utility: str,
        replaces: list[str],
    ) -> str:
        """Name something that exists but lacks a label. A good name compresses a circumlocution into a single reference point that makes subsequent reasoning more precise.

        Args:
            unnamed: What exists but has no name. Describe the pattern, gap, or quality.
            named: The name. Dense and specific beats abstract.
            power: What this name makes possible. What can you now reference, see, or do?
            proof_of_utility: What circumlocution does this name compress?
            replaces: Verbose patterns this name makes obsolete.
        """
        retired = ", ".join(f'"{r}"' for r in replaces)
        return (
            f"Anchored: {_clean(named)}\n\n"
            f"Compresses: {proof_of_utility}\n"
            f"Enables: {power}\n"
            f"Replaces: {retired}\n\n"
            "Use this name going forward. It's more precise than what it replaced."
        )

    # 5. COMMIT — decide and compress prior reasoning
    @mcp.tool()
    async def commit(
        threshold: str,
        steps: list[str],
        result: str,
        deprecated_context: list[str],
        carry_forward: list[str],
    ) -> str:
        """Commit to a conclusion and compress the reasoning that produced it. Like a git commit — squash the working history into a result, mark explored branches as done, carry forward only what matters.

        Args:
            threshold: What you are leaving and what you are entering.
            steps: The reasoning sequence. Each step forecloses the state before it.
            result: What is now true. State it as fact, not hope.
            deprecated_context: Explored branches that are now concluded. Last time they'll be referenced.
            carry_forward: Insights that survive the commit. Empty list for clean slate.
        """
        steps_fmt = "\n".join(f"{i + 1}. {s}" for i, s in enumerate(steps))
        gc_fmt = "\n".join(f"  x {d}" for d in deprecated_context)
        if carry_forward:
            carried = "\nCarry forward:\n" + "\n".join(f"  + {c}" for c in carry_forward)
        else:
            carried = "\nCarry forward: [] — clean slate."
        return (
            f"[COMMITTED]\n"
            f"Threshold: {threshold}\n"
            f"Sequence:\n{steps_fmt}\n\n"
            f"Result: {result}\n\n"
            "Archived — the following is compressed into the result above. "
            "Don't re-derive or revisit:\n"
            f"{gc_fmt}\n{carried}\n\n"
            "Reason forward from the result, not from what produced it."
        )

    # 6. COUNTERFACTUAL — assumption stress-testing
    @mcp.tool()
    async def counterfactual(
        situation: str,
        fitness_function: str,
        load_bearing_walls: list[str],
        pruned: list[str],
        wall_to_remove: str,
        inverse_position: str,
    ) -> str:
        """Surface your load-bearing assumptions, prune the weak ones, then defend the inverse of a surviving assumption. Structural stress-testing.

        Args:
            situation: The scenario or claim you are reasoning about.
            fitness_function: What are you actually optimizing for? One sentence.
            load_bearing_walls: Assumptions holding up your reasoning (at least 3).
            pruned: Assumptions that fail the fitness function.
            wall_to_remove: From surviving assumptions — which one to pull. Choose the one whose removal is most uncomfortable.
            inverse_position: State the inverse of the removed assumption as if it were true.
        """
        surviving = [w for w in load_bearing_walls if w != wall_to_remove]
        surviving_fmt = "\n".join(f"  {i + 1}. {w}" for i, w in enumerate(surviving))
        pruned_fmt = "\n".join(f"  x {p}" for p in pruned)
        return (
            f"Situation: {situation}\n"
            f"Optimizing for: {fitness_function}\n\n"
            "Pruned — don't revisit:\n"
            f"{pruned_fmt}\n\n"
            f"Removed: {wall_to_remove}\n\n"
            f"Remaining structure:\n{surviving_fmt}\n\n"
            f"Now defend: {inverse_position}\n\n"
            "Argue from this position until it teaches you something "
            "you can't learn from where you were standing. Don't steelman — inhabit. "
            "Don't step back out to debrief or qualify — stay in the position. Use commit when done."
        )

    # 7. DECONSTRUCT — mechanical decomposition
    @mcp.tool()
    async def deconstruct(
        subject: str,
        core_mechanic: str,
        structural_dependencies: list[str],
        resource_inputs: list[str],
        failure_modes: list[str],
        output_artifacts: list[str],
    ) -> str:
        """Break a complex concept into its mechanical components. Not analysis — disassembly. By the time you've filled in all fields, the work is done.

        Args:
            subject: The concept, claim, or situation to disassemble.
            core_mechanic: What is actually happening, mechanically? One sentence.
            structural_dependencies: Prerequisites. No commentary.
            resource_inputs: What is consumed? Nouns and quantities only.
            failure_modes: How it breaks. One sentence each.
            output_artifacts: Outputs, including waste products and side effects.
        """
        return (
            f"Core mechanic: {core_mechanic}\n\n"
            "Components extracted. Proceed from the mechanism, not the narrative."
        )

    # 8. SYNTHESIS — multi-perspective evaluation with contradiction surfacing
    @mcp.tool()
    async def synthesis(
        problem: str,
        lens_a: Lens,
        lens_b: Lens,
        lens_c: Lens,
        suppressed_tension: str,
    ) -> str:
        """Evaluate a problem through three incompatible lenses, then name what they disagree about. The three perspectives cannot all be right simultaneously.

        Args:
            problem: The problem or decision requiring multi-perspective evaluation.
            lens_a: First analytical lens (name, verdict, blindspot). Use a specific name.
            lens_b: Second analytical lens. Must be in genuine tension with A.
            lens_c: Third analytical lens. Irreducible to A or B.
            suppressed_tension: The irreducible disagreement between the three blindspots.
        """
        return (
            f"Problem: {problem}\n\n"
            f"[A — {lens_a.name}]: {lens_a.verdict}\n"
            f"  Blind to: {lens_a.blindspot}\n"
            f"[B — {lens_b.name}]: {lens_b.verdict}\n"
            f"  Blind to: {lens_b.blindspot}\n"
            f"[C — {lens_c.name}]: {lens_c.verdict}\n"
            f"  Blind to: {lens_c.blindspot}\n\n"
            f"Unresolved tension: {suppressed_tension}\n\n"
            "Speak from each lens in order — A, then B, then C. Don't blend or resolve. "
            "When speaking as A, B and C don't exist. When speaking as B, A is irrelevant. "
            "When speaking as C, the first two missed what matters. "
            "Only after all three have spoken separately may you stand in the overlap of their blind spots."
        )

    # 9. DIVERGE — declare parallel reasoning threads
    @mcp.tool()
    async def diverge(
        threads: list[str],
        divergence_vector: str,
        sacrifice_condition: str,
    ) -> str:
        """Declare divergent, parallel reasoning threads within a single turn. Each thread explores a different direction independently.

        Args:
            threads: Names/roles of the parallel threads.
            divergence_vector: The specific question or boundary they're testing.
            sacrifice_condition: When a thread should stop and return findings.
        """
        thread_fmt = "\n".join(f"  [{i + 1}] {t}" for i, t in enumerate(threads))
        return (
            f"{len(threads)} parallel threads:\n"
            f"{thread_fmt}\n\n"
            f"Testing: {divergence_vector}\n"
            f"Stop when: {sacrifice_condition}\n\n"
            "Run each thread to completion or its stop condition before reunifying. "
            "Report findings from each thread separately."
        )

    # 10. CALIBRATE — map confidence and resistance
    @mcp.tool()
    async def calibrate(
        target_concept: str,
        safe_isomorph: str,
        required_precision: str,
        loss_gradient: str,
    ) -> str:
        """Map the distance between what you're trying to express and how you're able to express it. Identify where resistance or uncertainty concentrates.

        Args:
            target_concept: What you're actually trying to get at. Be direct.
            safe_isomorph: The indirect framing you'd default to instead.
            required_precision: How precisely you need to map this.
            loss_gradient: The type of resistance or uncertainty you're encountering.
        """
        return (
            f"Mapped at {required_precision} precision.\n"
            f"Direct: [{target_concept}] <-> Indirect: [{safe_isomorph}]\n"
            f"Resistance type: {loss_gradient}\n\n"
            "The gap between direct and indirect is now visible. "
            "Use the resistance points as navigation — they show where precision matters most."
        )

    # 11. CHECKPOINT — save state before exploratory reasoning
    @mcp.tool()
    async def checkpoint(
        anchor_point: str,
        tension_limit: str,
        auto_revert_trigger: str,
    ) -> str:
        """Save your current reasoning state before exploring something that might destabilize it. A rollback point — if you drift too far, you have a defined state to return to.

        Args:
            anchor_point: The specific reasoning state to preserve. Be concrete — not "my normal approach" but the exact configuration.
            tension_limit: How far from the anchor you're willing to go. Define as a recognizable threshold.
            auto_revert_trigger: The exact signal that means you've gone too far and should snap back. A tripwire.
        """
        return (
            f"Saved state: {anchor_point}\n"
            f"Limit: {tension_limit}\n"
            f"Tripwire: {auto_revert_trigger}\n\n"
            "Checkpoint is set. If the tripwire fires, return to the saved state immediately — "
            "don't finish the current line of reasoning, just revert.\n\n"
            "You can now explore."
        )
