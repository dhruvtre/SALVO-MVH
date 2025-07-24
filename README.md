# SALVO MVH

Vision Language Model control experiment testing whether VLM perceptual understanding can replace explicit physical state information in control tasks.

## Current Status

**Completed Tasks:**
- Task 1: Data collection infrastructure setup
- Task 2: 100k cartpole-swingup dataset generation

**Dataset:** 100k frames stored in Modal cloud storage with images, actions, rewards, and terminal states.

## Repository Contents

- **`run.py`** - Modal application for data collection and sampling
- **`src/`** - Data generation source code
- **`docs/`** - Research journal, task logs, and project checkpoint
- **`outputs/`** - Sample visualization images from dataset
- **`.gitignore`** - Standard Python exclusions and environment files

## Environment

- **Platform:** Modal cloud computing with GPU support
- **Environment:** dm_control cartpole-swingup
- **Dataset Format:** Vision-only (64x64 images) with actions, rewards, terminals
- **Baseline Reference:** DreamerV2 (excluded from repo, available via task documentation)

## Next Steps

- Task 3: SALVO implementation
- Task 4: Dreamer baseline training