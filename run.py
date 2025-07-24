import modal

stub = modal.App("mvh-salvo-mini")

volume = modal.Volume.from_name("mvh-salvo-mini-outputs", create_if_missing=True)

image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install("xvfb", "libgl1-mesa-glx", "libosmesa6", "libglfw3", "mesa-utils")
    .env({"MUJOCO_GL": "egl"})
    .pip_install(
        "torch==2.3.1",
        "torchvision==0.18.1",
        "shimmy[dm-control]",
        "gymnasium==1.0.0a2",
        "transformers==4.41.2",
        "accelerate==0.30.1",
        "tensorboard==2.16.2",
        "pandas==2.2.2",
        "moviepy==1.0.3",
        "scikit-image==0.23.2",
        "numpy",
        "Pillow",
        "mujoco",
        "matplotlib",
    )
    .add_local_python_source("src")
)

@stub.function(
    image=image,
    volumes={"/outputs": volume},
    gpu="T4",  # Use GPU for better rendering support
    timeout=2400,  # 40 minutes timeout for 100k frame collection
)
def collect_data():
    """Generates and saves a 100,000-frame dataset from the dm_control
    Cartpole-swingup environment using a random policy."""
    import time
    
    print("🚀 Starting data collection process...")
    print("🎮 Using GPU with EGL rendering - attempting direct execution...")
    
    start_time = time.time()
    
    try:
        # Try direct execution first (GPU should support EGL without xvfb)
        from src.data_generation import generate_data
        generate_data()
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("-" * 50)
        print(f"⏱️  Total execution time: {duration:.2f} seconds")
        print("✅ Data generation completed successfully!")
        
    except Exception as e:
        print(f"❌ Direct execution failed: {e}")
        
        # Fallback to xvfb approach
        print("🔄 Falling back to xvfb virtual display...")
        import subprocess
        import sys
        
        cmd = [
            "xvfb-run", "-a", "-s", "-screen 0 1024x768x24",
            sys.executable, "-c", 
            "from src.data_generation import generate_data; generate_data()"
        ]
        print(f"   Command: {' '.join(cmd)}")
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            bufsize=1
        )
        
        print("📊 Fallback output:")
        print("-" * 50)
        
        for line in process.stdout:
            print(f"   {line.rstrip()}")
        
        process.wait()
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("-" * 50)
        print(f"⏱️  Total execution time: {duration:.2f} seconds")
        
        if process.returncode == 0:
            print("✅ Data generation completed successfully (via fallback)!")
        else:
            print(f"❌ Both direct and fallback execution failed")
            raise RuntimeError(f"Data generation failed with return code: {process.returncode}")

@stub.function(
    image=image,
    volumes={"/outputs": volume},
)
def sample_dataset_images(num_samples=5):
    """Sample and visualize random images from the collected dataset."""
    import time
    
    print("🖼️  Starting dataset image sampling...")
    
    dataset_path = "/outputs/cartpole_swingup_random_100k.npz"
    
    # Check if dataset exists
    import os
    if not os.path.exists(dataset_path):
        print(f"❌ Dataset not found at {dataset_path}")
        print("   Please run collect_data() first to generate the dataset.")
        return
    
    start_time = time.time()
    
    try:
        from src.data_generation import sample_images_from_dataset
        sample_images_from_dataset(dataset_path, num_samples=num_samples)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("-" * 50)
        print(f"⏱️  Total sampling time: {duration:.2f} seconds")
        print("✅ Dataset image sampling completed successfully!")
        
    except Exception as e:
        print(f"❌ Image sampling failed: {e}")
        raise

@stub.function(image=image)
def test_import():
    try:
        from dm_control.suite.gym import SUITE
        print("Successfully imported dm_control.suite.gym.SUITE")
    except ImportError as e:
        print(f"Failed to import: {e}")

@stub.local_entrypoint()
def main():
    # Collect data first
    collect_data.remote()
    
    # Then sample images for visualization
    print("\n" + "="*60)
    print("📸 Now sampling images from the collected dataset...")
    print("="*60)
    sample_dataset_images.remote(num_samples=5)

@stub.local_entrypoint()
def sample_only():
    """Just sample images from existing dataset without collecting new data."""
    print("📸 Sampling images from existing dataset...")
    sample_dataset_images.remote(num_samples=5)
