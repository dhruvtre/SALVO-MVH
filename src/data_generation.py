import numpy as np
from PIL import Image
import gymnasium as gym
import shimmy
import os

def generate_data():
    """Generates and saves a 100,000-frame dataset from the dm_control
    Cartpole-swingup environment using a random policy."""
    
    print("🔧 Setting up environment variables for GPU headless rendering...")
    # Set environment variables for headless rendering (MUST be set before importing dm_control)
    os.environ['MUJOCO_GL'] = 'egl'  # Use EGL for hardware-accelerated rendering
    print(f"   MUJOCO_GL = {os.environ.get('MUJOCO_GL')}")

    print("🏗️  Creating dm_control environment...")
    # Create the environment with pixel observations
    env = gym.make("dm_control/cartpole-swingup-v0", render_mode="rgb_array")
    print(f"   ✅ Environment created successfully!")
    print(f"   📊 Observation space: {env.observation_space}")
    print(f"   🎮 Action space: {env.action_space}")
    
    print("🎲 Setting random seed for reproducibility...")
    # Set a fixed random seed for reproducibility
    np.random.seed(42)
    print("   ✅ Random seed set to 42")
    
    print("📦 Initializing data storage...")
    # Initialize lists to store the collected data
    observations = []
    actions = []
    rewards = []
    terminals = []
    print("   ✅ Data storage initialized")
    
    print("🚀 Starting data collection (target: 100,000 frames)...")
    # Collect a total of at least 100,000 frames
    total_frames = 0
    episode_count = 0
    
    while total_frames < 100000:
        print(f"\n📈 Episode {episode_count + 1} | Total frames: {total_frames}/100,000 ({total_frames/1000:.1f}%)")
        
        obs, info = env.reset()
        if total_frames == 0:
            print(f"🔍 Initial observation analysis:")
            print(f"   Type: {type(obs)}")
            if isinstance(obs, dict):
                print(f"   Keys: {obs.keys()}")
                for key, value in obs.items():
                    print(f"     {key}: shape={getattr(value, 'shape', 'N/A')}, dtype={getattr(value, 'dtype', type(value))}")
        
        done = False
        episode_frames = 0
        episode_reward = 0
        
        while not done and total_frames < 100000:
            # Sample a random action from the environment's action space
            action = env.action_space.sample()
            
            # Step the environment
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            
            try:
                # Get the rendered image from the environment
                pixel_obs = env.render()
                
                # Resize the observation to 64x64 pixels
                img = Image.fromarray(pixel_obs).resize((64, 64))
                
                # Store the collected data
                observations.append(np.array(img))
                actions.append(action)
                rewards.append(reward)
                terminals.append(done)
                
                total_frames += 1
                episode_frames += 1
                episode_reward += reward
                
                # Progress updates every 1000 frames
                if total_frames % 1000 == 0:
                    print(f"   ⚡ Collected {total_frames} frames ({total_frames/1000:.1f}% complete)")
                    
            except Exception as e:
                print(f"   ❌ Error during frame {total_frames}: {e}")
                raise
        
        episode_count += 1
        print(f"   🏁 Episode {episode_count} completed: {episode_frames} frames, reward: {episode_reward:.2f}")
    
    print(f"\n💾 Saving dataset...")
    print(f"   📊 Final stats: {total_frames} frames across {episode_count} episodes")
    
    # Save the dataset to a single file
    print("   📁 Saving main dataset file...")
    np.savez_compressed(
        '/outputs/cartpole_swingup_random_100k.npz',
        observations=np.array(observations),
        actions=np.array(actions),
        rewards=np.array(rewards),
        terminals=np.array(terminals),
    )
    print("   ✅ Main dataset saved as 'cartpole_swingup_random_100k.npz'")
    
    # Save a single 64x64 PNG image of one frame from the dataset
    print("   🖼️  Saving sample frame...")
    Image.fromarray(observations[0]).save('/outputs/sample_frame.png')
    print("   ✅ Sample frame saved as 'sample_frame.png'")
    
    print(f"\n🎉 Data generation completed successfully!")
    print(f"   📊 Total frames collected: {total_frames}")
    print(f"   🎬 Total episodes: {episode_count}")
    print(f"   📁 Files saved to /outputs/")


