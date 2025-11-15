
# Using `state_cz_mapping.csv` in the Earnings Premium Simulation

This file provides a **synthetic but proportional** mapping from U.S. state abbreviations to the number of commuting zones (CZs) each state should have in Version 1 of the simulation.

> **Important:** The counts are *approximate* and intended only to make the simulation more realistic and interpretable. They are **not** the official USDA / Fowler commuting-zone counts. For research-grade work, this file should eventually be replaced with a mapping derived from the true CZ crosswalk.

## 1. File Structure

`state_cz_mapping.csv` has two columns:

- `state` – two-letter state (or DC) postal abbreviation.  
- `cz_count` – the number of synthetic commuting zones to create for that state.

Example rows:

```csv
state,cz_count
AL,9
AK,4
AZ,14
...
```

## 2. Where to Place the File

Place `state_cz_mapping.csv` at the **project root** or in a small data directory, for example:

- `./data/state_cz_mapping.csv`

If you use a `data/` folder, remember to update the path in the simulation code.

## 3. How Codex Should Wire This Into the Simulation

Below is the *logic* Codex should implement, **not literal code**.

1. **Load the mapping once at app startup.**  
   - Read `state_cz_mapping.csv` into a DataFrame or dictionary: `state -> cz_count`.
   - This can live in a helper such as `simulation/config.py`.

2. **When the user selects a state in the sidebar:**  
   - Look up `cz_count` for that state from the mapping.  
   - Use this value instead of the current fixed number of CZs.

3. **CZ generation logic should change from “fixed count” to “state-specific count.”**  
   - Currently, you probably do something like:  
     - `num_cz = fixed_value` (e.g., 10)  
   - Replace this with:  
     - `num_cz = state_to_cz_count[state_abbrev]`

4. **Programs per CZ slider stays the same.**  
   - Continue to use the existing slider (e.g., `Programs per CZ`) to decide how many synthetic programs to allocate to each commuting zone.  
   - Total programs in a state will now be:  
     - `total_programs = cz_count * programs_per_cz`

5. **Downstream logic (earnings, benchmarks, classifications) does not change.**  
   - All existing functions that:  
     - create local HS earnings per CZ,  
     - generate early/late earnings per program,  
     - compare against statewide and local benchmarks,  
     - compute pass/fail and distances,  
     continue to operate as before, just over a different number of CZs.

6. **Optional: display CZ count in the UI.**  
   - In the main panel, you may want to show a short text like:  
     - “This simulation uses **N** synthetic commuting zones for STATE, based on approximate proportional size.”  
   - This will help policymakers understand why California’s plot has more points than Arkansas’s.

## 4. Edge Cases & Defaults

- If for some reason a state abbreviation is not found in the mapping, default to a small number of CZs (e.g., 8) and log a warning.  
- The mapping includes all 50 states plus DC, so this should not normally occur.

## 5. Future Upgrade Path

When you are ready to move beyond approximations:

1. Replace `state_cz_mapping.csv` with a file derived from the official commuting-zone crosswalk (e.g., Fowler 2016 / 2020 or USDA ERS data).  
2. Set `cz_count` equal to the **actual number of CZs per state**.  
3. Optionally replace synthetic CZ IDs with the real CZ codes as a new column (e.g., `cz_id`).

Until then, this file gives you *state-specific geographic complexity* while keeping Version 1 conceptually simple and easy to maintain.
