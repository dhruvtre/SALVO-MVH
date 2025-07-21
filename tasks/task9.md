Goal: Analyze the evaluation results and generate a final report to explicitly validate or falsify the hypothesis.
Budget: { gpu_type: "none", max_hours: 0.1, max_memory_GB: 8 }
Output:
- Core Deliverables:
    - `/outputs/results.md`: A Markdown file summarizing the results. It must include:
        - A table with the mean and standard deviation of episodic returns for both models.
        - A clear statement of the success threshold from the MVH_SPEC.
        - A final, unambiguous verdict: "HYPOTHESIS VALIDATED" or "HYPOTHESIS FALSIFIED".
- Verification Artifacts:
    - Console output printing the final verdict.
Inputs:
- Data: `/outputs/evaluation_results.json`.
- Spec: The `MVH_SPEC` document.
Guidelines:
1.  Create a new file `src/analyze.py` with a function `generate_report()`.
2.  This function will load `/outputs/evaluation_results.json`.
3.  It will calculate the success threshold: `max(0.90 * baseline_mean_return, 450)`.
4.  It will compare the SALVO-mini mean return against this threshold.
5.  The function will format and write the results to `/outputs/results.md`.
6.  Add a final `@stub.function(...)` to `run.py` called `analyze_results` that executes this analysis. This function should be the final step in the Modal app's `local_entrypoint` call chain.
Additional Context: This is the final step that directly answers the research question posed by the MVH. The output should be clear and directly reference the criteria in the specification.