def sample_images_from_dataset(npz_file_path, num_samples=5, save_dir="/outputs"):
    """
    Sample and save consecutive frames from the dataset to show environment dynamics.
    
    Args:
        npz_file_path (str): Path to the .npz dataset file
        num_samples (int): Number of consecutive frames to sample (default: 5)
        save_dir (str): Directory to save the sampled images
    """
    print(f"🎬 Sampling {num_samples} consecutive frames from dataset...")
    print(f"   📁 Loading dataset from: {npz_file_path}")
    
    # Load the dataset
    try:
        data = np.load(npz_file_path)
        observations = data['observations']
        actions = data['actions']
        rewards = data['rewards']
        terminals = data['terminals']
        
        print(f"   ✅ Dataset loaded successfully!")
        print(f"   📊 Dataset info:")
        print(f"     - Total frames: {len(observations)}")
        print(f"     - Image shape: {observations[0].shape}")
        print(f"     - Actions shape: {actions[0].shape}")
        print(f"     - Reward range: [{rewards.min():.2f}, {rewards.max():.2f}]")
        
    except Exception as e:
        print(f"   ❌ Error loading dataset: {e}")
        return
    
    # Find a good starting point that won't go beyond the dataset
    total_frames = len(observations)
    max_start_idx = total_frames - num_samples
    start_idx = np.random.randint(0, max_start_idx)
    
    # Get consecutive frame indices
    sample_indices = list(range(start_idx, start_idx + num_samples))
    
    print(f"   🎲 Selected consecutive frames: {start_idx} → {start_idx + num_samples - 1}")
    
    # Load original environment to decode observations
    print(f"   🔍 Decoding state information...")
    
    # Save individual sample images with detailed info
    frame_data = []
    for i, idx in enumerate(sample_indices):
        obs_img = observations[idx]
        action = actions[idx]
        reward = rewards[idx]
        terminal = terminals[idx]
        
        # Convert to PIL Image and save
        img = Image.fromarray(obs_img)
        filename = f"consecutive_{i+1:02d}_frame_{idx:06d}.png"
        filepath = f"{save_dir}/{filename}"
        img.save(filepath)
        
        # Extract and format values
        action_val = float(action[0]) if hasattr(action, '__len__') else float(action)
        reward_val = float(reward)
        
        frame_info = {
            'frame_num': int(idx),
            'step': i + 1,
            'action': action_val,
            'reward': reward_val,
            'terminal': terminal,
            'image': obs_img
        }
        frame_data.append(frame_info)
        
        print(f"   💾 Saved {filename}")
        print(f"     - Step {i+1}: Frame {int(idx)}, Action={action_val:.3f}, Reward={reward_val:.3f}, Terminal={terminal}")
    
    # Create enhanced grid visualization
    print(f"   🎨 Creating detailed consecutive frames visualization...")
    
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    
    # Create a large figure for detailed visualization
    fig = plt.figure(figsize=(20, 12))
    
    # Title
    fig.suptitle(f'Consecutive Frame Analysis: Frames {start_idx} → {start_idx + num_samples - 1}', 
                fontsize=16, fontweight='bold', y=0.95)
    
    # Create subplots - 2 rows: images on top, detailed info below
    gs = fig.add_gridspec(3, num_samples, height_ratios=[2, 1, 0.5], hspace=0.3, wspace=0.2)
    
    for i, frame_info in enumerate(frame_data):
        # Image subplot
        ax_img = fig.add_subplot(gs[0, i])
        ax_img.imshow(frame_info['image'])
        ax_img.set_title(f"Step {frame_info['step']}\nFrame {frame_info['frame_num']}", 
                        fontsize=12, fontweight='bold')
        ax_img.axis('off')
        
        # Add step arrow
        if i < len(frame_data) - 1:
            # Add arrow between frames
            ax_arrow = fig.add_subplot(gs[1, i])
            ax_arrow.annotate('', xy=(0.8, 0.5), xytext=(0.2, 0.5),
                            arrowprops=dict(arrowstyle='->', lw=3, color='red'))
            ax_arrow.text(0.5, 0.7, f'Action: {frame_info["action"]:.3f}', 
                         ha='center', va='center', fontsize=10, fontweight='bold')
            ax_arrow.text(0.5, 0.3, f'→ Reward: {frame_data[i+1]["reward"]:.3f}', 
                         ha='center', va='center', fontsize=10, color='green')
            ax_arrow.set_xlim(0, 1)
            ax_arrow.set_ylim(0, 1)
            ax_arrow.axis('off')
        
        # Detailed info subplot
        ax_info = fig.add_subplot(gs[2, i])
        info_text = f"""Frame: {frame_info['frame_num']}
Action: {frame_info['action']:.4f}
Reward: {frame_info['reward']:.4f}
Terminal: {frame_info['terminal']}"""
        
        ax_info.text(0.5, 0.5, info_text, ha='center', va='center', 
                    fontsize=9, bbox=dict(boxstyle="round,pad=0.3", facecolor='lightblue', alpha=0.7))
        ax_info.set_xlim(0, 1)
        ax_info.set_ylim(0, 1)
        ax_info.axis('off')
    
    # Add summary statistics
    total_reward = sum(f['reward'] for f in frame_data)
    avg_action = np.mean([f['action'] for f in frame_data])
    
    fig.text(0.5, 0.02, f'Sequence Summary: Total Reward = {total_reward:.4f}, Avg Action = {avg_action:.4f}, Terminal States = {sum(f["terminal"] for f in frame_data)}', 
             ha='center', fontsize=12, bbox=dict(boxstyle="round,pad=0.5", facecolor='yellow', alpha=0.8))
    
    # Save the detailed visualization
    detailed_grid_filepath = f"{save_dir}/consecutive_frames_analysis.png"
    plt.savefig(detailed_grid_filepath, dpi=200, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Detailed visualization saved as 'consecutive_frames_analysis.png'")
    
    # Also create a simple grid for quick viewing
    fig, axes = plt.subplots(1, num_samples, figsize=(3*num_samples, 4))
    if num_samples == 1:
        axes = [axes]
    
    for i, frame_info in enumerate(frame_data):
        axes[i].imshow(frame_info['image'])
        axes[i].set_title(f"Step {frame_info['step']}\nA:{frame_info['action']:.3f}, R:{frame_info['reward']:.3f}", 
                        fontsize=10)
        axes[i].axis('off')
    
    plt.suptitle(f'Consecutive Frames {start_idx} → {start_idx + num_samples - 1}', fontsize=14)
    plt.tight_layout()
    simple_grid_filepath = f"{save_dir}/consecutive_frames_simple.png"
    plt.savefig(simple_grid_filepath, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"   ✅ Simple grid saved as 'consecutive_frames_simple.png'")
    print(f"\n🎉 Consecutive frame analysis completed!")
    print(f"   📊 Generated {len(frame_data)} individual images + 2 grid visualizations")
    print(f"   🎬 Analyzed frames {start_idx} → {start_idx + num_samples - 1}")
    print(f"   📈 Sequence stats: Total reward = {total_reward:.4f}, Avg action = {avg_action:.4f}")
    print(f"   📁 All files saved to {save_dir}/")
