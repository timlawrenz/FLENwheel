#!/usr/bin/env python3
"""
Test ComfyUI connection and get workflow structure.

Run this to verify ComfyUI is accessible and see what workflows are available.
"""

import sys
import json
from pathlib import Path

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'lib'))

from comfyui_client import ComfyUIClient, ComfyUIError

def main():
    print("=" * 80)
    print("ComfyUI Connection Test")
    print("=" * 80)
    
    # Connect to ComfyUI
    client = ComfyUIClient(base_url="http://127.0.0.1:8188")
    
    try:
        # Test 1: Get system stats
        print("\n1. Testing connection...")
        stats = client.get_system_stats()
        print(f"   ✓ Connected to ComfyUI")
        print(f"   VRAM: {stats.get('system', {}).get('vram', {})}")
        
        # Test 2: Check if we can access object info (available nodes)
        print("\n2. Checking available nodes...")
        response = client.session.get(f"{client.base_url}/object_info")
        if response.ok:
            nodes = response.json()
            qwen_nodes = [n for n in nodes.keys() if 'qwen' in n.lower() or 'Qwen' in n]
            print(f"   ✓ Found {len(nodes)} node types")
            if qwen_nodes:
                print(f"   ✓ Qwen-related nodes: {qwen_nodes}")
            else:
                print("   ⚠ No Qwen nodes found - may need to install custom nodes")
        
        # Test 3: Check queue
        print("\n3. Checking queue status...")
        response = client.session.get(f"{client.base_url}/queue")
        if response.ok:
            queue = response.json()
            pending = len(queue.get('queue_pending', []))
            running = len(queue.get('queue_running', []))
            print(f"   ✓ Queue: {running} running, {pending} pending")
        
        print("\n" + "=" * 80)
        print("✓ ComfyUI is ready!")
        print("=" * 80)
        print("\nNext steps:")
        print("1. Load a Qwen workflow in ComfyUI")
        print("2. Save as 'API Format' (not 'Workflow')")
        print("3. Place in: workflows/qwen_edit.json")
        print("4. Run: python scripts/generate_with_comfyui.py")
        
        return 0
        
    except ComfyUIError as e:
        print(f"\n✗ Error: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
